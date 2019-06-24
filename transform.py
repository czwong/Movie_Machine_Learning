import json
import os
import load
from extract import scrape_movies


def delete_empty_rows(record): 
    if record['gross'] == None: 
        del record
    else:
        return record

def transformed_record(record):
    return {
        "name": record["name"],
        "total_votes": record["votes"],
        "rating": record["rating"],
        "duration": record["duration"],
        "gross_earnings": record["gross"],
        "image": record["image"]
    }

def transform_data(data):
    for d in data:
        cleaned_record = delete_empty_rows(d)
        if cleaned_record:
            transformed = transformed_record(cleaned_record)
            load.load(transformed)


if __name__ == "__main__":
    transform_data(scrape_movies())

