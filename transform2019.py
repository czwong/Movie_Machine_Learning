import load2019
from extract2019 import read_movie


def transformed_record(record):
    # Return dictionary with information
    return {
            "name": record['name'],
            "image": record['image'],
            "release_date": record['release_date'],
            "genre": record['genre']
        }


def transform_data(data):
    # Loop through dicitonary records
    for d in data:
        transformed = transformed_record(d)
        # Load item into MySQL database
        load2019.load(transformed)

if __name__ == "__main__":
    transform_data(read_movie())