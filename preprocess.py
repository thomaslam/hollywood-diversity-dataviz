import pandas as pd
import re
from sexmachine import detector
from ethnicolr import pred_census_ln
from urllib.request import urlopen
from bs4 import BeautifulSoup

df = pd.read_csv('./datasets/movie_metadata.csv')
nndb_base_link = "https://search.nndb.com/search/nndb.cgi?query="
gender_detector = detector.Detector()

gender_table = {"male": "Male", "female": "Female", "mostly_male": "Male", "mostly_female": "Female", "andy": "Androgynous"}
race_table = {"api": "Asian", "black": "Black", "hispanic": "Hispanic", "white": "White"}

def findActorInfo(tr):
    actor_name = tr.select('td')[1].get_text(strip=True)
    actor_query = re.sub(" ", "+", actor_name)
    search_page = urlopen(nndb_base_link + actor_query)
    search_soup = BeautifulSoup(search_page, "html.parser")

    first_entry = search_soup.select("font > p > table > tr")[1]
    entry_name = first_entry.select("td")[0]
    entry_link = entry_name.select("a")[0].get("href")
    entry_name_text = entry_name.text.strip()
    entry_occupation = first_entry.select("td")[1].text.strip()

    gender = "Male"
    race = "White"
    if entry_name_text == actor_name and entry_occupation == "Actor":
        # Scrape bio page
        bio_page = urlopen(entry_link)
        bio_soup = BeautifulSoup(bio_page, "html.parser")
        bio_main = bio_soup.find_all("td", {"bgcolor": "F0F0F0"})[0]
        bio_para = bio_main.select("td > p")[0].select("p > p")[0]
        gender = str(bio_para.select("b")[0].next_sibling).strip()
        race = str(bio_para.select("b")[1].next_sibling).strip()
    else:
        # If NNDB bio page not found then use SexMachine or ethnicolr module to guess gender/race
        gender_guessed = gender_detector.get_gender(actor_name)
        gender = gender_table[gender_guessed]

        last_name = " ".join(actor_name.split(" ")[1:])
        last_name_df = pd.DataFrame([{'name':last_name}])
        race_guessed = pred_census_ln(last_name_df,'name')["race"][0]
        race = race_table[race_guessed]

    return (gender, race)



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

    # For each actor search for entry on NNDB
    j = 0
    for tr in credits_soup.find_all("tr", {"class": "odd"}):
        if j == 1:
            break
        j += 1
        (gender, race) = findActorInfo(tr)
        

    # for tr in credits_soup.find_all("tr", {"class": "even"}):
        # findActorInfo(tr)


        
