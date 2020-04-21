from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# client = MongoClient('mongodb://sampleID:samplePW@12.34.56.78', 27017)
client = MongoClient('mongodb://test:test@15.164.226.122', 27017)
db = client.dbsparta


# HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분
@app.route('/post', methods=['POST'])
def post():
    url_receive = request.form['url_give']  # 클라이언트로부터 url을 받는 부분
    category1_receive = request.form['category1_give']
    category2_receive = request.form['category2_give']
    nickname_receive = request.form['nickname_give']
    comment_receive = request.form['comment_give']  # 클라이언트로부터 comment를 받는 부분

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    url_image = og_image['content']
    url_title = og_title['content']
    url_description = og_description['content']

    article = {'url': url_receive, 'category1': category1_receive, 'category2': category2_receive,
               'nickname': nickname_receive, 'comment': comment_receive,
               'image': url_image, 'title': url_title, 'desc': url_description}

    db.articles.insert_one(article)

    return jsonify({'result': 'success'})


@app.route('/post', methods=['GET'])
def view():
    posts = db.articles.find({}, {'_id': 0})
    return jsonify({'result': 'success', 'articles': list(posts)})


if __name__ == '__main__':
    app.run('127.0.0.1', port=5000, debug=True)
