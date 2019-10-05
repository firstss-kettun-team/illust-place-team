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
data_10 = []

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
    rarities = ["N", "R", "SR", "UR"]
    weight = [0.8, 0.17, 0.029, 0.001]
    picked_rarity = np.random.choice(rarities, p=weight)

    #picked_rarityの中に入っている文字列と同じ名前の関数を呼び出す
    result_name = eval(picked_rarity)()

    #辞書型でデータを作成
    global data
    data = {'name':result_name, 'rarity':picked_rarity}
    return redirect(url_for("result"))

@app.route('/result')
def result():
    global data
    return render_template("result.html", data=data)

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