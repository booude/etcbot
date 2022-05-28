import os
import aiohttp
import json

from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, LargeBinary
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
from quart import Quart, render_template, jsonify
from flask_login import UserMixin

load_dotenv(os.path.abspath('.env'))

with open(os.path.abspath('resources/lang.json'), encoding='utf8') as json_file:
    strings = json.load(json_file)

SCRAPED_URL = os.environ.get('SCRAPED_URL')
SPOTIFY_REFRESH_TOKEN = os.environ.get('SPOTIFY_REFRESH_TOKEN')
SPOTIFY_CLIENT_HASH = os.environ.get('SPOTIFY_CLIENT_HASH')
DATABASE_URL = os.environ.get('DATABASE_URL')
secret_key = os.environ.get('CLIENT_SECRET')
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(DATABASE_URL, future=True, echo=False)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

ENV = os.environ.get('ENV')

app = Quart(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SECRET_KEY'] = secret_key

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Broadcaster(Base):
    __tablename__ = 'broadcaster'
    id = Column(Integer, primary_key=True)
    twitch_id = Column(String(25), unique=True, nullable=False)
    created_at = Column(Date, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    prizes = relationship("Prize", backref="broadcaster")
    lists = relationship("List", backref="broadcaster")


class List(Base):
    __tablename__ = 'list'
    id = Column(Integer, primary_key=True)
    name = Column(String(25), unique=True, nullable=False)
    created_by = Column(String(25))
    is_active = Column(Boolean, default=True)
    broadcaster_id = Column(Integer, ForeignKey('broadcaster.id'))


class Prize(Base):
    __tablename__ = 'prize'
    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    prize = Column(String(255))
    date = Column(Date, default=datetime.utcnow)
    broadcaster_id = Column(Integer, ForeignKey('broadcaster.id'))
    checkAlert = Column(Boolean, default=False)


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, nullable=False)
    password = Column(LargeBinary, nullable=False)


@app.route("/elo/<id>/<lang>/<region>")
async def api_elo(id, lang, region):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://{region}.{SCRAPED_URL}/{id}') as response:
            html = await response.text()
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
async def currentsong():
    return await render_template("currentsong.html")


async def spotify():
    try:
        async with aiohttp.ClientSession() as session:
            session.headers['Authorization'] = f"Basic {SPOTIFY_CLIENT_HASH}"
            async with session.post(f"https://accounts.spotify.com/api/token", data={
                    "grant_type": "refresh_token", "refresh_token": F"{SPOTIFY_REFRESH_TOKEN}"}) as token:
                access_token = await token.json()
                access_token = access_token["access_token"]
            session.headers["Authorization"] = f"Bearer {access_token}"
            async with session.get("https://api.spotify.com/v1/me/player/currently-playing") as res:
                response = await res.json()
                trackName = response['item']['name']
                artists = response['item']['artists']
                artistName = ", ".join([artist['name'] for artist in artists])
                return {'track': trackName, 'artist': artistName}
    except:
        return {'track': 'Not playing', 'artist': 'Not playing'}


@app.route('/currentsong')
async def api_currentsong():
    json = await spotify()
    trackName = json['track']
    artistName = json['artist']
    return jsonify({'track': trackName, 'artist': artistName})


@app.route('/currentsong/command')
async def api_currentsongcommand():
    json = await spotify()
    trackName = json['track']
    artistName = json['artist']
    if trackName == 'Not playing' and artistName == 'Not playing':
        return 'Spotify não está tocando'
    else:
        return f'{trackName} - {artistName}'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
