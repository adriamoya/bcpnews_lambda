# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
from crawlers.cincodias import parse_cincodias
from crawlers.expansion import parse_expansion

print('Loading function')

def lambda_handler(event, context):
    crawl_date = "20180720"
    fecha = datetime.datetime.strptime(crawl_date,"%Y%m%d")

    parse_cincodias(fecha)
    parse_expansion(fecha)


if __name__ == '__main__':
    lambda_handler({}, {})
