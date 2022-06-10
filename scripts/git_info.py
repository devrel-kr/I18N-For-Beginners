import subprocess
import re
from translate import *
from langid import classify
from word_dist import *

re_modifiy = re.compile('\[-([\s\S]+?)-\]{\+([\s\S]+?)\+}')
re_added = re.compile('{\+([\s\S]+?)\+}')
re_erased = re.compile('\[-([\s\S]+?)-\]')

def get_word_count(str):
	return len(str.split())

def get_modified_info(commit1, commit2, file_name):
	added = 0
	erased = 0
	translated = 0
	trans_err = 0
	trans_count = 0
	Trans = Translate()
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
			try:
				lang_del = classify(deleted_word)[0]
				lang_add = classify(added_word)[0]
			except:
				lang_del = lang_add = 'err'

			if lang_del == lang_add:		# if text is just modified
				deleted_count = get_word_count(deleted_word)
				added_count = get_word_count(added_word)
				word_dist = levenshtein(deleted_word, added_word)

				mod_data.append({'translated': False, 'added': added_word, 'deleted': deleted_word, 'distance': round(word_dist / max(len(added_word), len(deleted_word)) * 100, 2), 'count': (added_count, deleted_count), 'line_no': line_no})
				added += added_count
				erased += deleted_count

			else:							# if text is translated
				orig_text = added_word
				tran_text = deleted_word
				tran_count = len(tran_text)
				deleted_count = get_word_count(tran_text)
				added_count = get_word_count(orig_text)
				if tran_count > 5:
					trans_sentence = Trans.translate(orig_text, 'en', 'ko')
					cos_sim = cos_similarity(tran_text, trans_sentence)
					trans_count += 1
					if cos_sim < 0.3:
						trans_err += 1
				else:
					cos_sim = -2

				mod_data.append({'translated': True, 'original': orig_text, 'translated': tran_text, 'simularity': cos_sim, 'line_no': line_no})
				translated += get_word_count(orig_text)

		# get added part
		iter = re_added.finditer(line)
		for m in iter:
			if m.start() >= 2 and line[m.start()-2: m.start()]:
				continue
			added_word = m.group(1)
			added_count = get_word_count(added_word)
			mod_data.append({'translated': False, 'added': added_word, 'deleted': None, 'distance': -1, 'count': (added_count, 0), 'line_no': line_no})
			added += added_count

		#get deleted part
		iter = re_erased.finditer(line)
		for m in iter:
			if line[m.end():m.end()+2] == '{+':
				continue
			deleted_word = m.group(1)
			deleted_count = get_word_count(deleted_word)
			mod_data.append({'translated': False, 'added': None, 'deleted': deleted_word, 'distance': -1, 'count': (0, deleted_count), 'line_no': line_no})
			erased += deleted_count
		line_no += 1

	trans_words = get_git_word_count(commit1, file_name[1])
	orig_words = get_git_word_count(commit2, file_name[1])
	info = {'section': mod_data,
		'mod_rate': round((added + erased) / (trans_words + orig_words) * 100, 2),
		'trans_rate': round(translated / orig_words * 100, 2),
		'trans_err': round(trans_err / trans_count * 100 if trans_count != 0 else 0, 2),
		'original_words': orig_words,
		'translate_words': trans_words,
		'translated': translated,
		'added': added,
		'erased': erased,}
	return (added, erased), info

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

def get_diff_files(commit1, commit2):
	out = subprocess.check_output(['git', 'diff', '--name-status', commit1, commit2], encoding='utf-8').splitlines()
	files = []
	for c in out:
		files.append(c.split())
	return files

def get_files(tree):
	return subprocess.check_output(['git', 'ls-tree', '--name-only', '-r', tree], encoding='utf-8').splitlines()

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
	out = subprocess.check_output(['git', 'rev-list', commit, '-n', '1'], encoding='utf-8').strip()
	return out

def get_commit_date(commit):
	return subprocess.check_output(['git', 'show', '-s', '--format=%ci', commit], encoding='utf-8').strip()
	