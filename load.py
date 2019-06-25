import mysql.connector
from config import info

mydb = mysql.connector.connect(
    host=info["host"],
    user=info["username"],
    passwd=info["password"],
    database=info["database"]
)

drop_cursor = mydb.cursor()

drop_cursor.execute(f"drop table if exists {info['database']}.movies")

mycursor = mydb.cursor()

mycursor.execute \
(f"create table {info['database']}.movies \
  (name varchar(60) not null\
  ,total_votes bigint \
  ,rating float \
  ,duration integer \
  ,gross_earnings bigint \
  ,image varchar(200) \
  ,primary key (name))")


def load(record):

    movieInsert = "INSERT INTO movies (name, total_votes, rating, duration, gross_earnings, image) VALUES ( %s, %s, %s, %s, %s, %s)"

    # Convert the values to a list
    values = [record['name'], record['total_votes'], record['rating'], record['duration'], record['gross_earnings'], record['image']]
    mycursor.execute(movieInsert, values)

    mydb.commit()

    print(f"Imported movie {record['name']}")

