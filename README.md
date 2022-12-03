# Introduction
This project focus on creating crawlers to get beer raw data from different sources using Python and Scrapy.

## Data
Styles, Beers and Breweries are the data being collected. 

## Spiders
Spiders created to get data:
- [X] beeradvocate.com: `BeerAdvocateSpider`
- [ ] ratebeer.com

# Setup
Follow [these steps](https://docs.scrapy.org/en/latest/intro/install.html) to install Scrapy as it has some platform specific details to setup.

Create and activate `venv`:
```
python3 -m venv env 
source env/bin/activate
```

Install requirements:
```
pip install -r requirements.txt
```

# Getting the Data
To run it locally specify the `beeradvocate` crawler and the choose the [feed export](https://docs.scrapy.org/en/latest/topics/feed-exports.html#topics-feed-format-json):
```
scrapy crawl beeradvocate -O data.json
```
