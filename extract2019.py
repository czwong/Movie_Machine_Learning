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
            # Initiate dictionary
            data = {}
            # Store movie name
            data["name"] = row['name']
            # Store image url 
            data["image"] = row['image']
            print(data["image"])
            # Store release data 
            data["release_date"] = row['release_date']
            # Store genre
            data["genre"] = row['genre']

            #Append the dictionary to the list
            moviedata.append(data)
            
        return moviedata

if __name__ == "__main__":
    read_movie()

    
        

        

