import subprocess
import re
import sys
import json
from jinja2 import Template
from collections import defaultdict
from word_dist import levenshtein

re_modifiy = re.compile('\[-([\s\S]+?)-\]{\+([\s\S]+?)\+}')
re_added = re.compile('[^-][^\]]{\+([\s\S]+?)\+}')
re_erased = re.compile('\[-([\s\S]+?)-\]')

def dtree(): return defaultdict(dtree)

def get_leaf(t, where):
	for i in where:
		t = t[i]
	return t

def get_remote():
	remotes = subprocess.check_output(['git', 'remote', '-v'], encoding='utf-8').splitlines()
	remote_url = []
	for c in remotes:
		rem= c.split()
		rem_name = rem[0]
		url = rem[1]
		if (url, rem_name) not in remote_url:
			remote_url.append((url, rem_name))
	return remote_url

def get_files(commit1, commit2):
	out = subprocess.check_output(['git', 'diff', '--name-status', commit1, commit2], encoding='utf-8').splitlines()
	files = []
	for c in out:
		files.append(c.split())
	return files

def get_word_count(str):
	#p = re.compile('\w+')
	#words_list = [s for s in str.split() if p.match(s)]
	#return len(words_list)
	return len(str.split())


def is_exist(commit, file_name):
	out = subprocess.call(['git', 'cat-file', '-e', f'{commit}:{file_name}'], stderr=subprocess.DEVNULL)
	return out == 0

def is_textfile(commit, file_name):
	out = subprocess.check_output(['git', 'diff', '4b825dc642cb6eb9a060e54bf8d69288fbee4904', commit, '--numstat', '--', file_name], encoding='utf-8')
	num_data = out.split()
	if len(num_data) == 0:
		return False
	return num_data[0] != '-'

def get_git_word_count(commit, file_name):
	if is_exist(commit, file_name) == False: return 0
	out = subprocess.Popen(['git', 'cat-file', '-p', f'{commit}:{file_name}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = subprocess.Popen(['wc'], stdin=out.stdout, stdout=subprocess.PIPE).communicate()
	wordcount = int(out.decode('utf-8').split()[1])
	return wordcount

def get_modified_info(commit1, commit2, file_name):
	added = 0
	erased = 0

	mod_data = []

	out = subprocess.check_output(['git', 'diff', commit1, commit2, '--word-diff', '--', file_name[1]], encoding='utf-8').splitlines()
	line_no = 0

	for line in out:
		# get modified part
		if line.startswith('@@'):
			sp = line.split()[2]
			line_no = int(sp[1:].split(',')[0])
			continue
		
		iter = re_modifiy.finditer(line)
		for m in iter:
			deleted_word = m.group(1)
			added_word = m.group(2)

			deleted_count = get_word_count(deleted_word)
			added_count = get_word_count(added_word)
			word_dist = levenshtein(deleted_word, added_word)

			mod_data.append({'added': added_word, 'deleted': deleted_word, 'distance': word_dist, 'count': (added_count, deleted_count), 'line_no': line_no})
			added += added_count
			erased += deleted_count

		# get added part
		iter = re_added.finditer(line)
		for m in iter:
			added_word = m.group(1)
			added_count = get_word_count(added_word)
			mod_data.append({'added': added_word, 'deleted': None, 'distance': None, 'count': (added_count, 0), 'line_no': line_no})
			added += added_count

		#get deleted part
		iter = re_erased.finditer(line)
		for m in iter:
			if line[m.end():m.end()+2] == '{+':
				continue
			deleted_word = m.group(1)
			deleted_count = get_word_count(deleted_word)
			mod_data.append({'added': None, 'deleted': deleted_word, 'distance': None, 'count': (0, deleted_count), 'line_no': line_no})
			erased += deleted_count
		line_no += 1

	return (added, erased), mod_data

def get_diff(commit1, commit2, file_name):
	state = file_name[0][0]

	cur_name = file_name[1].split('/')[-1]
	info = None
	word_count = (-1, -1)

	exist = is_exist(commit2, file_name[1])
	doc_words = 0

	if state == 'M':
		if exist and is_textfile(commit2, file_name[1]):
			word_count, info = get_modified_info(commit1, commit2, file_name)
			doc_words = get_git_word_count(commit1, file_name[1])
		state = 'File Modified'
	elif state == 'A':
		if is_textfile(commit2, file_name[1]):
			word_count = (get_git_word_count(commit2, file_name[1]), 0)
			doc_words = get_git_word_count(commit2, file_name[1])
		state = 'File Added'
	elif state == 'R':
		cur_name = file_name[2].split('/')[-1]
		doc_words = get_git_word_count(commit2, file_name[2])
		state = 'File Renamed'
	elif state == 'D':
		state = 'File Deleted'

	return {'name': file_name[1].split('/')[-1],
		'new_name': cur_name,
		'word_count': word_count,
		'doc_words': doc_words,
		'state': state,
		'info': info}

def ptr(t, file, depth = 0):
	for k, v in t.items():
		if k != '/data/':
			file.write("%s └ %s\n" % ("".join(depth * ["    "]), k))
			ptr(t[k], file, depth + 1)
		else:
			file.write("%s -- %s\n" % ("".join(depth * ["    "]), v))
	file.write('\n')

def preorder(t, li, depth = 0):
	for k, v in t.items():
		if k != '/data/':
			li.append({'level': depth, 'data': k, 'is_leaf': False})
			preorder(t[k], li, depth + 1)
		else:
			li.pop()
			li.append({'level': depth-1, 'data': v, 'is_leaf': True})

def get_commit_str(commit):
	out = subprocess.check_output(['git', 'rev-list', commit, '-n', '1'], encoding='utf-8')
	return out

def print_report_by_tree(tree, c1, c2):
	result_tree = open('report_tree.txt', 'w')
	for i in get_remote():
		result_tree.write(f'{i[0]}\t{i[1]}\n')
	result_tree.write('\n')
	result_tree.write(f'recent commit:  \t{get_commit_str(c1)}')
	result_tree.write(f'outdated commit: \t{get_commit_str(c2)}')
	result_tree.write('\n/\n')
	ptr(tree, result_tree)
	result_tree.close()

def render_page(tree, c1, c2, md_file):
	tree_list = []
	remotes = {}
	for i in get_remote():
		remotes[i[1]] = i[0]
	preorder(tree, tree_list)
	fi= open('template.txt')
	template = Template(fi.read())
	with open(md_file, "w") as f:
		f.write(template.render(title='title', date='2022-06-03', res_tree=tree_list, repos=remotes, old_hash=get_commit_str(c1), new_hash=get_commit_str(c2)))

def main(commit1, commit2, md_file):
	files = get_files(commit1, commit2)
	tree = dtree()
	for f in files:
		f_dir = f[1].split('/')
		diff = get_diff(commit1, commit2, f)
		leaf = get_leaf(tree, f_dir)
		leaf['/data/'] = diff
	
	with open("json.txt", "w") as f:
		f.write(json.dumps(tree))

	print_report_by_tree(tree, commit1, commit2)
	render_page(tree, commit1, commit2, md_file)


if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2], sys.argv[3])