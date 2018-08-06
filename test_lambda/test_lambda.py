# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
from crawlers.cincodias import parse_cincodias
from crawlers.expansion import parse_expansion

print("Loading function")

def lambda_handler(event, context):
    """Lambda handler for the scraping / downloading process"""
    # Setting the crawl date
    if event["crawl_date"]:
        try:
            crawl_date = datetime.datetime.strptime(event["crawl_date"],"%Y%m%d")
            print("--> Crawling date %s" % event["crawl_date"])
        except:
            print("Wrong input crawl_date. Expecting a YYYYMMDD string, but got a:", event["crawl_date"])
    # Crawling newspaper
    if event["newspaper"]:
        if event["newspaper"] == "cincodias":
            print("--> Crawling cincodias")
            parse_cincodias(crawl_date)
        elif event["newspaper"] == "expansion":
            print("--> Crawling expansion")
            parse_expansion(crawl_date)
        else:
            print("Expecting the following newspapers: cincodias, expansion, eleconomista, elconfidenicial.")

if __name__ == "__main__":
    event = {
        "crawl_date": "20180720",
        "newspaper": "cincodias"

    }
    lambda_handler(event, {})
