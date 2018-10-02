# -*- coding: utf-8 -*-
import re
import csv
import boto3
import requests
import datetime
from bs4 import BeautifulSoup
# from newspaper import Article
# from crawlers.article_scraper import ArticleScraper

def parse_eleconomista(crawl_date, bucket_name):
    print("\nInitializing Eleconomista spider ...")
    print("-"*80)
    # connection to s3 bucket
    NEWSPAPER = "eleconomista"
    BASE_URL  = "http://www.eleconomista.es/"
    SECTIONS  = ['mercados-cotizaciones', 'economia', 'empresas-finanzas', 'tecnologia']

    if isinstance(crawl_date, datetime.datetime): # check if argument is datetime.datetime
        start_urls_list = []
        for section in SECTIONS:
            start_urls_list.append( BASE_URL + section + "/")
            print(BASE_URL + section + "/")

    articles_obj = []
    for url in start_urls_list:
        result = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if result.status_code == 200:
            c = result.content
            soup = BeautifulSoup(c, "lxml")
            cols = soup.find_all("div", {"class": re.compile("cols")})
            for col in cols:
                titles = col.find_all("h1", {"itemprop": "headline"})
                for title in titles:
                    a = title.find_all("a")[0]
                    if a:
                        url = a.get("href")
                        if 'http' not in url:
                            url = 'http:' + url
                        new_article_obj = {
                            'url': url,
                            'timestamp': crawl_date,
                            'newspaper': NEWSPAPER
                        }
                        print(url)
                        articles_obj.append(new_article_obj)

    keys = articles_obj[0].keys()
    with open('/tmp/eleconomista_articles.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(articles_obj)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    s3.Object(bucket_name, 'eleconomista_urls.csv').put(Body=open('/tmp/eleconomista_articles.csv', 'rb'))
