# Roadmap
- [ ] Preprocess data
  - [x] For each row in Kaggle dataset, use IMDB link to scrape for cast names
  - [ ] For each cast name, search on Notable Name Database or use SexMachine and ethnicolr python modules to find race/ethnicity/gender info
    - [x] Check first entry in results page in NNDB page if it contains correct name and occupation matches actor/actress
    - [x] Use SexMachine and ethnicolr module
    * **NOTE**: How to run faster? Parallelize code using AWS?
  - [x] Expand original movie_metadata dataset with cast and crew variables with their race/ethnicity/gender info
  - [ ] Run on dataset and make sure it works as intended
- [x] Set up single-page UI template (React? Bootstrap?)
- [ ] Create visualizations from datasets generated from preprocessing step
  - [ ] Line chart for displaying trend in percentage of actor/actress leads being persons of color (POC)
  - [ ] 

# Notes
* [Kaggle dataset](https://www.kaggle.com/carolzhangdc/imdb-5000-movie-dataset) and cast database created from scraping located at `data` folder which is at the source folder. These are not tracked by git
* SexMachine module breaks when using python v3.x.x. See [this](https://github.com/ferhatelmas/sexmachine/issues/6) for porting details. Circumvented this problem by downloading manually and fixing as per Github issue.
* The HTML template downloaded from [here](https://startbootstrap.com/themes/sb-admin-2/) and modified to incorporate our d3 visualisations.
* A python server needs to be started in the html folder on the terminal. Commands are:
  For python 2: python -m SimpleHTTPServer 8000
  For python 3: Python3 -m http.server 8000
  These commands start a server on port 8000. To open the index page, open localhost:8000 on the browser.