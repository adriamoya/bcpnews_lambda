
import json
import datetime

# from crawlers.main import crawl_newspapers  # process_all_newspapers
from crawlers.cincodias import parse_cincodias


def crawl(event, context):
    crawl_date = "20180720"
    fecha = datetime.datetime.strptime(crawl_date,"%Y%m%d")

    parse_cincodias(fecha)
    
    # Running date.
    # Crawling newspapers.
    # print('\nCrawling the news...')
    # print('-'*80)
    # crawl_newspapers(fecha)
    # print('Done.')
