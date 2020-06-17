from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .util import random_album_img_urls, get_album_img_urls_to_list, current_album_img_urls, random_song_name
from .arena_util import load_json
from .recommend_model import dummy_func
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd


print("@@@@")
train = pd.DataFrame(load_json('train.json'))
print("####")
song_meta = pd.DataFrame(load_json('song_meta.json'))
# song_meta['id'] = song_meta['id'].astype('int')
print("$$$$")
plylst_song_map = pd.DataFrame(load_json('plylst_song_map.json'))
print("^^^^")
model_result = pd.DataFrame(load_json('model_result.json'))
print("&&&&")
model_result = pd.DataFrame(model_result)
print("~~~~")
def index(request):
    template = loader.get_template('musicApp/index.html')
    context = {
        'latest_question_list': "test",
    }
    temp = []
    res_dict = random_song_name(temp, 10)
    return render(request, 'musicApp/index.html', {'res_dict' : res_dict})

def get_recommend_music(request):
    if request.method == 'POST':
        recv_list = request.POST.getlist('nameList[]')
        print(recv_list)

        # model_result['songs']=model_result['songs'].astype('int')

        total_song=[] #노래아이디찾기
        for name in recv_list:
            total_song.append(song_meta[song_meta['song_name']==name]['id'].values[0])
        ply_dic={} #중복노래가 많은 plyId찾기   
        for song_temp in total_song:
            for i in plylst_song_map[plylst_song_map['songs']==song_temp]['id'] : 
                if i in ply_dic.keys():
                    ply_dic[i]+=1
                else:
                    ply_dic[i]=1
        ply_id = sorted(ply_dic.items(), key=lambda x: x[1], reverse=True)[0][0]
        outputList=pd.merge(model_result[model_result['id']==ply_id]['songs'],song_meta[['id','song_name']],left_on='songs',right_on='id')['song_name'].tolist()[:30]
        print(outputList)
        response_data = {}
        response_data['name'] = outputList
        response_data['album_img_url'] = get_album_img_urls_to_list(outputList)

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def update_list(request):
    if request.method == 'POST':
        recv_list = request.POST.getlist('nameList[]')
        # print("0.",  recv_list)
        response_data = {}
        
        nameTemp = []
        urlTemp = []
        selected = []

        outputList = current_album_img_urls(recv_list)

        for key, value in outputList.items():
            # print("1. ", key, ":", value)
            nameTemp.append(value['song_name'])
            urlTemp.append(value['img_url'])
            selected.append(1)

        outputList = random_album_img_urls(recv_list, 10)

        for key, value in outputList.items():
            # print("2. ", key, ":", value)
            nameTemp.append(value['song_name'])
            urlTemp.append(value['img_url'])
            selected.append(0)
        
        response_data['name'] = nameTemp
        response_data['album_img_url'] = urlTemp
        response_data['selected'] = selected

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
