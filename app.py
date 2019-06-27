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
        Movies.gross_earnings
        # Movies.image
    ]

    table = db.session.query(*sel).group_by(Movies.name).\
        filter(Movies.name == movie).all()

    movie_data = []
    for results in table:
        movie = {}
        movie["Title"] = results[0]
        movie["Rating"] = results[1]
        movie["Duration"] = results[2]
        movie["Gross_Earning"] = results[3]
        # movie["Poster_Image"] = results[4]
        movie_data.append(movie)

    return jsonify(movie_data)


import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

cnx = sqlite3.connect('db/movie_data.sqlite')
df = pd.read_sql_query("SELECT * FROM movies", cnx)
# Break up the big genre string into a string array
df['genre'] = df['genre'].str.split('|')
# Convert genres to string value
df['genre'] = df['genre'].fillna("").astype('str')

tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(df['genre'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Build a 1-dimensional array with movie titles
titles = df['name']
indices = pd.Series(df.index, index=df['name'])

# Function that get movie recommendations based on the cosine similarity score of movie genres
def genre_recommendations(title):
    newtitle = title + '\xa0'
    idx = indices[newtitle]
    print(idx)
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]
 

@app.route("/movie_recommendation/<movie>")
def movie_recommender(movie):
    movie_recommendation = genre_recommendations('Spectre').head(18).tolist()

    # movie_recommendation_list = []
    # for recommendation in movie_recommendation:
    #     movie_recommendation_list.append(recommendation.replace('\xa0', ''))

    return jsonify(movie_recommendation)



if __name__ == '__main__':
    app.run(debug=True)