import sys
import git_info
import yaml
import os
from datetime import datetime
from jinja2 import Template
from collections import defaultdict

from translate import Translate

def dtree(): return defaultdict(dtree)

def get_leaf(t, where):
	for i in where:
		t = t[i]
	return t

def get_diff(commit1, commit2, file_name):
	state = file_name[0][0]

	cur_name = file_name[1].split('/')[-1]
	info = None
	word_count = (-1, -1)

	exist = git_info.is_exist(commit2, file_name[1])
	doc_words = 0

	if state == 'M':
		if exist:
			word_count, info = git_info.get_modified_info(commit1, commit2, file_name)
			doc_words = git_info.get_git_word_count(commit1, file_name[1])
		state = 'Modified'
	elif state == 'A':
		doc_words = git_info.get_git_word_count(commit2, file_name[1])
		word_count = (doc_words, 0)
		state = 'Added'
	elif state == 'R':
		cur_name = file_name[2].split('/')[-1]
		doc_words = git_info.get_git_word_count(commit2, file_name[2])
		state = 'Renamed'
	elif state == 'D':
		state = 'Deleted'

	return {'dir': file_name[1],
		'name': file_name[1].split('/')[-1],
		'new_name': cur_name,
		'word_count': word_count,
		'doc_words': doc_words,
		'state': state,
		'info': info}

def preorder(t, li, depth = 0):
	for k, v in t.items():
		if k != '/data/':
			li.append({'level': depth, 'data': k, 'is_leaf': False})
			preorder(t[k], li, depth + 1)
		else:
			li.pop()
			li.append({'level': depth-1, 'data': v, 'is_leaf': True})

def render_page(title, tree, c1, c2, md_file, stat):
	tree_list = []
	remotes = {}
	for i in git_info.get_remote():
		remotes[i[1]] = i[0]

	trans_list = git_info.get_files(c1)
	trans_list = [x for x in trans_list if not is_untracking_file(c1, x)]

	orig_list = git_info.get_files(c2)
	orig_list = [x for x in orig_list if not is_untracking_file(c2, x)]

	origin_info = {'commit': git_info.get_commit_str(c2),
			'date': git_info.get_commit_date(c2),
			'file_num': len(orig_list),
			'url': remotes['upstream']}

	trans_info = {'commit': git_info.get_commit_str(c1),
			'date': git_info.get_commit_date(c1),
			'file_num': len(trans_list),
			'url': remotes['origin']}
	
	preorder(tree, tree_list)
	fi= open('scripts/template.txt')
	template = Template(fi.read())
	with open('../' + md_file, "w") as f:
		f.write(template.render(title=title, date=datetime.today().strftime('%Y-%m-%d'), res_tree=tree_list, origin_info=origin_info, trans_info=trans_info, status=stat))

def is_untracking_file(commit, file_dir):
	return file_dir.startswith('.') or '/.' in file_dir or not (file_dir.endswith('.md') or file_dir.endswith('.markdown'))
	
def main(commit1, commit2, md_file, settings):
	files = git_info.get_diff_files(commit1, commit2)
	tree = dtree()
	file_stat = {'Added': 0, 'Modified': 0, 'Deleted': 0, 'Renamed': 0}
	for f in files:
		f_dir = f[1].split('/')
		if is_untracking_file(commit2, f[1]):
			continue
		diff = get_diff(commit1, commit2, f)
		file_stat[diff['state']] += 1
		leaf = get_leaf(tree, f_dir)
		leaf['/data/'] = diff

	if os.path.exists('../' + md_file):
		ran_num = 1
		while os.path.exists('../' + md_file.replace('.', f'({ran_num}).')):
			ran_num += 1
		render_page(settings['document']['title'] + f' ({ran_num})', tree, commit1, commit2, md_file.replace('.', f'({ran_num}).'), file_stat)
	else:
		render_page(settings['document']['title'], tree, commit1, commit2, md_file, file_stat)


if __name__ == '__main__':
	with open('settings.yml') as f:
		settings = yaml.load(f, yaml.FullLoader)
	translate = Translate()
	translate.set_api_key(settings['keys']['translate-api'])

	main(sys.argv[1], sys.argv[2], sys.argv[3], settings)
	translate.save_translate_cache()