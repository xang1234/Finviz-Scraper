# Finviz-Scraper
Simple Scraper for [Finviz](https://finviz.com/) stock data.

The function `scrape_finviz` accepts a `list` of tickers and returns a pandas `dataframe`. All data from the financial highligths table (72 variables) are returned. A progressbar is displayed for tracking (requires the `progressbar` library)

<img src="/resource/scrape-finviz.JPG" alt="">

## Usage
The list of tickers may be in `uppercase` or `lower case`
```python
# data is a pandas DataFrame
data=scrape_finviz(['FB','INGN'])
```

## Data accuracy
The price data has a lag of 15-20 mins. Certain financial ratios might be affected by the price. It is recommended to scrape after market close or before market open. Further cleaning of the scraped data might be required (e.g. Market Cap, Income and Sales are returned with B or M for Billion or Million respectively).
