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

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/movie_data.sqlite"
db = SQLAlchemy(app)

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Movies = Base.classes.movies

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/movie_title")
def movies():
    movies = db.session.query(Movies.name).distinct()

    # Return a list of the column names (team names)
    return jsonify(list(movies))

@app.route("/movies/<movie>")
def find(movie):
    sel = [
        Movies.name,
        Movies.rating,
        Movies.duration,
        Movies.gross_earnings,
        Movies.image
    ]

    table = db.session.query(*sel).filter(Movies.name == movie).all()

    movie_list = []
    for results in table:
        movie = {}
        movie["Title"] = results[0]
        movie["Rating"] = results[1]
        movie["Duration"] = results[2]
        movie["Gross_Earning"] = results[3]
        movie["Poster_Image"] = results[4]
        movie_list.append(movie)

    return jsonify(movie_list)



if __name__ == '__main__':
    app.run(debug=True)