import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

load_dotenv(os.path.abspath('.env'))

uri = os.environ.get('DATABASE_URL')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

ENV = os.environ.get('ENV')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = uri

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Prizes(db.Model):
    __tablename__ = 'prizes'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(25))
    prize = db.Column(db.Integer)
    date = db.Column(db.DateTime())

    def __init__(self, nickname, prize, date):
        self.nickname = nickname
        self.prize = prize
        self.date = date


headings = ("Nickname", "Prize", "Date")


@app.route("/", methods=["GET"])
def table():
    return render_template("table.html", headings=headings, data=Prizes.query.all())


if __name__ == "__main__":
    app.run()
