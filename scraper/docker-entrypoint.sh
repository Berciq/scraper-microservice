#!/bin/bash

SCRIPT_LOCATION=$(dirname $(readlink -f "$0"))
cd $SCRIPT_LOCATION

echo "Starting scraper"
scrapy crawl -L INFO content