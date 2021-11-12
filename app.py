import pandas as pd
from flask import Flask, render_template, jsonify, request, redirect, url_for
from sklearn.metrics.pairwise import cosine_similarity 
from sklearn.feature_extraction.text import CountVectorizer
import json

cv = CountVectorizer(max_features=5000,stop_words='english')
cols_data1 = ["video_id","title","category_id","trending_date",]
data1 = pd.read_csv("data1.csv",encoding="utf-8",usecols=cols_data1)

def listRecommend(id , listVideo) : 
    df = data1[data1['category_id'] == id ]
    df.reset_index(drop=True , inplace= True)
    listOfdata = []
    lst = []
    #สร้าง vector จาก DataFrame ที่มี Category id เดียวกัน 
    vector = cv.fit_transform(df['trending_date']).toarray()
    similarity = cosine_similarity(vector)
    for video in listVideo :
        #print(video)
        index = df[df['video_id'] == video].index[0]
        distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
        for i in distances[1:6]:
            if i[1] > 0.9 : 
                listOfdata.append(data1.iloc[i[0]].video_id)
    return listOfdata

def idToEverything(listvideo) : 
    lst = []
    data_set = pd.read_csv('GBvideos.csv',encoding='utf-8',usecols=['video_id','title','channel_title','comment_count','views','likes','dislikes','description'])
    for video in listvideo : 
       index = data_set[data_set['video_id'] == video].index[0] 
       lst.append(data_set.iloc[index])
    return lst

def videoidToTitle(list_vid) : 
    temp_list = []
    for video in list_vid : 
        index = data1[data1['video_id'] == video].index[0] 
        temp_list.append(data1.iloc[index].title)
    return temp_list

data_set = pd.read_csv('GBvideos.csv',encoding='utf-8',usecols=['video_id','views','likes','dislikes'])

def find_covariance(video) :
          
    data1 = data_set[data_set["video_id"] == video]
    data1['likes - dislikes'] = data1.likes - data1.dislikes
    buffer = data1.drop(columns=['video_id','likes','dislikes']) 
    co = buffer.cov() 
    print("co = " , co) 
    return(co['likes - dislikes'][0])

cols = ["video_id","title","category_id"] 
coords = {}
f = open ('GB_category_id.json', "r")
data = json.loads(f.read())

for i in data['items']:
    coords[i['id']] = i['snippet']['title']
# print(coords)
f.close()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', data=coords)

@app.route('/list_user/<genre>', methods=['GET','POST'])
def list_user(genre):
    if request.method == "POST":
        if request.form['data_button'] != 'None':
                    data = request.form['data_button']
                    global pick_user
                    global genre_id
                    pick_user = data
                    genre_id = genre
                    print(request.form['data_button'])
                    return redirect(url_for('result'))
    df = pd.read_csv("data1.csv",encoding="utf-8",usecols=cols)
    df_music = df.query("category_id=={}".format(genre))
    df_music = df_music.drop_duplicates(subset= 'title')
    df_music_list = list(map(str,(df_music['title'].tolist())))
    df_music_id = list(map(str,(df_music['video_id'].tolist())))
    # df_music_list = list(dict.fromkeys(df_music_list))
    return render_template('get_list.html', genre=genre,data=coords,pick_list=df_music_list,img_list=df_music_id,zip=zip)

@app.route('/result')
def result():
            temp_str = pick_user.split(",")
            print(temp_str)
            df = pd.read_csv("data1.csv",encoding="utf-8",usecols=cols)
            df_music = df.query("category_id=={}".format(genre_id))
            df_music = df_music.drop_duplicates(subset= 'title')
            df_music_list = list(map(str,(df_music['title'].tolist())))
            df_music_id = list(map(str,(df_music['video_id'].tolist())))
            show_list = listRecommend(int(genre_id), temp_str)
            title_list = videoidToTitle(show_list)
            print(show_list)
            print(title_list)
            return render_template('result.html', entry_data = show_list, genre=genre_id,data=coords,tile_vid=title_list,img_list=df_music_id,zip=zip)
            # return "Data is {}".format(listRecommend(int(genre_id), temp_str))

@app.route('/detail/<video_id>' , methods=['GET','POST'])
def detail(video_id):
            print("Check Vid ID", video_id)
            temp_list = []
            temp_list.append(video_id)
            data_item = idToEverything(temp_list)
            temp_condition = ""
            if find_covariance(video_id) > 0:
                temp_condition = 1
            else:
                temp_condition = -1
            return render_template('detail.html', item_id = data_item[0][0], title_vid = data_item[0][1], des = data_item[0][7], views = data_item[0][3], likes = data_item[0][4], dislikes = data_item[0][5], condition = temp_condition)

if __name__ == '__main__':
    app.run(debug=True)