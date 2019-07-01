import mysql.connector
from config import info

#Connection settings
mydb = mysql.connector.connect(
    host=info["host"],
    user=info["username"],
    passwd=info["password"],
    database=info["database"]
)

drop_cursor = mydb.cursor()

#Drop table if exists
drop_cursor.execute(f"drop table if exists {info['database']}.movie_data")
drop_cursor.execute(f"drop table if exists {info['database']}.new_data")

mycursor = mydb.cursor()

#Table Schema
mycursor.execute \
(f"create table {info['database']}.movie_data \
  (movieID int NOT NULL AUTO_INCREMENT \
  ,name varchar(80) not null\
  ,total_votes bigint \
  ,rating float \
  ,duration integer \
  ,gross_earnings bigint \
  ,genre varchar(200) \
  ,primary key (movieID))")

mycursor.execute \
(f"create table {info['database']}.new_data \
  (movieID int NOT NULL AUTO_INCREMENT \
  ,name varchar(80) not null\
  ,total_votes bigint \
  ,rating float \
  ,duration integer \
  ,gross_earnings bigint \
  ,genre varchar(200) \
  ,primary key (movieID))")

def load(record):

    movieInsert = "INSERT INTO movie_data (name, total_votes, rating, duration, gross_earnings, genre) VALUES ( %s, %s, %s, %s, %s, %s)"

    # Convert the values to a list
    values = [record['name'], record['total_votes'], record['rating'], record['duration'], record['gross_earnings'], record['genre']]
    mycursor.execute(movieInsert, values)

    print("Loaded " + record['name'])

    mydb.commit()

def reload_distinct():

  movieInsert = "INSERT INTO new_data (SELECT DISTINCT * FROM movie_data)"
  mycursor.execute(movieInsert)
  mydb.commit()

