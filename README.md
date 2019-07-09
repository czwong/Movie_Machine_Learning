# Content-Based Movie Recommender

Our project uses a content-based movie recommender algorithm that recommends movies to users based on the movie’s genre similarity. It uses the Vector Space Model, which stores movies as a vector of their genres; the cosine between the angles of vectors is calculated to determine the similarity between genres of the movies. 

In addition to the movie recommender, we used a Random Forest Regressor model to predict the gross of movies based on a few movie variables such as IMDB rating, movie budget, and content rating. The most important feature in predicting the gross was the number of users that voted.

### Files:
* `Resources/movie_metadata.csv`: IMDB movie dataset with 28 columns and 5000 rows.
* `Resources/ `: Notebook version of the movie recommender algorithm. 
* `db/newfinaldata.sqlite`: SQLite database with four tables:
    * `movie_data`: Dataset with movie title and its content features including rating, duration, genre, etc.
    * `images`: Title of movie and its poster image
    * `upcoming`: Upcoming 2019 movies and their poster image, content rating and release date
    * `predictions`: Actual gross and predicted gross
* `webscrape_2019_movies.ipynb`: Web scrapes upcoming movie information from https://www.imdb.com/list/ls029217360/
    * NOTE: The contents of the webscraped site were exported to `upcoming_movies_2019.csv`
    * `extract2019.py`, `transform2019.py`, `load2019.py`: Cleans the csv fie and exports it to a MySQL database
* `extractMovie.py`, `trasnformMovie.py`, `loadMovie.py`: Cleans the movie_metadata.csv and exports it to a MySQL database
* `extractImages.py`, `transformImages.py`, `loadImages.py`: Web scrapes the image of each movie in the movie_data.csv and exports it to a MySQL database
* `randomForestRegressor.py`: Random Forest Regressor model; outputs gross predictions and actual gross directly to the SQLite file
* 

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

### Webpages:
* `/`: Main movie recommender that suggests similar movies
* `/upcoming_movies`: Second movie recommender that suggests upcoming movies based on selection of past movies
* `/data_exploration`: Various graphs of the distribution of variables used in the Random Forest Regressor model and possible correlations
* `/gross_predictions`: Quantification of the Random Forest Regressor model

### How to run the app locally:
* NOTE: SQLite file is pre-loaded with all the data




