import loadImages
from extractImages import scrape


def transformed_record(record):
    if len(record['name']) > 80:
        record['name'] = record['name'][0:80]
    
    return {
            "name": record['name'],
            "image": record['image']
        }


def transform_data(data):
    for d in data:
        transformed = transformed_record(d)
        loadImages.load(transformed)


if __name__ == "__main__":
    transform_data(scrape())

