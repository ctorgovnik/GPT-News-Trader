import mysql.connector
import datetime
import yfinance as yf

class OrderRepositorySQL:
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

    def create_orders_table(self):
        # Create the orders table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS orders_test (
            OrderID INT AUTO_INCREMENT PRIMARY KEY,
            Article VARCHAR(255),
            Ticker VARCHAR(20),
            Category VARCHAR(50),
            Date DATE,
            Time TIME,
            Quantity INT,
            Price FLOAT
        )
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(create_table_query)
        self.db_connection.commit()

    def get_current_stock_price(self, ticker):
        try:
            # Fetch current stock price using yfinance
            stock_data = yf.download(ticker, period='1d', interval='1m')
            # price = price_series.iloc[0] if not price_series.empty else None
            current_price = stock_data.iloc[-1]['Close'] if not stock_data.empty else None
            return current_price
        except Exception as e:
            print(f"Error fetching stock price: {e}")
            return None

    def add_order(self, article, tickers_str, category, quantity):
        # Split the comma-separated string of tickers into a list of tickers
        tickers_list = tickers_str.split(',')

        # Get the current date and time
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.datetime.now().strftime('%H:%M:%S')

        # Loop through the list of tickers and insert each ticker into a separate row
        for ticker in tickers_list:
            # Convert the ticker to a string
            ticker_str = str(ticker.strip())  # Remove any leading/trailing spaces

            price = self.get_current_stock_price(ticker_str)

            # Insert the order into the orders table
            insert_query = """
            INSERT INTO orders_test (Article, Ticker, Category, Date, Time, Quantity, Price)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            with self.db_connection.cursor() as cursor:
                cursor.execute(insert_query, (article, ticker_str, category, current_date, current_time, quantity, price))
            self.db_connection.commit()

    def analyze_data(self):
        """
        Perform analysis on the stored orders data.
        Implement your analysis methods here.
        """
        # Example: Calculate statistics, generate insights, visualize data, etc.
        # analysis_results = ...

        # Return analysis_results if needed
        # return analysis_results

    # ... (other methods)



