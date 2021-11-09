import pandas as pd
from flask import Flask, render_template, jsonify, request, redirect, url_for
import json

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
                    pick_user = data
                    print(request.form['data_button'])
                    return redirect(url_for('result'))
    df = pd.read_csv("GBvideos.csv",encoding="utf-8",usecols=cols)
    df_music = df.query("category_id=={}".format(genre))
    df_music = df_music.drop_duplicates(subset= 'title')
    df_music_list = list(map(str,(df_music['title'].tolist())))
    df_music_id = list(map(str,(df_music['video_id'].tolist())))
    # df_music_list = list(dict.fromkeys(df_music_list))
    return render_template('get_list.html', genre=genre,data=coords,pick_list=df_music_list,img_list=df_music_id,zip=zip)

@app.route('/result')
def result():
            return "Data is {}".format(pick_user)

if __name__ == '__main__':
    app.run(debug=True)