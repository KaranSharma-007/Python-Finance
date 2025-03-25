from bs4 import BeautifulSoup
import pandas as pd
import requests

def Xml_Extract_Financials(df):
    """This function extract financials data from the xml file link

    Args:
        df (str): url link

    Returns:
        dataframe: dataframe of financials
    """
    url = df
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    # Parse the XML with BeautifulSoup
    soup = BeautifulSoup(response.content, "xml")

    # Extract all tags with numerical data
    data = []

    for tag in soup.find_all():
        if tag.namespace is not None:
            if tag.get("contextRef") == 'OneD' and tag.get("unitRef") == 'INR' :
                #print(tag)
                data.append({
                "FullTag": tag.name,
                "Value": tag.text.strip()
                })

    return pd.DataFrame(data)


def Extract_Important_Financials(df):
    """This functions extract only important financials from the xml file link

    Args:
        df (str): url link

    Returns:
        dataframe
    """
    Financials = Xml_Extract_Financials(df)
    
    # Defaults
    Total_Revenue= None 
    RevenueFromOperations = None
    ProfitBeforeTax = None
    FinanceCosts = None
    DepreciationDepletionAndAmortisationExpense = None
    Total_Expenses = None

    if len(Financials)> 6:
        Total_Revenue = float(Financials[Financials['FullTag'] == 'Income']['Value'].iloc[0])
        RevenueFromOperations = float(Financials[Financials['FullTag'] == 'RevenueFromOperations']['Value'].iloc[0])
        ProfitBeforeTax = float(Financials[Financials['FullTag'] == 'ProfitBeforeTax']['Value'].iloc[0])
        FinanceCosts = float(Financials[Financials['FullTag'] == 'FinanceCosts']['Value'].iloc[0])
        DepreciationDepletionAndAmortisationExpense = float(Financials[Financials['FullTag'] == 'DepreciationDepletionAndAmortisationExpense']['Value'].iloc[0])
        Total_Expenses = float(Financials[Financials['FullTag'] == 'Expenses']['Value'].iloc[0])


    data = {'Total_Revenue': [Total_Revenue], 
            'RevenueFromOperations': [RevenueFromOperations], 
            'ProfitBeforeTax': [ProfitBeforeTax],
            'FinanceCosts': [FinanceCosts],
            'DepreciationDepletionAndAmortisationExpense': [DepreciationDepletionAndAmortisationExpense],
            'Total_Expenses': [Total_Expenses]}
    
    return pd.DataFrame(data)