import numpy as np
import pandas_ta as ta

def add_financial_ratios(financials_data):
    """This function adds financial ratio features in the financial dataframe

    Args:
        financials_data (dataframe): finacial data containing col: ProfitBeforeTax, Total_Revenue, FinanceCosts, FinanceCosts, EBITDA, RevenueFromOperations, Total_Expenses

    Returns:
        dataframe: finacial dataframe with features added
    """
    financials_data['Operating_Margin'] = financials_data['ProfitBeforeTax'] / financials_data['Total_Revenue']
    financials_data['EBITDA'] = financials_data['ProfitBeforeTax'] + financials_data['FinanceCosts'] + financials_data['DepreciationDepletionAndAmortisationExpense']
    financials_data['EBITDA_Margin'] = financials_data['EBITDA'] / financials_data['Total_Revenue']
    financials_data['Profit_Margin'] = financials_data['ProfitBeforeTax'] / financials_data['Total_Revenue']
    financials_data['Revenue_Contribution'] = financials_data['RevenueFromOperations'] / financials_data['Total_Revenue']
    financials_data['Expense_Ratio'] = financials_data['Total_Expenses'] / financials_data['Total_Revenue']
    financials_data['Depreciation_Ratio'] = financials_data['DepreciationDepletionAndAmortisationExpense'] / financials_data['Total_Revenue']
    financials_data['FinanceCost_Ratio'] = financials_data['FinanceCosts'] / financials_data['Total_Revenue']
    return financials_data

def add_price_features(stock_data):
    """This function adds featurs to the stock price data

    Args:
        stock_data (dataframe): stock price dataframe

    Returns:
        dataframe: stock price dataframe with features added
    """
    stock_data = stock_data.sort_values('Date')
    stock_data['Daily_Return'] = stock_data['Close'].pct_change()
    stock_data['Intraday_Range'] = stock_data['High'] - stock_data['Low']
    stock_data['Close/Open'] = stock_data['Close'] / stock_data['Open']
    stock_data['High/Low'] = stock_data['High'] / stock_data['Low']
    stock_data['Direction'] = np.where(stock_data['Close'] > stock_data['Open'], 1, 0)

    stock_data['SMA_10'] = stock_data['Close'].rolling(10).mean()
    stock_data['SMA_30'] = stock_data['Close'].rolling(30).mean()

    stock_data['Volatility_10'] = stock_data['Daily_Return'].rolling(10).std()
    stock_data['Momentum_5D'] = stock_data['Close'] - stock_data['Close'].shift(5)

    stock_data['Volume_Avg_10'] = stock_data['Volume'].rolling(10).mean()

    stock_data['RSI'] = ta.rsi(stock_data['Close'], length=14)
    return stock_data
