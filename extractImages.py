import csv
from bs4 import BeautifulSoup
import requests
from time import sleep

SLEEP_INTERVAL_SECS = 0.05

def scrape():
    csvpath = (r'''movie_metadata.csv''')

    #Open the CSV
    with open(csvpath, newline="") as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=",")
        #header = next(csvreader)
        
        moviedata = []

        #Loop through each row
        for row in csvreader:
            # initiate a dictionary
            data = {
                "name": "",
                "image": ""
            }
            try: 
                # store the movie name and remove unnecessary characters
                data["name"] = (row["movie_title"]).split('\xa0')[0]
                # Website link for image
                link = row['movie_imdb_link']
                # Store the response for the link
                response = requests.get(link)
                # Format response to a BeautifulSoup Object 
                soup = BeautifulSoup(response.text, 'html.parser')
                # Find the div the image is in
                poster = soup.find("div", class_="poster")
                #sleep(SLEEP_INTERVAL_SECS)
                #sleep(SLEEP_INTERVAL_SECS)
                # Obtain image link
                image = poster.find("img")["src"]
                # Store the image link in the dictionary
                data["image"] = image
                # Append dictionary to list
                moviedata.append(data)
                print(f"added {data['name']} image")

            # If there is an error, then append the current dictionary to a list    
            except (AttributeError):
                moviedata.append(data)
            except(TypeError):
                moviedata.append(data)

    return moviedata

if __name__ == "__main__":
    scrape()
