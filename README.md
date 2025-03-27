# Python Finance – Stock Price Prediction for Indian Market 🇮🇳

This project is focused on building a machine learning pipeline to predict stock prices and movements for Indian stocks using technical indicators, fundamental financials, and sentiment analysis.

---

![output](https://github.com/user-attachments/assets/66a4e9f9-6f90-418d-9a44-21a12d4db0b5)

---

<img width="1404" alt="Screenshot 2025-03-24 at 10 15 48" src="https://github.com/user-attachments/assets/3a398cd3-0775-4446-b0af-df6293a2ebfd" />


## 🚀 Project Highlights

- ✅ Predict stock prices using XGBoost Regresser
- ✅ Predict Buy/Sell signals using XGBoost Classifier (future scope)
- ✅ Feature engineering with:
  - Technical indicators (SMA, RSI, Momentum, etc.)
  - Fundamental ratios (EBITDA, Profit Margins, etc.)
  - Sentiment data (TextBlob + news sentiment)
- ✅ Visualizations for:
  - Prediction vs Actual
  - Buy/Sell signals on stock chart (future scope)
  - Error distributions
- ✅ Hyperparameter tuning with RandomizedSearchCV

---

## 📁 Project Structure

| File/Folder        | Description |
|--------------------|-------------|
| `main.ipynb`       | 🔁 Main notebook that executes the entire pipeline — from preprocessing to model training and evaluation. |
| `feature_engineer.py` | Feature engineering functions including technical indicators (SMA, RSI, etc.) and financial ratios. |
| `NseXRBL.py`       | Extracts financial statement data (like revenue, EBITDA) from NSE’s published XBRL/XML reports using `BeautifulSoup`. |
| `preprocessing.py` | Functions to load stock price data via Yahoo Finance, clean, and update existing CSV files. |
| `sentiments.py`    | Extracts news headlines using Google Search and computes sentiment scores using `TextBlob`. |
| `Data/`            | Contains local CSV and Excel files (stock price history, scraped financials, etc.). |
| `requirements.txt` | All required Python libraries for easy environment setup. |
| `README.md`        | This file — explains everything! |

---

## 🛠️ Tech Stack

- `Python 3.x`
- `pandas`, `numpy`
- `scikit-learn`, `xgboost`
- `matplotlib`, `seaborn`
- `pandas-ta` for technical indicators like RSI
- `TextBlob`, `BeautifulSoup`, `requests` for sentiment extraction
- `yfinance` for historical stock price data

---

## 📈 Target Variables

- **Regression:** Predict next-day closing price
- **Classification:** Predict Buy (1) or Sell (0) signal

---

## 📊 Sample Features

- `SMA_10`, `SMA_30`, `RSI`, `Momentum_5D`, `Volume_Change`
- `Aggregated Sentiment Score`
- `EBITDA_Margin`, `Profit_Margin`, `Expense_Ratio`
- `DaysAgoReportPublished`

---

## ⚙️ How to Run

1. **Clone this repo**
   ```bash
   git clone https://github.com/KaranSharma-007/Python-Finance
   cd Python-Finance
