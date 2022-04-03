import os

from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template
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


headings = ("Name", "Prize", "Date")


@app.route("/", methods=["GET"])
def table():
    return render_template("table.html", headings=headings, data=Prize.query.all())


if __name__ == "__main__":
    app.run()
