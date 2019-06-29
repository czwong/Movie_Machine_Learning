import loadMovie 
from extractMovie import read_movie



def transformed_record(record):
    return {
            "name": record['name'],
            "image": record['image'],
            "release_date":record['release_date'],
            "genre": record['genre']
        }

        


def transform_data(data):
    for d in data:
        transformed = transformed_record(d)
        loadMovie.load(transformed)

if __name__ == "__main__":
    transform_data(read_movie())