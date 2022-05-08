import subprocess
import re
import sys

def get_files(commit1, commit2):
	out = subprocess.check_output(['git', 'diff', '--name-status', commit1, commit2], encoding='utf-8').splitlines()
	files = []
	for c in out:
		files.append(c.split())
	return files

def get_word_count(str):
	#p = re.compile('\w+')
	#words_list = [s for s in str.split() if p.match(s)]
	return len(str.split())


def is_exist(commit, file_name):
	out = subprocess.call(['git', 'cat-file', '-e', f'{commit}:{file_name}'], stderr=subprocess.DEVNULL)
	return out == 0

def get_diff(commit1, commit2, file_name):
	state = file_name[0]

	out = subprocess.check_output(['git', 'diff', commit1, commit2, '--word-diff=porcelain', file_name[1]], encoding='utf-8').splitlines()
	start_from = 0

	for i in range(len(out)):
		if out[i].startswith('@@'):
			start_from = i + 1
			break
	
	added = 0
	erased = 0

	for i in range(start_from, len(out)):
		if out[i].startswith('+'):
			added += get_word_count(out[i][1:])
		elif out[i].startswith('-'):
			erased += get_word_count(out[i][1:])

	return {'name': file_name[1],
		'state': state,
		'diff': (added, erased) }

def main(b1, b2):
	files = get_files(b1, b2)
	result = ""
	
	for f in files:
		if is_exist(b1, f[1]) and is_exist(b2, f[1]):
			diff = get_diff(b1, b2, f)
			result += f'~ File: {diff["name"]}\n'
			if diff['state'] == 'M':
				result += '\tFile Modified\n'
			elif diff['state'] == 'A':
				result += '\tFile Added\n'
			elif diff['state'] == 'R':
				result += '\tFile Renamed\n'
			elif diff['state'] == 'D':
				result += '\tFile Deleted\n'
			else:
				result += f'\t{diff["state"]}\n'

			result += f"\tAdded words: {diff['diff'][0]}, Deleted words: {diff['diff'][1]}\n"
	with open("report.txt", "w") as f:
		f.write(result)


if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])