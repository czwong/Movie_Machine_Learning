import json
import mysql.connector

def load(record):
    db_conn.session.add(db_conn.Violation(**record))
    db_conn.session.commit()

    return "hey"

