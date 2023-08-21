import mysql.connector
import datetime
import yfinance as yf

class AlpacaOrderRepository:
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
        CREATE TABLE IF NOT EXISTS alpaca_orders (
            OrderID INT AUTO_INCREMENT PRIMARY KEY,
            Ticker VARCHAR(20),
            Type VARCHAR(50),
            Category VARCHAR(50),
            Date DATE,
            Start TIME,
            End Time NULL,
            Duration Time NULL,
            Quantity INT,
            Price FLOAT,
            Pl FLOAT NULL,
            Plpc FLOAT NULL,
            Open TINYINT(1) 
        )
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(create_table_query)
        self.db_connection.commit()


    # def get_current_stock_price(self, ticker):
    #     try:
    #         # Fetch current stock price using yfinance
    #         stock_data = yf.download(ticker, period='1d', interval='1m')
    #         # price = price_series.iloc[0] if not price_series.empty else None
    #         current_price = stock_data.iloc[-1]['Close'] if not stock_data.empty else None
    #         return current_price
    #     except Exception as e:
    #         print(f"Error fetching stock price: {e}")
    #         return None

    def add_order(self, ticker, type, category, quantity, end = None, duration = None, pl = None, plpc = None, open = 1):
        # Split the comma-separated string of tickers into a list of tickers
        # tickers_list = tickers_str.split(',')

        # Get the current date and time
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.datetime.now().strftime('%H:%M:%S')

        # Loop through the list of tickers and insert each ticker into a separate row
        # for ticker in tickers_list:
        # Convert the ticker to a string
        # ticker_str = str(ticker.strip())  # Remove any leading/trailing spaces

        price = self.get_current_stock_price(ticker)

        # Insert the order into the orders table
        insert_query = """
        INSERT INTO alpaca_orders ( Ticker, Type, Category, Date, Start, End, Duration, Quantity, Price, Pl, Plpc, Open)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        with self.db_connection.cursor() as cursor:
            cursor.execute(insert_query, (ticker, type, category, current_date, current_time, end, duration, quantity, price, pl, plpc, open))
        self.db_connection.commit()

    def modify_order(self, ticker, date, end, duration, pl, plpc, open = 0):
        """
        Modify an existing order based on its ticker and date.
        
        Args:
        - ticker (str): The ticker of the order.
        - date (str): The date when the order was created.
        - pl (float): Profit/loss.
        - plpc (float): Profit/loss percentage.
        - open (int): 1 for open, 0 for closed.
        
        Returns:
        - bool: True if the order was modified successfully, False otherwise.
        """
        try:
            update_query = """
            UPDATE alpaca_orders
            SET End = %s, Duration = %s, Pl = %s, Plpc = %s, Open = %s
            WHERE Ticker = %s AND Date = %s
            """
            
            with self.db_connection.cursor() as cursor:
                cursor.execute(update_query, (end, duration, pl, plpc, open, ticker, date))
            
            self.db_connection.commit()
            return True
        
        except Exception as e:
            print(f"Error modifying order: {e}")
            return False


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



