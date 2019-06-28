import loadMovie 
from extractMovie import read_movie

def clean_data(record):
    if 'gross_earnings' not in record.keys() or record['gross_earnings'] == None or 'duration' not in record.keys() or not record['duration']: 
        del record
    else:
        return record

def accommodateNull(record, columnString):
    if len(record[columnString]) == 0:
        print('Found a null: ' + columnString)
        return 0
    else:
        return int(record[columnString])

titles = set()



def transformed_record(record):
    # print('Heres the records name: ' + record['name'])
    if len(record['name']) > 80:
        record['name'] = record['name'][0:80]
    # if record['name'] not in titles:
    #     titles.add(record['name'])
    #     return {
    #         "name": record['name'],
    #         "total_votes": accommodateNull(record, 'total_votes'),
    #         "rating": float(record['rating']),
    #         "duration": int(record['duration']),
    #         "gross_earnings": accommodateNull(record, 'gross_earnings'),
    #         "genre": record['genre']
    #     }
    # else:
    #     print(record['name'] + " already in titles")
    #     return False
    return {
            "name": record['name'],
            "total_votes": accommodateNull(record, 'total_votes'),
            "rating": float(record['rating']),
            "duration": int(record['duration']),
            "gross_earnings": accommodateNull(record, 'gross_earnings'),
            "genre": record['genre']
        }


def transform_data(data):
    for d in data:
        cleaned_data = clean_data(d)
        if cleaned_data:
            transformed = transformed_record(cleaned_data)
            if transformed:
                loadMovie.load(transformed)


if __name__ == "__main__":
    transform_data(read_movie())