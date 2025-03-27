import numpy as np
import pandas_ta as ta

def add_financial_ratios(financials_data):
    """This function adds financial ratio features in the financial dataframe

    Args:
        financials_data (dataframe): finacial data containing col: ProfitBeforeTax, Total_Revenue, FinanceCosts, FinanceCosts, EBITDA, RevenueFromOperations, Total_Expenses

    Returns:
        dataframe: finacial dataframe with features added
    """
    financials_data['Operating_Margin'] = round(financials_data['ProfitBeforeTax'] / financials_data['Total_Revenue'], 2)
    financials_data['EBITDA'] = financials_data['ProfitBeforeTax'] + financials_data['FinanceCosts'] + financials_data['DepreciationDepletionAndAmortisationExpense']
    financials_data['EBITDA_Margin'] = round(financials_data['EBITDA'] / financials_data['Total_Revenue'], 2)
    financials_data['Profit_Margin'] = round(financials_data['ProfitBeforeTax'] / financials_data['Total_Revenue'], 2)
    financials_data['Revenue_Contribution'] = round(financials_data['RevenueFromOperations'] / financials_data['Total_Revenue'], 2)
    financials_data['Expense_Ratio'] = round(financials_data['Total_Expenses'] / financials_data['Total_Revenue'], 2)
    financials_data['Depreciation_Ratio'] = round(financials_data['DepreciationDepletionAndAmortisationExpense'] / financials_data['Total_Revenue'], 2)
    return financials_data

def add_price_features(stock_data):
    """This function adds featurs to the stock price data

    Args:
        stock_data (dataframe): stock price dataframe

    Returns:
        dataframe: stock price dataframe with features added
    """
    stock_data = stock_data.sort_values('Date')

    # Convert to int
    stock_data['Close'] = stock_data['Close']//1
    stock_data['High'] = stock_data['High']//1
    stock_data['Low'] = stock_data['Low']//1
    stock_data['Open'] = stock_data['Open']//1

    stock_data['Daily_Return'] = round(stock_data['Close'].pct_change()*100, 2)
    stock_data['Intraday_Range'] = stock_data['High'] - stock_data['Low']
    stock_data['Close/Open'] = round(stock_data['Close'] / stock_data['Open'], 2)
    stock_data['High/Low'] = round(stock_data['High'] / stock_data['Low'], 2)
    stock_data['Direction'] = np.where(stock_data['Close'] > stock_data['Open'], 1, 0)

    stock_data['SMA_10'] = round(stock_data['Close'].rolling(10).mean() ,2)
    stock_data['SMA_30'] = round(stock_data['Close'].rolling(30).mean(), 2)

    stock_data['Volatility_10'] = round(stock_data['Daily_Return'].rolling(10).std(), 2)
    stock_data['Momentum_5D'] = round(stock_data['Close'] - stock_data['Close'].shift(5), 2)

    stock_data['Volume_Avg_10'] = round(stock_data['Volume'].rolling(10).mean(), 2)

    stock_data['RSI'] = round(ta.rsi(stock_data['Close'], length=14), 2)

    return stock_data
