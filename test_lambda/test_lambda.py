# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
from crawlers.cincodias import parse_cincodias
from crawlers.expansion import parse_expansion
from crawlers.eleconomista import parse_eleconomista
from crawlers.elconfidencial import parse_elconfidencial

print("Loading function")

def lambda_handler(event, context):
    """Lambda handler for the scraping / downloading process"""
    # Setting the crawl date
    # if event["crawl_date"]:
    #     try:
    #         crawl_date = datetime.datetime.strptime(event["crawl_date"],"%Y%m%d")
    #         print("--> Crawling date %s" % event["crawl_date"])
    #     except:
    #         print("Wrong input crawl_date. Expecting a YYYYMMDD string, but got a:", event["crawl_date"])
    
    crawl_date = datetime.datetime.now()
    print("--> Crawling date %s" % crawl_date.strftime("%Y-%m-%d"))

    # Crawling newspaper
    if event["newspaper"]:
        if event["newspaper"] == "cincodias":
            print("--> Crawling cincodias")
            parse_cincodias(crawl_date)
        elif event["newspaper"] == "expansion":
            print("--> Crawling expansion")
            parse_expansion(crawl_date)
        elif event["newspaper"] == "eleconomista":
            print("--> Crawling eleconomista")
            parse_eleconomista(crawl_date)
        elif event["newspaper"] == "elconfidencial":
            print("--> Crawling elconfidencial")
            parse_elconfidencial(crawl_date)
        else:
            print("Expecting the following newspapers: cincodias, expansion, eleconomista, elconfidenicial.")

if __name__ == "__main__":
    event = {
        "crawl_date": "20180720",
        "newspaper": "elconfidencial"
    }
    lambda_handler(event, {})
