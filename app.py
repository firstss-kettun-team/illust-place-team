# coding: UTF-8
from flask import (
    Flask, render_template,
    redirect, url_for, request,
    session
)
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager, logout_user
import numpy as np

app = Flask(__name__)
auth = HTTPBasicAuth()

#ページ間でのdataの受け渡しがうまくいかないので、グローバル変数にする
data = {}
datas = []#複数形が違うのはご愛嬌
max_data = {}

#ログイン、DB機能は保留
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gacha.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
db.create_all()

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Text())

@auth.get_password
def get_pw(user_name):
    if user_name in users:
        return users.get(user_name)
    return None
"""

@app.route('/')
def index():
    #posts = Post.query.all()
    return render_template("index.html")

#ログイン
@app.route('/login', methods=['POST'])
def login():
    return redirect(url_for('dashboard'))

#ログアウト
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/select')
def select():
    global data
    global datas
    data = [] #一応初期化
    datas = [] #初期化
    rarities = ["N", "R", "SR", "UR"]
    weight = [0.8, 0.17, 0.025, 0.005]
    picked_rarity = np.random.choice(rarities, p=weight)

    #picked_rarityの中に入っている文字列と同じ名前の関数を呼び出す
    result_name = eval(picked_rarity)()

    #辞書型でデータを作成
    data = {'name':result_name, 'rarity':picked_rarity}
    datas.append(data)
    return redirect(url_for("result"))

#10連ガチャするいい方法が思いつかないのでページを分ける
@app.route('/select10')
def select10():
    global data
    global datas
    global max_data
    data = [] #一応初期化
    datas = [] #初期化
    max_data = {} #初期化
    mxr = 0
    for _ in range(10):
        rarities = ["N", "R", "SR", "UR"]
        weight = [0.8, 0.17, 0.025, 0.005]
        picked_rarity = np.random.choice(rarities, p=weight)
        #rarityを数値化
        if picked_rarity == "N":
            temp_rarity = 1
        elif picked_rarity == "R":
            temp_rarity = 2
        elif picked_rarity == "SR":
            temp_rarity = 3
        else:
            temp_rarity = 4

        #picked_rarityの中に入っている文字列と同じ名前の関数を呼び出す
        result_name = eval(picked_rarity)()

        ###picked_rarityの最も高いものを選ぶ
        if mxr < temp_rarity:
            mxr = temp_rarity
            max_rarity = picked_rarity
            max_name = result_name

        #辞書型でデータを作成
        data = {'name':result_name, 'rarity':picked_rarity, 'max_name':max_name, 'max_rarity':max_rarity}
        datas.append(data)

    max_data = {'max_name':max_name}
    return redirect(url_for("result"))

@app.route('/select_stillUR')
def select_stillUR():
    global data
    global datas
    global max_data
    data = [] #一応初期化
    datas = [] #初期化
    max_data = {} #初期化
    while True:
        rarities = ["N", "R", "SR", "UR"]
        weight = [0.8, 0.17, 0.025, 0.005]
        picked_rarity = np.random.choice(rarities, p=weight)

        #picked_rarityの中に入っている文字列と同じ名前の関数を呼び出す
        result_name = eval(picked_rarity)()

        #辞書型でデータを作成
        data = {'name':result_name, 'rarity':picked_rarity}
        datas.append(data)

        if picked_rarity == "UR":
            max_name = result_name
            break

    max_data = {'max_name':max_name}
    return redirect(url_for("result_stillUR"))

@app.route('/result')
def result():
    global datas
    global max_data
    return render_template("result.html", datas=datas, max_data=max_data)

@app.route('/result_stillUR')
def result_stillUR():
    global datas
    global max_data
    return render_template("stillUR.html", datas=datas, max_data=max_data)

def N():
    #いらすとや画像の名前を文字列で入れていく
    n = ["勝気な男の子", "内気な女の子"]
    return np.random.choice(n)

def R():
    #いらすとや画像の名前を文字列で入れていく
    r = ["エビフライ", "ミートパイ"]
    return np.random.choice(r)

def SR():
    #いらすとや画像の名前を文字列で入れていく
    sr = ["横浜マリンタワー", "武道館"]
    return np.random.choice(sr)

def UR():
    #いらすとや画像の名前を文字列で入れていく
    ur = ["ガリレオ", "ジャンヌダルク"]
    return np.random.choice(ur)

if __name__ == "__main__":
    app.run(debug=True, port=8888, threaded=True)