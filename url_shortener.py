from flask import Flask, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import string
import sqlite3

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

    # ensure uniqueness
    def generate_short(cursor):
        short = ''.join(choices(chars,k=4))
        exist = cursor.execute("select short_url from urls where short_url = {}".format(short), (short_url,)).fetchone()
        if exist:
            generate_short(cursor)
        else:
            return short

    url = str(request.json['url'])
    print("URL+++++++++++++++++++")
    print("URL IS: ", url)
    sqlconnection = sqlite3.connect("database.db")
    cursor = sqlconnection.cursor()
    chars = string.digits + string.ascii_letters
    # check if url exists already
    exist = cursor.execute("SELECT * from URLS where original_url={}".format(url))
    print("EXISTS: ",  exist)

    if exist:
        short = exist
    else:
        short = generate_short(cursor)
        cursor.execute("INSERT INTO urls(original_url,short_url) VALUES ('{}', '{}')".format(url, short))
        sqlconnection.commit()


    created_at = cursor.execute("SELECT created from urls where short_url={}".format(short)).fetchone()
    sqlconnection.close()

    shortened_url = request.host_url + short
    data = {
        'url': url,
        'shortened': shortened_url,
        'date created': created_at
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


@app.route('/stored_urls', methods=['GET'])
def list_all():
    urls = []
    urls.append({'url': 'ssdd'})
    return jsonify(urls)

