import loadMovie 
from extractMovie import read_movie

#Create function to remove rows with missing values for each column 
def clean_data(record):
    if 'gross_earnings' not in record.keys() or record['gross_earnings'] == None or 'duration' not in record.keys() or not record['duration']: 
        del record
    else:
        return record

#Look for empty values in columns 
def accommodateNull(record, columnString):
    if len(record[columnString]) == 0:
        print('Found a null: ' + columnString)
        return 0
    else:
        return int(record[columnString])

titles = set()


def transformed_record(record):
    #Return dictionary with data
    if len(record['name']) > 80:
        record['name'] = record['name'][0:80]

    return {
            "name": record['name'],
            "total_votes": accommodateNull(record, 'total_votes'),
            "rating": float(record['rating']),
            "duration": int(record['duration']),
            "gross_earnings": accommodateNull(record, 'gross_earnings'),
            "genre": record['genre']
        }


def transform_data(data):
    #Loop through each row in the dictioanry
    for d in data:
        cleaned_data = clean_data(d)
        if cleaned_data:
            transformed = transformed_record(cleaned_data)
            #Load into MySQL database
            if transformed:
                loadMovie.load(transformed)

    loadMovie.reload_distinct()

if __name__ == "__main__":
    transform_data(read_movie())