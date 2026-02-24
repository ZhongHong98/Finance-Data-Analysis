# Finance-Data-Analysis
## 1️⃣ Project Overview
This project analyzes historical stock and ETF price data to evaluate performance, risk, and trading behavior. The analysis focuses on identifying top-performing stocks using annualized compound returns (CAGR), measuring volatility as a risk metric, and visualizing the risk-return tradeoff to support investment decision-making.

Key objectives:

- Identify top-performing stocks based on annualized returns

- Measure and compare stock volatility (risk)

- Visualize price trends and risk-return relationships

## 2️⃣ Tools Used

Python

- pandas (data manipulation)

- numpy (numerical computation)

- matplotlib (data visualization)

## 3️⃣ Dataset Description

The dataset contains historical daily stock price data with the following columns:

- fund_symbol	Stock
- price_date
- open
- high
- low
- close
- adj_close
- volume

Total records: ~3.8 million rows

📁 Dataset: [View Dataset](Dataset/Finance_Dataset.zip)

## 4️⃣ Data Validation (Python)

The following data validation steps were performed:

✅ Data Type Assignment

Converted fund_symbol to categorical type

Converted price_date to datetime

Ensured price columns were float and volume integer

✅ Missing Values Check

Checked null values in all columns

Removed rows with missing adjusted close prices

✅ Duplicate Check

Identified and removed duplicate rows

✅ Invalid Price Logic Check

Removed rows where price relationships were invalid:

high < open, close, low

low > open, close, high

✅ Missing Trading Days Check

Identified gaps in trading dates per stock to detect missing trading periods

## 5️⃣ Data Analysis (Python)
📈 Top 10 CAGR Stocks

Annual Compound Return (CAGR) was calculated to normalize performance across different listing periods.

⚠️ Top 10 Volatile Stocks

Annualized volatility was calculated using the standard deviation of daily returns.

## 6️⃣ Data Visualization (Python)

The following charts were created:

Top 10 CAGR Stocks Bar Chart
![Top 10 CAGR Stocks Bar Chart](Image/Top_10_CAGR_Stocks_Bar_Chart.png)

Top 3 CAGR Stocks Price Trend Line Chart
![Top 3 CAGR Stocks Price Trend Line Chart](Image/Top_3_CAGR_Stocks_Price_Trend_Line_Chart.png)

Top 10 Volatility Stocks Bar Chart
![Top 10 Volatility Stocks Bar Chart](Image/Top_10_Volatility_Stocks_Bar_Chart.png)

Risk vs Return Scatter Plot
![Risk vs Return Scatter Plot](Image/Risk_vs_Return_Scatter_Plot.png)

📁 Python file: [View Python File](Python/Finance_Python.py)

## 7️⃣ Key Business Insights
📌 1. Extremely High CAGR Stocks Are Mostly Short-Term or High-Risk Assets

AMER, TRYP, and SDEI recorded very high CAGR values (up to ~2900%). However, these stocks also have relatively short trading histories and extremely high volatility. This suggests that high returns are likely driven by speculative price surges rather than stable long-term growth.

Business implication: High CAGR does not always indicate a good long-term investment. Investors should consider risk and historical duration.

📌 2. Strong Positive Relationship Between Risk and Return

The risk vs return scatter plot shows that stocks with higher volatility generally achieved higher returns. AMER and TRYP appear in the top-right quadrant, indicating both high risk and high reward.

Business implication: Investors seeking high returns must accept higher risk. Low-risk stocks generally produce lower returns.

📌 3. Leveraged and Thematic ETFs Show Higher Growth and Risk

Stocks such as FNGU, URNM, WUGI, and KRBN are thematic or leveraged ETFs and showed strong CAGR performance. However, these instruments are known to amplify market movements, increasing both gains and losses.

Business implication: Leveraged ETFs can generate high returns but are unsuitable for conservative investors.

📌 4. High Volatility Does Not Always Guarantee High Returns

Some stocks (e.g., FRAK, NRGU, JDST, TVIXF) show high volatility but are not in the top return list. This indicates that volatility alone does not ensure positive performance.

Business implication: Risk without return is undesirable. Investors should evaluate risk-adjusted performance metrics such as Sharpe Ratio.

📌 5. Most Stocks Cluster at Low Risk and Low Return

The majority of stocks cluster in the lower-left region of the risk-return chart, indicating stable but modest returns.

Business implication: Most stocks provide steady but moderate performance, while extreme returns are rare and risky.
