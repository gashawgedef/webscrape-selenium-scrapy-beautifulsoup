# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import sqlite3
from itemadapter import ItemAdapter


class SpiderTutorialPipeline:
      def open_spider(self, spider):
        self.conn = sqlite3.connect('audible_books.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_title TEXT,
                book_author TEXT,
                narrated_by TEXT,
                series TEXT,
                book_length TEXT,
                released_date TEXT,
                language TEXT,
                ratings TEXT
            )
        ''')
        self.conn.commit()
        logging.info("Opened SQLite database and ensured books table exists")

      def close_spider(self, spider):
        self.conn.close()
        logging.info("Closed SQLite database connection")

      def process_item(self, item, spider):
        logging.info(f"Processing item: {item}")
        self.cursor.execute('''
            INSERT INTO books (book_title, book_author, narrated_by, series, book_length, released_date, language, ratings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get('book_title'),
            item.get('book_author'),
            item.get('narrated_by'),
            item.get('series'),
            item.get('book_length'),
            item.get('released_date'),
            item.get('language'),
            item.get('ratings')
        ))
        self.conn.commit()
        logging.info(f"Inserted item into database: {item}")
        return item