# Content-Based Movie Recommender

Our project is a content-based movie recommender program that recommends movies to users based on the movie’s genre similarity to other movies. It uses the Vector Space Model, which stores movies as a vector of their genres; the cosine between the angles of vectors is calculated to determine the similarity between genres of the movies. 

In addition to the movie recommender, we used a Random Forest Regressor model to predict the gross of movies based on a few movie variables such as IMDB rating, movie budget, and content rating.

### Files:
* `Resources/movie_metadata.csv`: IMDB movie dataset with 28 columns and 5000 rows.
* `Resources/ `: Notebook version of the movie recommender algorithm. 
* `db/newfinaldata.sqlite`: SQLite database with four tables:
    * `movie_data`: 
    * `images`:
    * `upcoming`:
    * `predictions`:

### Programs/Tools Used:
Python Flask
SQLite
Sklearn
Javascript
HTML
CSS
Plotly.js
D3.js
SQLAlchemy






