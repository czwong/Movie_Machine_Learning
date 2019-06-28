import csv

def read_movie():

    #Set path for file
    # csvpath = os.path.join("Resources/movie_metadata.csv")
    csvpath = ("upcoming_movies_2019.csv")

    #Open the CSV
    with open(csvpath, newline="") as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=",")

        # header = next(csvreader)

        moviedata = []

        #Loop through each row
        for row in csvreader:
            data = {}

            data["name"] = row['name']
            data["image"] = row['image']
            print(data["image"])
            data["release_date"] = row['release_date']
            data["genre"] = row['genre']

            #Append the dictionary to the list
            moviedata.append(data)
            
        return moviedata

if __name__ == "__main__":
    read_movie()

    
        

        

