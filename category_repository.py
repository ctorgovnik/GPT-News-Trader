import mysql.connector
import datetime

class CategoryRepository:
    def __init__(self, host, user, password, database):
        self.last_order_id = 0

        # Connect to MySQL database
        self.db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # Create the categories and article_links tables if they don't exist
        self.create_classification_table()
        self.create_article_links_table()

    def __del__(self):
        # Close the MySQL database connection when the object is deleted
        self.db_connection.close()

    def create_classification_table(self):
    # Create the categories table if it doesn't exist
      create_table_query = """
      CREATE TABLE IF NOT EXISTS categories (
          OrderID INT AUTO_INCREMENT PRIMARY KEY,
          Article VARCHAR(255),
          Ticker VARCHAR(50),
          Category VARCHAR(50),
          BPCategory VARCHAR(50),
          Date DATE,
          Time TIME,
          ArticleTime VARCHAR(50),
          ArticleLinkID INT,  -- Use OrderID as the foreign key
          FOREIGN KEY (ArticleLinkID) REFERENCES article_links(LinkID)
      )
      """
      with self.db_connection.cursor() as cursor:
          cursor.execute(create_table_query)
      self.db_connection.commit()


    def create_article_links_table(self):
        # Create the article_links table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS article_links (
            LinkID INT AUTO_INCREMENT PRIMARY KEY,
            ArticleLink VARCHAR(255)
        )
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(create_table_query)
        self.db_connection.commit()

    def add_classification(self, article, ticker, category, bp_category, article_time, article_link):
        # Get the current date and time
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.datetime.now().strftime('%H:%M:%S')

        # Insert the article link into the article_links table
        insert_link_query = """
        INSERT INTO article_links (ArticleLink)
        VALUES (%s)
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(insert_link_query, (article_link,))
        self.db_connection.commit()

        # Get the last inserted LinkID
        link_id = cursor.lastrowid

        # Insert the classification into the categories table, referencing the article link
        insert_query = """
        INSERT INTO categories (Article, Ticker, Category, BPCategory, Date, Time, ArticleTime, ArticleLinkID)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(insert_query, (article, ticker, category, bp_category, current_date, current_time, article_time, link_id))
        self.db_connection.commit()
