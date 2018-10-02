# -*- coding: utf-8 -*-
import csv
import boto3
import requests
import datetime
from bs4 import BeautifulSoup
# from newspaper import Article
# from crawlers.article_scraper import ArticleScraper

def parse_expansion(crawl_date, bucket_name):
    print("\nInitializing Expansion spider ...")
    print("-"*80)
    # connection to s3 bucket
    NEWSPAPER = 'expansion'
    BASE_URL  = 'http://www.expansion.com/hemeroteca/'

    if isinstance(crawl_date, datetime.datetime): # check if argument is datetime.datetime
        dates = [crawl_date - datetime.timedelta(days=3), crawl_date - datetime.timedelta(days=2), crawl_date - datetime.timedelta(days=1), crawl_date]
        sections = ['apertura', 'media', 'cierre', 'noche']
        start_urls_list = []
        for date in dates:
            for section in sections:
                start_urls_list.append(BASE_URL + date.strftime("%Y/%m/%d") + "/" + section + ".html")

    articles_obj = []
    for url in start_urls_list:
        result = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if result.status_code == 200:
            c = result.content
            soup = BeautifulSoup(c, "lxml")
            articles = soup.find_all("article")
            for article in articles:
                titles = article.find_all('h2')
                for title in titles:
                    a = title.find_all('a')[0]
                    url = a.get('href')
                    new_article_obj = {
                        'url': url,
                        'timestamp': crawl_date,
                        'newspaper': NEWSPAPER
                    }
                    print(url)
                    articles_obj.append(new_article_obj)

    keys = articles_obj[0].keys()
    with open('/tmp/expansion_articles.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(articles_obj)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    s3.Object(bucket_name, 'expansion_urls.csv').put(Body=open('/tmp/expansion_articles.csv', 'rb'))
