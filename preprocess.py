import pandas as pd
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

df = pd.read_csv('./datasets/movie_metadata.csv')
nndb_base_link = "https://search.nndb.com/search/nndb.cgi?query="
i = 0
for idx, row in df.iterrows():
    if i == 1:
        break
    i += 1

    director_name = row["director_name"]

    # Parse movie_imdb_link column to get credit link
    imdb_link = row["movie_imdb_link"].split("?")[0]
    credits_link = imdb_link + "fullcredits"

    # Scrape credit page using BeautifulSoup module
    credits_page = urlopen(credits_link)
    credits_soup = BeautifulSoup(credits_page, "html.parser")

    j = 0
    for tr in credits_soup.find_all("tr", {"class": "odd"}):
        if j == 1:
            break
        j += 1

        # Find actor name and search for entry on NNDB
        actor = tr.select('td')[1].get_text(strip=True)
        actor = re.sub(" ", "+", actor)
        search_page = urlopen(nndb_base_link + actor)
        search_soup = BeautifulSoup(search_page, "html.parser")

        first_entry = search_soup.select("font > p > table > tr")[1]
        print(first_entry.prettify())
        

    # for tr in credits_soup.find_all("tr", {"class": "even"}):
        # actor = tr.select('td')[1].get_text(strip=True)


        
