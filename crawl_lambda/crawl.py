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

    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(INSTANCE_ID)

    crawl_date = datetime.datetime.now()
    print("--> Crawling date %s" % crawl_date.strftime("%Y-%m-%d"))

    try:
        trigger_file = event['Records'][0]['s3']['object']['key']
        if trigger_file:
            # After the first crawling, an S3 event will trigger when the
            # the output object (csv file) is put into the corresponding
            # bucket. The process will repeat for each crawler automatically.
            if 'cincodias' in trigger_file:
                print("--> Crawling Elconfidencial")
                parse_elconfidencial(crawl_date)
            elif 'elconfidencial' in trigger_file:
                print("--> Crawling Eleconomista")
                parse_eleconomista(crawl_date)
            elif 'eleconomista' in trigger_file:
                print("--> Crawling Expansion")
                parse_expansion(crawl_date)
            elif 'expansion' in trigger_file:
                print("--> Launching EC2...")
                response = instance.start()
    except:
        # A cloudwatch event will trigger the first crawler
        print("--> Crawling cincodias")
        parse_cincodias(crawl_date)
