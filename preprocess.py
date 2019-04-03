import pandas as pd
import re, sqlite3
from sexmachine import detector
from ethnicolr import pred_census_ln
from urllib.request import urlopen
from bs4 import BeautifulSoup

df = pd.read_csv('./data/movie_metadata.csv')
nndb_base_link = "https://search.nndb.com/search/nndb.cgi?query="
gender_detector = detector.Detector()

gender_table = {
    "male": "Male", "mostly_male": "Male",
    "female": "Female", "mostly_female": "Female"
    }

race_table = {
    "api": "Asian", 
    "black": "Black", 
    "hispanic": "Hispanic", 
    "white": "White"
    }

gender_num_table = {"Male": "num_males", "Female": "num_females"}
race_num_table = {"White": "num_whites", "Black": "num_blacks", "Asian": "num_asians", "Hispanic": "num_hispanics"}

def scrapeActorInfo(actor_name, db_conn):
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
        if gender_guessed in gender_table.keys():
            gender = gender_table[gender_guessed]
        else:
            gender = "Others"

        last_name = " ".join(actor_name.split(" ")[1:])
        last_name_df = pd.DataFrame([{'name': last_name}])
        race_guessed = pred_census_ln(last_name_df, 'name')["race"][0]
        if race_guessed in race_table.keys():
            race = race_table[race_guessed]
        else:
            race = "Multiracial"

    # Insert entry into casts.db
    db_cursor = db_conn.cursor()

    db_cursor.execute("INSERT INTO casts VALUES (%s,%s,%s)" % (actor_name, gender, race))
    db_cursor.commit()
    db_cursor.close()
    return (gender, race)

def findActorInfo(actor_name, db_conn):
    gender = "Male"
    race = "White"

    db_cursor = db_conn.cursor()
    # Search in SQL database for actor/actress name and retrieve relevant gender/race info
    db_cursor.execute("SELECT * FROM casts WHERE name == '%s';" % actor_name)
    result = db_cursor.fetchone()
    if result != None:
        (gender, race) = (result[1], result[2])
    # If entry not found in SQL database, scrape NNDB or use Python modules to get gender/race
    # and then insert entry into database
    else:
        (gender, race) = scrapeActorInfo(actor_name, db_conn)
    
    db_cursor.commit()
    db_cursor.close()

    return (gender, race)

def updateDF(row, gender, race):
    gender_col_name = "num_males"
    if gender in gender_num_table.keys():
        gender_col_name = gender_num_table[gender]

    race_col_name = "num_whites"
    if race in race_num_table.keys():
        race_col_name = race_num_table[race]
    # pylint: disable=no-member
    df.loc[row, [gender_col_name, race_col_name]] += 1

def createCastsTable(db_file):
    sql_create_casts_table = """CREATE TABLE IF NOT EXISTS casts (
            name text NOT NULL PRIMARY KEY,
            gender text NOT NULL,
            race text NOT NULL
        );"""
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(sql_create_casts_table)
        cursor.commit()
        cursor.close()
        return conn
    except sqlite3.Error as e:
        print(e)
    
    return None

def main():
    db_file = "./data/casts.db"
    db_conn = createCastsTable(db_file)
    
    if (db_conn != None):
        print("Connected to SQL DB")

    # Create and initialize all column values
    # pylint: disable=no-member
    df = df.assign(num_whites=0, num_blacks=0, num_asians=0, num_hispanics=0, num_males=0, num_females=0)

    # pylint: disable=no-member
    for idx, row in df.iterrows():
        if idx == 1:
            break

        director_name = row["director_name"]

        # Parse movie_imdb_link column to get credit link
        imdb_link = row["movie_imdb_link"].split("?")[0]
        credits_link = imdb_link + "fullcredits"

        # Scrape credit page using BeautifulSoup module
        credits_page = urlopen(credits_link)
        credits_soup = BeautifulSoup(credits_page, "html.parser")

        # For each actor find gender/race info using findActorInfo function
        j = 0
        for tr in credits_soup.find_all("tr", {"class": "odd"}):
            if j == 1:
                break
            j += 1
            actor_name = tr.select('td')[1].get_text(strip=True)
            (gender, race) = findActorInfo(actor_name, db_conn)
            updateDF(idx, gender, race)
            
        j = 0
        for tr in credits_soup.find_all("tr", {"class": "even"}):
            if j == 1:
                break
            j += 1
            actor_name = tr.select('td')[1].get_text(strip=True)
            (gender, race) = findActorInfo(actor_name, db_conn)
            updateDF(idx, gender, race)


if __name__ == "__main__":
    main()
