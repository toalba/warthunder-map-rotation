# Used to test the API and the data that is returned
import requests
import json
from show_data import graph_lastone, graph_lastten
s = requests.Session()
cookies = None
with open("cookies.json") as json_file:
    cookies = json.load(json_file)
s.cookies.update(cookies) 

def analyser(data,max_date):
    filtered_data = list(filter(lambda x: x['endTime'] > max_date, data))
    for i in data:
        if i['endTime'] < max_date:
            return filtered_data,True
    return filtered_data, False

def map_analyser(map_item,mapcount={}):
    title = map_item['title']
    map = title.split("] ")[1]
    #if map has (winter) in it then remove it
    if "(winter)" in map:
        map = map.replace(" (winter)","")
    if map in mapcount:
        mapcount[map]['count'] += 1
        mapcount[map]['sessions'].append(map_item['sessionId'])
    else:
        # if the map is not in the dictionary then add it
        mapcount[map] = {}
        mapcount[map]['count'] = 1
        mapcount[map]['sessions'] = [map_item['sessionId']]
    return mapcount


def get_map_data():
    data = json.loads(open("data.json").read())
    nextpage=1
    current_time = 0
    ten_min_past = 0
    ten_min_meet = False
    raw_maps = []
    while not ten_min_meet:
        data['page']=nextpage
        r = s.post("https://warthunder.com/en/api/replay",json=data)
        rjson = r.json()
        items = rjson['items']
        if nextpage == 1:
            current_time = rjson['items'][0]['endTime']
            ten_min_past = current_time - 600
        raw, ten_min_meet = analyser(items,ten_min_past)
        raw_maps.extend(raw)
        nextpage=rjson['pagination']['nextNum']
        r.close()
    with open("maps.json", "w") as outfile:
        outfile.write(json.dumps(raw_maps, indent=4))

def plot_ten():
    with open("maps.json") as json_file:
        data = json.load(json_file)
        mapcount = {}
        for i in data:
            mapcount.update(map_analyser(i,mapcount))
        umap_list = [[k,mapcount[k]['count']] for k,v in mapcount.items()]
        fig = graph_lastten(sorted(umap_list))
        return fig
    
def plot_one():
    with open("maps.json") as json_file:
        data = json.load(json_file)
        filtered_data = list(filter(lambda x: x['endTime'] > data[0]['endTime']-70, data))
        mapcount = {}
        for i in filtered_data:
            mapcount.update(map_analyser(i,mapcount))
        umap_list = [[k,mapcount[k]['count']] for k,v in mapcount.items()]
        fig = graph_lastone(sorted(umap_list))
        return fig
    
if __name__ == "__main__":
    plot_one().show()