# Roadmap
- [ ] Preprocess data
  - [x] For each row in Kaggle dataset, use IMDB link to scrape for cast names
  - [ ] For each cast name, search on Notable Name Database or use SexMachine python module to find race/ethnicity/gender info
  - [ ] Expand original movie_metadata dataset with cast and crew variables with their race/ethnicity/gender info
- [ ] Set up single-page UI template (React? Bootstrap?)
- [ ] Create visualizations from datasets generated from preprocessing step
  - [ ] Line chart for 

# Notes
* [Kaggle dataset](https://www.kaggle.com/carolzhangdc/imdb-5000-movie-dataset) and other datasets created from scraping are downloaded to `datasets` folder which is at the source folder. These are not tracked by git
