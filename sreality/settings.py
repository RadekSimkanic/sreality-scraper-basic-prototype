# Scrapy settings for sreality project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from utils.config import load_db_configuration, load_sreality_configuration

BOT_NAME = "sreality"

SPIDER_MODULES = ["sreality.spiders"]
NEWSPIDER_MODULE = "sreality.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Load database configuration
DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT = load_db_configuration()

DATABASE = {
    'host': DB_HOST,
    'port': DB_PORT,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_NAME,
}

# Load sreality configuration
SREALITY_URL, SREALITY_NUMBER_OF_ITEMS = load_sreality_configuration()

ITEM_PIPELINES = {
    'sreality.pipelines.PostgresPipeline': 300,
}
