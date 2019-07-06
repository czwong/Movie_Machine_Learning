def clean_movies_two(movies, title):
    counter = 0
    for movie in movies:
        if movie == title:
            movies.remove(movie)
            counter += 1

    if counter == 0:
        del movies[-1]
    
    return movies


def recommend_upcoming(movie_name, genre):

    cnx = sqlite3.connect('db/newfinaldata.sqlite')
    df_upcoming = pd.read_sql_query("SELECT * FROM upcoming", cnx)

    # Break up the big genre string into a string array
    df_upcoming['genre'] = df_upcoming['genre'].str.split('|')

    dict1 = {
        "name": movie_name,
        "genre": genre
    }
    df_upcoming.append(dict1, ignore_index=True)

    # Convert genres to string value
    df_upcoming['genre'] = df_upcoming['genre'].fillna("").astype('str')

    tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(df_upcoming['genre'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Build a 1-dimensional array with movie titles
    titles = df_upcoming['name']
    indices = pd.Series(df_upcoming.index, index=df_upcoming['name'])

    newtitle = movie_name
    idx = indices[newtitle]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[0:3]
    movie_indices = [i[0] for i in sim_scores]

    recommendations =  titles.iloc[movie_indices]

    return recommendations


@app.route("/get_genre/<movie>")
def get_genre(movie):
    sel = [
        Movies.name,
        Movies.genre
    ]

    table = db.session.query(*sel).filter(Movies.name == movie).all()

    movie_data = []
    for results in table:
        movie = {}
        movie["Title"] = results[0]
        movie["Genre"] = results[4]
        movie_data.append(movie)

    upcoming_movies = recommend_upcoming(movie, movie_data[0]["Genre"])

    try:
        movie_recommendation = clean_movies_two(upcoming_movies, movie)
    except KeyError:
        movie_recommendation: []

    return movie_recommendation


@app.route("/upcoming/<movie>")
def find_upcoming(movie):
    sel = [
        Upcoming.name,
        Upcoming.image,
        Upcoming.release_data,
        Upcoming.genre
    ]

    table = db.session.query(*sel).filter(Upcoming.name == movie).all()

    movie_data = []
    for results in table:
        movie = {}
        movie["Title"] = results[0]
        movie["Poster_Image"] = results[1]
        movie["Release_Date"] = results[2]
        movie["Genre"] = results[3].replace("|", ", ")
        movie_data.append(movie)


    return jsonify(movie_data)