import loadImages
from extractImages import scrape


def transformed_record(record):
    # If the length is over 80, only grab the first 80 characters
    if len(record['name']) > 80:
        record['name'] = record['name'][0:80]
    
    # Return dicitonary with the name of the movie and iamge url
    return {
            "name": record['name'],
            "image": record['image']
        }


def transform_data(data):
    # Loop through every dictionary record
    for d in data:
        transformed = transformed_record(d)
        # Load record to a MySQL database
        loadImages.load(transformed)
    # Re-load distinct records
    loadImages.reload_distinct()


if __name__ == "__main__":
    transform_data(scrape())

