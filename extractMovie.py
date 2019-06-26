import os
import csv

def read_movie():

    #Set path for file
    csvpath = os.path.join("Resources/movie_metadata.csv")

    #Open the CSV
    with open(csvpath, newline="") as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=",")

        header = next(csvreader)

        moviedata = []

        #Loop through each row
        for row in csvreader:
            data = {}

            data["name"] = row['movie_title']
            data["gross_earnings"] = row['gross']
            data["duration"] = row['duration']
            data["total_votes"] = row['num_voted_users']
            data["rating"] = row['imdb_score']
            data["genre"] = row['genres']

            #Append the dictionary to the list
            moviedata.append(data)
            
            print(moviedata)

if __name__ == "__main__":
    read_movie()

    
        

        

