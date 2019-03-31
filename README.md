# Roadmap
- [ ] Preprocess data
  - [x] For each row in Kaggle dataset, use IMDB link to scrape for cast names
  - [ ] For each cast name, search on Notable Name Database or use SexMachine and ethnicolr python modules to find race/ethnicity/gender info
    * Check first entry in results page in NNDB page if it contains correct name and occupation matches actor/actress
    * Parallelize code using AWS?
  - [ ] Expand original movie_metadata dataset with cast and crew variables with their race/ethnicity/gender info
- [ ] Set up single-page UI template (React? Bootstrap?)
- [ ] Create visualizations from datasets generated from preprocessing step
  - [ ] Line chart for displaying trend in percentage of actor/actress leads being persons of color (POC)
  - [ ] 

# Notes
* [Kaggle dataset](https://www.kaggle.com/carolzhangdc/imdb-5000-movie-dataset) and other datasets created from scraping are downloaded to `datasets` folder which is at the source folder. These are not tracked by git
* SexMachine module breaks when using python v3.x.x. See [this](https://github.com/ferhatelmas/sexmachine/issues/6) for porting details. Circumvented this problem by downloading manually and fixing as per Github issue.
