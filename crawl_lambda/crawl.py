# -*- coding: utf-8 -*-
from __future__ import print_function
import boto3
import datetime
from crawlers.cincodias import parse_cincodias
from crawlers.elconfidencial import parse_elconfidencial
from crawlers.eleconomista import parse_eleconomista
from crawlers.expansion import parse_expansion

print("Loading function")

def lambda_handler(event, context):
    """Lambda handler for the scraping / downloading process"""

    REGION = 'eu-central-1' # region to launch instance.
    INSTANCE_ID = 'i-02ad64e2ab12d8719'
    INSTANCE_TYPE = 't2.medium' # instance type to launch.
    BUCKET_NAME = 'bluecaparticles'

    ec2 = boto3.resource('ec2', REGION)
    instance = ec2.Instance(INSTANCE_ID)

    crawl_date = datetime.datetime.now()
    print("\n--> Crawling date %s" % crawl_date.strftime("%Y-%m-%d"))

    # try:
    try:
        trigger_file = event['Records'][0]['s3']['object']['key']
    except:
        trigger_file = ''

    if trigger_file:
        if 'cincodias' in trigger_file:
            print("\n--> Crawling Elconfidencial")
            parse_elconfidencial(crawl_date, BUCKET_NAME)
        elif 'elconfidencial' in trigger_file:
            print("\n--> Crawling Eleconomista")
            parse_eleconomista(crawl_date, BUCKET_NAME)
        elif 'eleconomista' in trigger_file:
            print("\n--> Crawling Expansion")
            parse_expansion(crawl_date, BUCKET_NAME)
        elif 'expansion' in trigger_file:
            print("\n--> Launching EC2...")
            response = instance.start()
    else:
        print("\n--> Crawling cincodias")
        parse_cincodias(crawl_date, BUCKET_NAME)


# if __name__ == '__main__':
#
#     # -------------
#     # TEST
#     # -------------
#
#     # Cincodias
#     event = { 'newspaper': 'cincodias' }
#     context = {}
#     lambda_handler(event, context)
#
#     # Elconfidencial
#     event = {
#         'Records': [
#             {
#                 's3': {
#                     'object': {
#                         'key': 'cincodias_urls.csv'
#                     }
#                 }
#             }
#         ]
#     }
#     context = {}
#     lambda_handler(event, context)
#
#     # Eleconomista
#     event = {
#         'Records': [
#             {
#                 's3': {
#                     'object': {
#                         'key': 'elconfidencial_urls.csv'
#                     }
#                 }
#             }
#         ]
#     }
#     context = {}
#     lambda_handler(event, context)
#
#     # Expansion
#     event = {
#         'Records': [
#             {
#                 's3': {
#                     'object': {
#                         'key': 'eleconomista.csv'
#                     }
#                 }
#             }
#         ]
#     }
#     context = {}
#     lambda_handler(event, context)
