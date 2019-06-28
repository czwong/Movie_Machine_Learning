import mysql.connector
from config import info

# Connection settings
mydb = mysql.connector.connect(
    host=info["host"],
    user=info["username"],
    passwd=info["password"],
    database=info["database"]
)

drop_cursor = mydb.cursor()

# Drop table if it exists
drop_cursor.execute(f"drop table if exists {info['database']}.upcoming")

mycursor = mydb.cursor()

# Table schema
mycursor.execute \
(f"create table {info['database']}.upcoming \
  (movieID int NOT NULL AUTO_INCREMENT \
  ,name varchar(255) not null \
  ,image varchar(255) not null \
  ,release_date varchar(255) not null \
  ,genre varchar(255) not null \
  ,primary key (movieID))")


def load(record):

    movieInsert = "INSERT INTO upcoming (name, image, release_date, genre) VALUES ( %s, %s, %s, %s)"

    # Convert the values to a list
    values = [record['name'], record['image'], record['release_date'], record['genre']]
    # Insert values into the upcoming table
    mycursor.execute(movieInsert, values)

    print("Loaded " + record['name'])
    # Commit action
    mydb.commit()

    # print(f"Imported movie {record['name']}")

