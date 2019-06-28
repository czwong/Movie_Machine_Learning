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
            data = {
                "name": "",
                "image": ""
            }
            try: 
                data["name"] = (row["movie_title"]).split('\xa0')[0]
                link = row['movie_imdb_link']
                response = requests.get(link)
                soup = BeautifulSoup(response.text, 'html.parser')
                poster = soup.find("div", class_="poster")
                #sleep(SLEEP_INTERVAL_SECS)
                #sleep(SLEEP_INTERVAL_SECS)
                image = poster.find("img")["src"]
                data["image"] = image
                moviedata.append(data)
                print(f"added {data['name']} image")
            except (AttributeError):
                moviedata.append(data)
            except(TypeError):
                moviedata.append(data)

    return moviedata

if __name__ == "__main__":
    scrape()
