import json

with open("mdpo/settings.json", "r") as json_file:
    dict1 = json.load(json_file)
    path_sum_sync=''
    path_sum_mdpo=''
    for k in dict1['path']:
        path_sum_mdpo+=k+' '
        path_sum_sync+='^'+k+'|'
    dict1["path_sum_sync"] = path_sum_sync[:-1]
    dict1["path_sum_mdpo"] = path_sum_mdpo[:-1]
    del dict1["path"]
    with open("mdpo/settings_modified.json", "w") as json_w:
        json.dump(dict1, json_w)
