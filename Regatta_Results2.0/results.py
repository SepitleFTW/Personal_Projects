import  requests
from bs4 import BeautifulSoup
import json
"""
URL for the regatta results page
"""

URL = "https://www.regattaresults.co.za/home/2025-results/"

def results_scrape():
    response = requests.get(URL)
    soup = BeautifulSoup(respones.text, "html.parser")

    race_data = {}

    for link in soup.find.all("a", href=True):
        race_name  = link.text.strip()
        race_url = link["href"]
        if race_name:
            race_data[race_name] = race_url
    
    with open("race_results.json", "w") as f:
        json.dump(race_data, f, indent=4)

if __name__ == "__main __":
    results_scrape()

    