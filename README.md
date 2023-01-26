# rea-scraper
Scrape search results for property listings from <a href="https://realcommercial.com.au">realcommercial.com.au</a>. 

## How to Use
1. Install poetry:
```
pip install poetry
```
2. Go to project root, install requirements from poetry.lock, and start shell:
```
poetry add --group dev poetry-lock-package
poetry shell
```
4. Change dir to the scrapy project folder:
```
cd rea_scraper
```
5. Run spider:
```
python -m scrapy crawl realcommercial -o outfile.json
```
This will start a crawl for 2000 pages of search results for *for-sale* and *for-lease* property listings.

## Data Notes

- The realcommercial website limits results to 1000 pages per search query, with 10 properties listed per page. 
- Currently, this project is able to scrape results for *for-sale* & *for-lease* properties.
- An additional "CATEGORY" key is added each item to differentiate results from different search categories.


## Sample Data
See included sample output for <a href="https://raw.githubusercontent.com/temujin-lampasa/rea-scraper/main/sample_data/sample_data.json"> 20 pages of results</a>. \
Download this larger sample file for <a href='https://drive.google.com/file/d/121G4_4qkMbDrC4HUbSndfXqJD7htSjyL/view?usp=sharing'>2000 pages of results</a>.

