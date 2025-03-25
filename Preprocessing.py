import pandas as pd
import os
from datetime import datetime
import ast
import yfinance as yf

def preprocess_fillings_NonConsolidated_csv(path):
    """This function loads and cleans fillings list data file

    Args:
        path (str): file path

    Returns:
        dataframe: fillings list dataframe
    """
    # Load the file
    fillings_files_df = pd.read_csv(path)

    # Select only NonConsolidated reports
    fillings_files_df = fillings_files_df[fillings_files_df['CONSOLIDATED / NON-CONSOLIDATED'] == 'Non-Consolidated']

    # Fill na values
    # Since there is not much difference between Exchange Received Time and Exchange Dissemination Time, we can fill with the same value
    fillings_files_df['Exchange Dissemination Time'] = fillings_files_df['Exchange Dissemination Time'].fillna(fillings_files_df['Exchange Received Time'])

    # Drop unwanted columns, select ['COMPANY NAME', 'PERIOD ENDED','Exchange Dissemination Time','** XBRL'] 
    return fillings_files_df #['COMPANY NAME', 'PERIOD ENDED', 'Exchange Dissemination Time', '** XBRL']


def preprocess_stock_price_data(stock_name, market, path):
    """This function loads, update and cleans stock price data and saves it at the file path

    Args:
        stock_name (str): name of stock 
        market (str): market indicator
        path (str): file path

    Returns:
        dataframe: stock price dataframe
    """
    current_date = pd.Timestamp(datetime.now().date())

    # Check if the stock data file exists
    if os.path.isfile(path):
        # Load the existing CSV
        stock_data = pd.read_csv(path)
        
        # Convert 'Date' column to datetime format
        stock_data['Date'] = pd.to_datetime(stock_data['Date'])
        
        # Get the latest date from the CSV
        latest_date_in_csv = stock_data['Date'].max()
        start_date = (latest_date_in_csv + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Check if the latest date in the CSV is older than today's date
        if latest_date_in_csv < current_date:
            print(f"Updating data from {start_date} to {current_date}...")
            
            # Download missing data from Yahoo Finance
            new_data = yf.download(stock_name + market, start=start_date)
            
            # Reset the index and flatten columns
            new_data.reset_index(inplace=True)
            new_data.columns = new_data.columns.droplevel([1])
            
            # Append the new data to the existing DataFrame
            stock_data = pd.concat([stock_data, new_data], ignore_index=True)
            stock_data.drop_duplicates('Date',inplace=True)
            
            # Save the updated DataFrame to the CSV
            stock_data.to_csv(path, index=False)

            print(f"Data updated successfully and saved to {path}.")
        else:
            print("The CSV file is already up to date.")
    else:
        # If the file does not exist, download the complete data
        print(f"File '{path}' does not exist.")
        print("Downloading data from Yahoo Finance...")
        
        # Fetch the stock data
        stock_data = yf.download(stock_name + market)
        
        # Flatten MultiIndex columns
        stock_data.columns = stock_data.columns.droplevel([1])
        
        # Remove index by resetting it
        stock_data.reset_index(inplace=True)
        
        # Save the data to CSV
        stock_data.to_csv(path, index=False)
        
        print(f"Data downloaded successfully and saved to {path}.")

    return stock_data


# Fix the mixed data types in the 'Articles' column
def ensure_list(value):
        if isinstance(value, str):
            return ast.literal_eval(value)
        return value

def preprocess_sentiment_file(stock_name, market, path):
    """This function loads, update and cleans stock sentiment data and saves it at the file path

    Args:
        stock_name (str): name of stock 
        market (str): market indicator
        path (str): file path

    Returns:
        dataframe: stock sentiment dataframe
    """
    current_date = pd.Timestamp(datetime.now().date())

    # Check if the sentiment file exists
    if os.path.isfile(path):
        # Load the existing CSV
        sentiment_score = pd.read_csv(path)
        # Apply the function to the 'Articles' column
        sentiment_score['Articles'] = sentiment_score['Articles'].apply(ensure_list)
        # Convert 'Date' column to datetime format
        sentiment_score['Date'] = pd.to_datetime(sentiment_score['Date'])
        
        # Get the latest date from the CSV
        latest_date_in_csv = sentiment_score['Date'].max()
        
        # Check if the latest date in the CSV is older than today's date
        if latest_date_in_csv < current_date:
            print(f"Updating date from {latest_date_in_csv + pd.Timedelta(days=1)} to {current_date}...")
            
            # Generate a range of dates to append
            new_dates = pd.date_range(start=latest_date_in_csv + pd.Timedelta(days=1), end=current_date)
        
            # Create a DataFrame with these new dates
            new_dates_df = pd.DataFrame({'Date': new_dates})
        
            # Append the new dates to the original DataFrame
            sentiment_score = pd.concat([sentiment_score, new_dates_df], ignore_index=True)
            sentiment_score.drop_duplicates('Date',inplace=True)
            sentiment_score.to_csv(path, index=False)

            print("Dates updated successfully!")
        else:
            print("The CSV file is already up to date.")
    else:
        # If the file does not exist, create a template file
        print(f"File '{path}' does not exist.")
        
        start_date = (preprocess_stock_price_data(stock_name, market, path=f'{stock_name}.csv')['Date'].min()).strftime('%Y-%m-%d')
        # Generate a range of dates to append
        new_dates = pd.date_range(start=start_date, end=current_date.strftime('%Y-%m-%d'))

        # Create a DataFrame with these new dates
        sentiment_score = pd.DataFrame({'Date': new_dates,
                                        'Articles': None,
                                        'Aggregated Sentiment Score': None})
        sentiment_score.to_csv(path, index= False)
    
        print(f"Sentiment score template file created successfully and saved to {path}.")

    return sentiment_score
