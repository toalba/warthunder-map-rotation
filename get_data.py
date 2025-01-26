# Used to test the API and the data that is returned
import requests
import json
from show_data import graph
s = requests.Session()
cookies = None
with open("cookies.json") as json_file:
    cookies = json.load(json_file)
s.cookies.update(cookies) 

def analyser(data,max_date,mapcount={}):
    for i in data:
        if i['statisticGroup'] != "tank":
            print("Not a tank replay")
        if i['endTime'] < max_date:
            return mapcount, True
        title = i['title']
        map = title.split("] ")[1]
        #if map has (winter) in it then remove it
        if "(winter)" in map:
            map = map.replace(" (winter)","")
        if map in mapcount:
            mapcount[map]['count'] += 1
            mapcount[map]['sessions'].append(i['sessionId'])
        else:
            # if the map is not in the dictionary then add it
            mapcount[map] = {}
            mapcount[map]['count'] = 1
            mapcount[map]['sessions'] = [i['sessionId']]
    return mapcount, False


def get_map_data():
    data = json.loads(open("data.json").read())
    nextpage=1
    current_time = 0
    ten_min_past = 0
    ten_min_meet = False
    raw_maps = {}
    while not ten_min_meet:
        data['page']=nextpage
        r = s.post("https://warthunder.com/en/api/replay",json=data)
        rjson = r.json()
        items = rjson['items']
        if nextpage == 1:
            current_time = rjson['items'][0]['endTime']
            ten_min_past = current_time - 600
        raw_maps, ten_min_meet = analyser(items,ten_min_past,raw_maps)
        nextpage=rjson['pagination']['nextNum']
        r.close()
    umap_list = [[k,raw_maps[k]['count']] for k,v in raw_maps.items()]
    with open("maps.json", "w") as outfile:
        outfile.write(json.dumps(umap_list, indent=4))

def plot():
    with open("maps.json") as json_file:
        data = json.load(json_file)
        fig = graph(sorted(data))
        return fig

# Get the last date of the data