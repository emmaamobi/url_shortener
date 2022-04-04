from flask import Flask, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import string
from datetime import datetime
from random import choices

# setup configs
app = Flask(__name__)


urls = {} # url: [original, short, created_at]
short_suffixes = set()
short_urls = {}
shortened_urls = {}

@app.route("/")
def home_page():
    return "<p>Url shortener</p>"

@app.route('/encode',methods=['POST'])
def encode_url():

    # ensure uniqueness
    def generate_short(suffixes):
        short = ''.join(choices(chars,k=4))
        if short in suffixes:
            generate_short(suffixes)
        else:
            return short 

    url = str(request.json['url'])
    chars = string.digits + string.ascii_letters
    # check if url exists already

    if url in urls:
        short = urls[url][1]
    else:
        short = generate_short(short_suffixes)
        short_suffixes.add(short)
        urls[url] = []
        urls[url].append(url)
        urls[url].append(short)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        urls[url].append(current_time)



    created_at = urls[url][2]

    shortened_url = request.host_url + "short?url=" + short
    shortened_urls[shortened_url] = url
    short_urls[short] = url
    print("SHORTTT")
    print(short_urls)
    data = {
        'url': url,
        'shortened': shortened_url,
        'date created': created_at
    }
    return jsonify(data)

@app.route('/decode',methods=['POST'])
def decode_url():
    url = str(request.json['url'])
    print("URL : ", url)
    if url not in shortened_urls:
        return jsonify({"error": "shortened url does not exist"})
    decoded = shortened_urls[url]
    print("short_urls: ", short_urls)
    time_stamp = urls[decoded][2]
    data = {
        'url': decoded,
        'shortened': url,
        'date created': time_stamp
    }
    return jsonify(data)

@app.route('/short/')
def open_url():
    short_url = request.args.get('url', default = 1, type = str)
    if short_url not in short_urls:
        return '',404
    redirect_url = short_urls[short_url]
    print("REDIRECT URL: ", redirect_url)
    return redirect(redirect_url)


@app.route('/stored', methods=['GET'])
def list_all():
    cur_urls = []
    for url in urls:
        original = urls[url][0]
        short = urls[url][1]
        short = request.host_url + "short?url=" + short
        time_ = urls[url][2]
        append_ = {
            'url': original,
            'shortened': short,
            'date created': time_
        }
        cur_urls.append(append_)

    return jsonify(cur_urls)

