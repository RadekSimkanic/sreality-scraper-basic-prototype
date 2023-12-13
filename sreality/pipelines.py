# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2
from psycopg2 import sql
from utils.config import load_db_configuration


class PostgresPipeline(object):
    """Pipeline for storing scraped data into a PostgreSQL database."""

    def __init__(self):
        # Load important information from config or environment
        db_name, db_user, db_password, db_host, db_port = load_db_configuration()

        # PostgreSQL connection
        self.base_connection = psycopg2.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )

        # Create the database if they don't exist
        self.create_database_if_not_exists(db_name)

        # PostgreSQL connection
        self.connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        self.cursor = self.connection.cursor()

        # Create the table if they don't exist
        self.create_table_if_not_exists()

    @classmethod
    def from_crawler(cls, crawler):
        """Class method to create an instance of the pipeline using settings from settings.py."""
        return cls()

    def open_spider(self, spider):
        """Method called when the spider is opened."""
        pass

    def close_spider(self, spider):
        """Method called when the spider is closed, responsible for closing DB connections."""
        self.base_connection.close()
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        """Process each extracted item and insert it into the PostgreSQL database."""
        insert_query = """
            INSERT INTO flats (title, locality, price, images)
            VALUES (%s, %s, %s, %s);
        """
        values = (
            item['title'],
            ";".join(item['locality']),
            str(item['price']),
            ";".join(item['images']),
        )

        self.cursor.execute(insert_query, values)

        return item

    def create_database_if_not_exists(self, db_name):
        """Create the database if it doesn't exist."""
        cursor = self.base_connection.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()
        if not exists:
            self.base_connection.rollback()
            self.base_connection.autocommit = True
            self.base_connection.rollback()
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            self.base_connection.autocommit = False
        cursor.close()

    def create_table_if_not_exists(self):
        """Create the table if it doesn't exist."""
        self.cursor.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)", ('flats',))
        table_exists = self.cursor.fetchone()[0]
        if not table_exists:
            self.cursor.execute(f"""
                CREATE TABLE flats (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(512),
                    images VARCHAR(2048)
                );
            """)
        else:
            self.cursor.execute("SELECT setval('flats_id_seq', (SELECT MAX(id) FROM flats));")
