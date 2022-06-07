import subprocess
import re
from word_dist import levenshtein

re_modifiy = re.compile('\[-([\s\S]+?)-\]{\+([\s\S]+?)\+}')
re_added = re.compile('[^-][^\]]{\+([\s\S]+?)\+}')
re_erased = re.compile('\[-([\s\S]+?)-\]')

def get_word_count(str):
	return len(str.split())

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


def get_commit_str(commit):
	out = subprocess.check_output(['git', 'rev-list', commit, '-n', '1'], encoding='utf-8')
	return out