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

from datetime import timedelta

app = Flask(__name__)


#################################################
# Database Setup
#################################################

# clean cache 
app.config['SEND_FILE_MAX_AG_DEFAULT'] = timedelta(seconds = 1)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/newfinaldata.sqlite"
db = SQLAlchemy(app)

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Movies = Base.classes.movie_data
Images = Base.classes.images
Upcoming = Base.classes.upcoming

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/dataexploration")
def dataexploration():
    """Return data exploration page."""
    return render_template("dataexploration.html")

@app.route("/upcoming")
def upcoming():
    """Return the upcoming movie page."""
    return render_template("upcoming.html")


@app.route("/movie_title")
def movies():
    # movies = db.session.query(Movies.name).order_by(Movies.name.asc()).distinct()
    movies = db.session.query(Movies.name).filter(Movies.name == Images.name).order_by(Movies.name.asc()).distinct()

    # Return a list of the column names (team names)
    return jsonify(list(movies))


@app.route("/movies/<movie>")
def find(movie):
    sel = [
        Movies.name,
        Movies.rating,
        Movies.duration,
        Movies.gross_earnings,
        Movies.genre,
        Movies.total_votes,
        Images.image
    ]

    # table = db.session.query(*sel).join(Movies, Movies.name == Images.name).\
    #     group_by(Movies.name).\
    #     filter(Movies.name == movie).all()

    table = db.session.query(*sel).join(Movies, Movies.name == Images.name).\
        filter(Movies.name == movie).all()

    movie_data = []
    for results in table:
        movie = {}
        movie["Title"] = results[0]
        movie["Rating"] = results[1]
        movie["Duration"] = results[2]
        movie["Gross_Earning"] = results[3]
        movie["Genre"] = results[4].replace("|", ", ")
        movie["Total_Votes"] = results[5]
        movie["Poster_Image"] = results[6]
        movie_data.append(movie)

    return jsonify(movie_data)


import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

cnx = sqlite3.connect('db/newfinaldata.sqlite')
df_movie = pd.read_sql_query("SELECT * FROM movie_data", cnx)
# df_movie = df_movie.drop_duplicates(subset="name")
df_img = pd.read_sql_query("SELECT * FROM images", cnx)
# df_img = df_img.drop_duplicates(subset="name")
df = pd.merge(df_movie, df_img, how="inner", on='name')

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
    newtitle = title
    idx = indices[newtitle]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[0:21]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]

def clean_movies(title):
    movies = genre_recommendations(title).head(19).tolist()
    counter = 0
    for movie in movies:
        if movie == title:
            movies.remove(movie)
            counter += 1

    if counter == 0:
        del movies[-1]
    
    return movies

@app.route("/movie_recommendation/<movie>")
def movie_recommender(movie):
    try:
        movie_recommendation = clean_movies(movie)

    except KeyError:
        movie_recommendation = []

    return jsonify(movie_recommendation)


#################################################
# upcoming movies set up
#################################################

@app.route("/upcoming_movies/<movie>")
def upcoming_movies(movie):
    # movies = db.session.query(Movies.name).order_by(Movies.name.asc()).distinct()
    # upcoming_movies = db.session.query(Upcoming.name).order_by(Upcoming.name.asc()).distinct()

    sel = [
        Upcoming.image
    ]

    table = db.session.query(*sel).filter(Upcoming.name == movie).all()

    movie_data_1 = []
    for results in table:
        movies = {}
        movies["Poster_Image"] = results[0]
        movie_data_1.append(movies)

    return jsonify(movie_data_1)



@app.route("/recommend_upcoming_movies/<movie>")
def recommend_upcoming_find(movie):
    sel = [
        Upcoming.name,
        Upcoming.release_date,
        Upcoming.genre,
        Upcoming.image
    ]

    # table = db.session.query(*sel).join(Movies, Movies.name == Images.name).\
    #     group_by(Movies.name).\
    #     filter(Movies.name == movie).all()

    table = db.session.query(*sel).filter(Upcoming.name == get_genre(movie)[0]).all()

    movie_data = []
    for results in table:
        movies = {}
        movies["Title"] = results[0]
        movies["Release_date"] = results[1]
        movies["Genre"] = results[2]
        movies["Poster_Image"] = results[3]
        movie_data.append(movies)

    return jsonify(movie_data)

#########################################################
# still need to do some change, i haven't checked details
#########################################################

# Function that get movie recommendations based on the cosine similarity score of movie genres
def recommend_upcoming(movie_name, genre):

    cnx = sqlite3.connect('db/newfinaldata.sqlite')
    df_upcoming = pd.read_sql_query("SELECT * FROM upcoming", cnx)
    
    # drop unnecessary column
    df_upcoming = df_upcoming[['name', 'genre']]
    
    # print(df_upcoming.head())

    # Break up the big genre string into a string array
    df_upcoming['genre'] = df_upcoming['genre'].str.split(',')
    
    # print(df_upcoming.head())

    dict1 = {
         "name": movie_name['Title'],
         "genre": genre
    }
    
    # print(dict1)
    
    ref_df = pd.DataFrame(dict1, index = [0])
    ref_df['genre'] = ref_df['genre'].str.split('|')
    # ref_df['genre'] = ref_df['genre'].fillna("").astype('str')
    # print(ref_df)
    
    
    df_upcoming = df_upcoming.append(ref_df, ignore_index=True)
    
    # print(df_upcoming.tail())

    # Convert genres to string value
    df_upcoming['genre'] = df_upcoming['genre'].fillna("").astype('str')
    # print(df_upcoming.tail())

    tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(df_upcoming['genre'])
    # print(tfidf_matrix)
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    # print(cosine_sim)
    

    # Build a 1-dimensional array with movie titles
    titles = df_upcoming['name']
    indices = pd.Series(df_upcoming.index, index=df_upcoming['name'])
    # print(indices)

    idx = indices[movie_name['Title']]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[0:3]
    movie_indices = [i[0] for i in sim_scores]

    recommendations =  titles.iloc[movie_indices]

    return recommendations

@app.route("/upcoming_movie_recommendation/<movie>")
def get_genre(movie):
    sel = [
        Movies.name,
        Movies.genre
    ]

    table = db.session.query(*sel).filter(Movies.name == movie).all()
    # print(table)

    movie_data = []
    for results in table:
        movie = {}
        movie["Title"] = results[0]
        movie["Genre"] = results[1]
        movie_data.append(movie)
    
    data = movie_data[0]
    
    # movie_data['Genre'] = movie_data['Genre'].split("|")
    # print(movie_data['Genre'])

    upcoming_movies = list(recommend_upcoming(movie, data["Genre"]))
    # print(type(upcoming_movies))
    
    counter = 0
    for item in upcoming_movies:
        if item == data["Title"]:
            upcoming_movies.remove(data["Title"])
            counter += 1

    if counter == 0:
        del upcoming_movies[-1]
        
    return upcoming_movies

if __name__ == '__main__':
    app.run(debug=True)