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

        # Create the orders table if it doesn't exist
        self.create_orders_table()

    def __del__(self):
        # Close the MySQL database connection when the object is deleted
        self.db_connection.close()

    def create_classification_table(self):
        # Create the orders table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS categories (
            OrderID INT AUTO_INCREMENT PRIMARY KEY,
            Article VARCHAR(255),
            Ticker VARCHAR(20),
            Category VARCHAR(50),
            BPCategory VARCHAR(50),
            Date DATE,
            Time TIME
        )
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(create_table_query)
        self.db_connection.commit()

    def add_classification(self, article, ticker, category, bp_category):
        # Get the current date and time
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.datetime.now().strftime('%H:%M:%S')

        # Insert the order into the orders table
        insert_query = """
        INSERT INTO orders (Article, Ticker, Category,BPCategory, Date, Time)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(insert_query, (article, ticker, category, bp_category, current_date, current_time))
        self.db_connection.commit()
