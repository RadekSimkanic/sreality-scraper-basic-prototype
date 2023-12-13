#!/bin/bash
set -e

python wait_for_db.py
scrapy crawl sreality
python app.py