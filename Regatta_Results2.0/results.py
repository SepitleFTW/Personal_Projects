import  requests
from bs4 import BeautifulSoup
import json
"""
URL for the regatta results page
"""

URL = "https://www.regattaresults.co.za/home/2025-results/"

def results_scrape():
    """
    Function to scrape the regatta results page and save the results to a json file
    """
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    race_data = {} #dict to store race names as keys and URLS as values

    for link in soup.find_all("a", href=True): #this loop finds all <a> with href attribute
        race_name  = link.text.strip() #extract text of the link and remove whitespace
        race_url = link["href"]
        if race_name: #storing race data into a dictionary
            race_data[race_name] = race_url
    
    with open("race_results.json", "w") as f:
        json.dump(race_data, f, indent=4)

if __name__ == "__main__":
    results_scrape()

    print("Results scraped successfully.")
    # This will print the scraped data to the console
    