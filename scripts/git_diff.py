import subprocess
import re
import sys
from collections import defaultdict

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
	p = re.compile('\w+')
	words_list = [s for s in str.split() if p.match(s)]
	return len(words_list)


def is_exist(commit, file_name):
	out = subprocess.call(['git', 'cat-file', '-e', f'{commit}:{file_name}'], stderr=subprocess.DEVNULL)
	return out == 0

def is_textfile(commit, file_name):
	out = subprocess.check_output(['git', 'diff', '4b825dc642cb6eb9a060e54bf8d69288fbee4904', commit, '--numstat', file_name], encoding='utf-8')
	num_data = out.split()
	return num_data[0] != '-'

def get_git_word_count(commit, file_name):
	if is_exist(commit, file_name) == False: return 0
	out = subprocess.Popen(['git', 'cat-file', '-p', f'{commit}:{file_name}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = subprocess.Popen(['wc'], stdin=out.stdout, stdout=subprocess.PIPE).communicate()
	wordcount = int(out.decode('utf-8').split()[1])
	return wordcount

def get_diff(commit1, commit2, file_name):
	state = file_name[0][0]
	
	added = 0
	erased = 0
	added_rate = 0
	erased_rate = 0

	cur_name = file_name[1].split('/')[-1]

	if state == 'M':
		if is_exist(commit2, file_name) and is_textfile(commit2, file_name):
			word_count = get_git_word_count(commit1, file_name[1])
			out = subprocess.check_output(['git', 'diff', commit1, commit2, '--word-diff=porcelain', file_name[1]], encoding='utf-8').splitlines()
			start_from = 0

			for i in range(len(out)):
				if out[i].startswith('@@'):
					start_from = i + 1
					break

			for i in range(start_from, len(out)):
				if out[i].startswith('+'):
					added += get_word_count(out[i][1:])
				elif out[i].startswith('-'):
					erased += get_word_count(out[i][1:])

			added_rate = (added / word_count) if word_count != 0 else 1
			erased_rate = (erased / word_count) if word_count != 0 else 0
		state = 'File Modified'
	elif state == 'A':
		added_rate = 1
		state = 'File Added'
	elif state == 'R':
		cur_name = file_name[2].split('/')[-1]
		state = 'File Renamed'
	elif state == 'D':
		state = 'File Deleted'

	return {'name': file_name[1].split('/')[-1],
		'new_name': cur_name,
		'state': state,
		'diff': (added, erased),
		'diff_rate': (added_rate, erased_rate)}

def ptr(t, file, depth = 0):
	for k, v in t.items():
		if k != '/data/':
			file.write("%s └ %s\n" % ("".join(depth * ["    "]), k))
			depth += 1
			ptr(t[k], file, depth)
			depth -= 1
		else:
			file.write("%s -- %s\n" % ("".join(depth * ["    "]), v))
	file.write('\n')

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

def main(commit1, commit2):
	files = get_files(commit1, commit2)
	tree = dtree()
	result = ""
	for f in files:
		f_dir = f[1].split('/')
		diff = get_diff(commit1, commit2, f)
		leaf = get_leaf(tree, f_dir)
		leaf['/data/'] = diff
		result += f'~ File: {diff["name"]}\n'
		result += f'\t{diff["state"]}\n'

		result += f"\tAdded words: {diff['diff'][0]}, Deleted words: {diff['diff'][1]}\n"
			
	with open("report.txt", "w") as f:
		f.write(result)
	
	import json
	with open("json.txt", "w") as f:
		f.write(json.dumps(tree))

	print_report_by_tree(tree, commit1, commit2)


if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])