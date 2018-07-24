# -*- coding: utf-8 -*-
import requests
import datetime
from bs4 import BeautifulSoup
from crawlers.article_scraper import ArticleScraper
from newspaper import Article

def parse_expansion(crawl_date):
    print("\nInitializing Expansion spider ...\n")
    print("-"*80)

    NEWSPAPER = 'expansion'
    BASE_URL  = 'http://www.expansion.com/hemeroteca/'

    try:
        if isinstance(crawl_date, datetime.datetime): # check if argument is datetime.datetime
            dates = [crawl_date - datetime.timedelta(days=3), crawl_date - datetime.timedelta(days=2), crawl_date - datetime.timedelta(days=1), crawl_date]
            sections = ['apertura', 'media', 'cierre', 'noche']
            start_urls_list = []
            for date in dates:
                for section in sections:
                    start_urls_list.append(BASE_URL + date.strftime("%Y/%m/%d") + "/" + section + ".html")
    except TypeError:
        print("\nArgument type not valid.")
        pass

    for url in start_urls_list:
        result = requests.get(url)
        c = result.content
        soup = BeautifulSoup(c, "lxml")
        articles = soup.find_all("article")
        for article in articles:
            titles = article.find_all('h2')
            for title in titles:
                a = title.find_all('a')[0]
                url = a.get('href')
                new_article = ArticleScraper(url, NEWSPAPER)
