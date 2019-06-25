import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import or_

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/data.sqlite"
db = SQLAlchemy(app)

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Games = Base.classes.games
Pricing = Base.classes.pricing
Venues = Base.classes.venues

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/movie_title")
def movies():
    movies = db.session.query(Games.team1).distinct()

    # Return a list of the column names (team names)
    return jsonify(list(movies))

@app.route("/movies/<movie>")
def find(movie):
    sel = [
        Games.title,
        Venues.lat,
        Venues.lon,
        Pricing.low_price,
        Pricing.high_price
    ]

    table = db.session.query(*sel).\
        join(Venues, Games.venue_id == Venues.venue_id).\
        join(Pricing, Games.game_id == Pricing.game_id).\
        filter(or_(Games.team1 == team, Games.team2 == team)).\
        order_by(Games.utcdate).all()

    movie_list = []
    for results in table:
        events = {}
        events["Event"] = results[0]
        events["Latitude"] = results[1]
        events["Longitude"] = results[2]
        events["Low_price"] = results[3]
        events["High_price"] = results[4]
        movie_list.append(events)

    return jsonify(movie_list)



if __name__ == '__main__':
    app.run(debug=True)