import mysql.connector
from config import info

mydb = mysql.connector.connect(
    host=info["host"],
    user=info["username"],
    passwd=info["password"],
    database=info["database"]
)

drop_cursor = mydb.cursor()

drop_cursor.execute(f"drop table if exists {info['database']}.images")

mycursor = mydb.cursor()

mycursor.execute \
(f"create table {info['database']}.images \
  (movieID int NOT NULL AUTO_INCREMENT \
  ,name varchar(250) not null\
  ,image varchar(255) \
  ,primary key (movieID))")


def load(record):

    movieInsert = "INSERT INTO images (name, image) VALUES ( %s, %s)"

    # Convert the values to a list
    values = [record['name'], record['image']]
    mycursor.execute(movieInsert, values)

    mydb.commit()

    print(f"Imported movie {record['name']}")