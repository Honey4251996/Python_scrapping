#!/bin/bash

. /home/mike/forward-api-env/bin/activate
cd /home/mike/DTS-Mike/channel-gsmarena.com/gsmarena_scraper
PATH=$PATH:/usr/local/bin
export PATH
scrapy crawl gsmarena_spider