import load 
from extractMovie import read_movie

def clean_data(record):
    if 'gross_earnings' not in record.keys() or record['gross_earnings'] == None or 'duration' not in record.keys() or record['duration']: 
        del record
    else:
        return record

def transformed_record(record):
    return{
        "name": record['name'],
        "total_votes": int(record['total_votes']),
        "rating": float(record['rating']),
        "duration": int(record['duration']),
        "gross_earnings": int(record['gross_earnings'].replace(',', '')),
        "genre": record['genre']
    }

def transform_data(data):
    for d in data:
        cleaned_data = clean_data(d)
        if cleaned_data:
            transformed = transformed_record(cleaned_data)
            load.load(transformed)


if __name__ == "__main__":
    transform_data(read_movie())