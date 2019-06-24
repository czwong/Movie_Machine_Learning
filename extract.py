from bs4 import BeautifulSoup
import requests
import json

def scrape_movies():

    # Link to all 2019 movies
    url = "https://www.imdb.com/list/ls029217360/"

    # Get the url response
    response = requests.get(url)

    # Format url response with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Container for movie items
    items_list = soup.find('div', class_="lister-list")
    # Find all movie items
    movie_info = items_list.find_all('div', class_="lister-item mode-detail")

    info_list = []

    # Loop through each movie item
    for movie in movie_info:
        dict1 = {}
        
        try:
            # Find elements that contain info for votes and gross revenue
            items = movie.find_all("p", class_="text-muted text-small")
            # Loop through each of these items
            for item in items:
                # Find each specific element of information
                value = item.find_all("span", {"name": "nv"})
                # Loop through each one
                for i in range(len(value)):
                    # Assign the text value to a variable
                    value_text = value[i]["data-value"]
                    # If the text value's (nth + 1) position is even, assign it to the gross key
                    if ((i +1) % 2 == 0):
                        dict1["gross"] = value_text
                    # If the text value's (nth + 1) position is odd, assign it to the votes key
                    else:
                        dict1["votes"] = value_text
            
            # Find the rest of the movie information and store it in the dictionary
            dict1["rating"] = movie.find("span", class_="ipl-rating-star__rating").text
            dict1["duration"] = (movie.find("span", class_="runtime").text).split(" ")[0]
            dict1["name"] = movie.find("h3", class_="lister-item-header").find("a").text
            dict1["image"] = movie.find("img")["loadlate"]
            
            # Append the dictionary to the list
            info_list.append(dict1)
            
        except (AttributeError):
            pass
        except(TypeError):
            pass

    print("Finished scraping all data.")
    movies_json = json.dumps(info_list)

    return movies_json

if __name__ == "__main__":
    scrape_movies()
        