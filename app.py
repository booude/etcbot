import os
import requests
import json
import datetime

from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

load_dotenv(os.path.abspath('.env'))

with open(os.path.abspath('resources/lang.json'), encoding='utf8') as json_file:
    strings = json.load(json_file)

SCRAPED_URL = os.environ.get('SCRAPED_URL')
SPOTIFY_REFRESH_TOKEN = os.environ.get('SPOTIFY_REFRESH_TOKEN')
SPOTIFY_CLIENT_HASH = os.environ.get('SPOTIFY_CLIENT_HASH')
uri = os.environ.get('DATABASE_URL')
secret_key = os.environ.get('CLIENT_SECRET')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

ENV = os.environ.get('ENV')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SECRET_KEY'] = secret_key

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Broadcaster(db.Model):
    __tablename__ = 'broadcaster'
    id = db.Column(db.Integer, primary_key=True)
    twitch_id = db.Column(db.String(25), unique=True, nullable=False)
    created_at = db.Column(db.Date, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    prizes = db.relationship("Prize", backref="broadcaster")
    lists = db.relationship("List", backref="broadcaster")


class List(db.Model):
    __tablename__ = 'list'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    created_by = db.Column(db.String(25))
    is_active = db.Column(db.Boolean, default=True)
    broadcaster_id = db.Column(db.Integer, db.ForeignKey('broadcaster.id'))


class Prize(db.Model):
    __tablename__ = 'prize'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    prize = db.Column(db.String(255))
    date = db.Column(db.Date, default=datetime.utcnow)
    broadcaster_id = db.Column(db.Integer, db.ForeignKey('broadcaster.id'))
    checkAlert = db.Column(db.Boolean, default=False)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.LargeBinary, nullable=False)


@app.route("/elo/<id>/<lang>")
def api_elo(id, lang):
    html = requests.get(f'{SCRAPED_URL}{id}').content
    soup = BeautifulSoup(html, 'html.parser')
    nome = soup.find("div", id="playerName").string
    tag = soup.find("div", id="playerTag").string
    elo = soup.find(
        "span", class_="badge badge-overlay text-white").string.split()
    elo[0] = strings[lang][elo[0]]
    lp = strings[lang]['LP']
    elo = ' '.join(elo)
    try:
        rp = soup.find(
            "span", class_="badge badge-overlay text-gold").string.replace(' RP', '')
        return f'{nome}#{tag}: {elo} ({rp} {lp})'
    except:
        return f'{nome}#{tag}: {elo}'


@app.route("/currentsong/marquee", methods=["GET"])
def currentsong():
    return render_template("currentsong.html")


def spotify():
    try:
        token = requests.post("https://accounts.spotify.com/api/token", headers={"Authorization": f"Basic {SPOTIFY_CLIENT_HASH}"}, data={
            "grant_type": "refresh_token", "refresh_token": F"{SPOTIFY_REFRESH_TOKEN}"}).json()["access_token"]
        res = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers={
            "Authorization": f"Bearer {token}"
        })
        res = res.json()
        trackName = res['item']['name']
        artists = res['item']['artists']
        artistName = ", ".join([artist['name'] for artist in artists])
        return {'track': trackName, 'artist': artistName}
    except:
        return {'track': 'Not playing', 'artist': 'Not playing'}


@app.route('/currentsong')
def api_currentsong():
    json = spotify()
    trackName = json['track']
    artistName = json['artist']
    return jsonify({'track': trackName, 'artist': artistName})


@app.route('/currentsong/command')
def api_currentsongcommand():
    json = spotify()
    trackName = json['track']
    artistName = json['artist']
    if trackName == 'Not playing' and artistName == 'Not playing':
        return 'Spotify não está tocando'
    else:
        return f'{trackName} - {artistName}'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
