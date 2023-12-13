#! /bin/sh
set -e

scrapy crawl sreality
python app.py