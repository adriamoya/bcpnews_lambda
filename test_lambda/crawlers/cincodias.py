# -*- coding: utf-8 -*-
import requests
import datetime
from bs4 import BeautifulSoup
from crawlers.article_scraper import ArticleScraper
from newspaper import Article

def parse_cincodias(crawl_date):
    print("\nInitializing Cincodias spider ...\n")
    print("-"*80)

    NEWSPAPER = 'cincodias'
    BASE_URL  = 'https://cincodias.elpais.com'

    try:
        if isinstance(crawl_date, datetime.datetime): # check if argument is datetime.datetime
            dates = [crawl_date - datetime.timedelta(days=3), crawl_date - datetime.timedelta(days=2), crawl_date - datetime.timedelta(days=1), crawl_date]
            start_urls_list = []
            for date in dates:
                for i in range(1,4):
                    start_urls_list.append( BASE_URL + '/tag/fecha/' + date.strftime("%Y%m%d") + "/" + str(i) )
    except TypeError:
        print("\nArgument type not valid.")
        pass

    for url in start_urls_list:
        result = requests.get(url)
        c = result.content
        soup = BeautifulSoup(c, "lxml")
        articles = soup.find_all('article', {"class": "articulo"})
        for article in articles:
            titles = article.find_all('h2', {"class": "articulo-titulo"})
            for title in titles:
                a = title.find_all('a')[0]
                url = BASE_URL + a.get('href')
                new_article = ArticleScraper(url, NEWSPAPER)
