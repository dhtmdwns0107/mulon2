import numpy as np
import pandas as pd
from django.conf import settings

def random_song_name(curr_list, num):
    df = pd.read_csv(settings.MUSIC_SONG_META_TOP_200_URL_PATH)
    df = df[['song_name', 'album_name', 'img_url']]

    for drop_item in curr_list:
        df = df.drop(df[df.song_name == drop_item].index)

    sample_df = df.sample(n=num)
    res = sample_df.to_dict(orient="index")    
    return res

def random_album_img_urls(curr_list, num):
    df = pd.read_csv(settings.MUSIC_SONG_META_TOP_200_URL_PATH)
    df = df[['song_name', 'album_name', 'img_url']]

    for drop_item in curr_list:
        df = df.drop(df[df.song_name == drop_item].index)

    sample_df = df.sample(n=num)
    res = sample_df.to_dict(orient="index")
    return res

def current_album_img_urls(curr_list):
    df = pd.read_csv(settings.MUSIC_SONG_META_TOP_200_URL_PATH)
    df = df[['song_name', 'album_name', 'img_url']]
    
    new_df = pd.DataFrame(columns=['song_name', 'album_name', 'img_url'])
    for get_item in curr_list:
        new_df = new_df.append(df[df.song_name == get_item])
    
    res = new_df.to_dict(orient="index")
    return res

def get_album_img_urls_to_list(music_list):
    df = pd.read_csv(settings.MUSIC_SONG_META_TOP_URL_PATH)
    new_df = pd.DataFrame(columns=['album_name', 'img_url'])
    for item in music_list:
        if df[df['album_name'] == item].empty:
            new_df = new_df.append(pd.DataFrame([{'album_name': item, 'img_url': 'None'}]), ignore_index=True)
        else:
            new_df = new_df.append(pd.DataFrame(df[df['album_name'] == item], columns=['album_name', 'img_url']))
            
    res = list(np.array(new_df['img_url'].tolist()))
    return res
    
if __name__ == '__main__':
    # test1
    print("[teset 1]")
    temp=["Unplugged...And Seated (Deluxe Edition)",
        "THOMAS COOK"]
    tdict = random_album_img_urls(temp, 20)
    print(tdict)

    print()
    # test2
    print("[teset 2]")
    tl = ["피아노로 듣는 영화음악 지금 만나러 갑니다 `Cinema Piano`",
        "Unplugged...And Seated (Deluxe Edition)",
        "THOMAS COOK",
        "Best Of The Indigo 2000-2006",
        "Roped In",
        "Choral Adagios"]
    tlist2 = get_album_img_urls_to_list(tl)
    print(tlist2)