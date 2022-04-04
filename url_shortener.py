from flask import Flask, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import string

# setup configs
app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')


db = SQLAlchemy(app)

# class Url(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     original_url = db.Column(db.String(550))
#     shortened_url = db.Column(db.String(10), unique=True)
#     time_created = db.Column(db.DateTime, default=datetime.now)

@app.route("/")
def home_page():
    return "<p>Url shortener</p>"

# todo: fix this 
@app.route('/encode',methods=['POST'])
def encode_url():
    url = request.json['url']
    sqlconnection = sqlite3.connect("urls.db")
    chars = string.digits + string.ascii_letters
    short = ''.join(choices(chars,k=4))
    data = {
        'url': url,
        'shortened': 'blah blah',
        'date created': 'blah blah'
    }
    return jsonify(data)
# @app.route('decode', )
@app.route('/decode',methods=['POST'])
def decode_url():
    url = request.json['url']
    url = request.host_url + url
    data = {
        'url': url,
        'shortened': 'blah blah',
        'date created': 'blah blah'
    }
    return jsonify(data)
@app.route('/short/')
def open_url():


@app.route('/stored_urls', methods=['GET'])
def list_all():
    urls = []
    urls.append({'url': 'ssdd'})
    return jsonify(urls)

