import json

with open("mdpo/settings.json", "r") as json_file:
    dict1 = json.load(json_file)
    path_sum_sync=''
    path_sum_mdpo=''
    path_mkdir=''
    for k in dict1['path']:
        path_sum_mdpo+=k+' '
        path_sum_sync+='^'+k+'|'
        text_split=k.split('/')
        path_tmp=""

        for k in range(len(text_split)-1):
            path_tmp+=text_split[k]
            path_tmp+='/'
        path_tmp=path_tmp[:-1]
        path_mkdir+=path_tmp+' '
    dict1["path_sum_sync"] = path_sum_sync[:-1]
    dict1["path_sum_mdpo"] = path_sum_mdpo[:-1]
    dict1["path_mkdir"] = path_mkdir[:-1]
    del dict1["path"]
    with open("mdpo/settings_modified.json", "w") as json_w:
        json.dump(dict1, json_w)
