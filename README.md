# rea-scraper
Scrape for-sale property listings from realcommercial.com.au. \
The website provides 1000 pages of results, with 10 items per page. \
See `data/listings.json` for sample output.

## Usage:
1. Install requirements from poetry.lock
```poetry add --group dev poetry-lock-package```
2. Navigate to scrapy project folder **rea-scraper**
3. Run ```python -m scrapy crawl realcommercial -o data.json```

