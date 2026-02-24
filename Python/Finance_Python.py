import pandas as pd
import pandas_market_calendars as mcal
import matplotlib.pyplot as plt
import numpy as np

# Import data and assign data type
df = pd.read_csv(
    r"C:\Users\zhlim\OneDrive\Data Analytic\Finance Project\Finance Dataset.csv",
    dtype={
        "fund_symbol": "category",
        "open": "float32",
        "high": "float32",
        "low": "float32",
        "close": "float32",
        "adj_close": "float32",
        "volume": "int32"
    },
    parse_dates=["price_date"]   # ✅ convert during import
)

# Data overview
print("Overview")
print(df.head())
print()
print("Data type")
print(df.info())
print()
print("Total row: ",len(df))
print()

# Check null value
print("Null value")
print(df.isnull().sum())
print()

# Check duplicate value
duplicates = df.duplicated().sum()
print("Duplicates:", duplicates)
print()

# Check invalid price logic, high >= open, close, low OR low <= open, close, high
invalid_prices = df[(df["high"] < df[["open","close","low"]].max(axis=1)) |
                    (df["low"] > df[["open","close","high"]].min(axis=1))]

print("Invalid rows:", len(invalid_prices))
print()

# Remove invalid rows and check invalid rows after removed
df = df.drop(invalid_prices.index)
invalid_prices = df[(df["high"] < df[["open","close","low"]].max(axis=1)) |
                    (df["low"] > df[["open","close","high"]].min(axis=1))]
print("Invalid row after removed:", len(invalid_prices))
print()

# Check missing trading days
nyse = mcal.get_calendar('NYSE')
schedule = nyse.schedule(start_date=df["price_date"].min(),
                         end_date=df["price_date"].max())

valid_days = schedule.index

missing_days = set(valid_days) - set(df["price_date"].unique())
print("Missing trading days:", len(missing_days))
print()

# Sort data
df = df.sort_values(["fund_symbol", "price_date"])

# Calculate first and last price per stock
first_price = df.groupby("fund_symbol")["adj_close"].first()
last_price  = df.groupby("fund_symbol")["adj_close"].last()

# Fix zero price issue
first_price = first_price.replace(0, np.nan)

# Calculate years per stock
dates = df.groupby("fund_symbol")["price_date"].agg(["min", "max"])
dates["years"] = (dates["max"] - dates["min"]).dt.days / 365.25

# Merge price and years
price_data = pd.concat([first_price, last_price], axis=1)
price_data.columns = ["first_price", "last_price"]
price_data = price_data.join(dates["years"])

# Clear invalid rows
price_data = price_data[(price_data["first_price"] > 0) & (price_data["years"] > 0)]

# Calculate CAGR
price_data["cagr_pct"] = ((price_data["last_price"] / price_data["first_price"]) ** (1 / price_data["years"]) - 1) * 100
price_data = price_data.replace([np.inf, -np.inf], np.nan).dropna()

# Top 10 CAGR stock
top10_cagr = price_data.sort_values("cagr_pct", ascending=False).head(10).reset_index()
print("Top 10 CAGR stock")
print(top10_cagr)

# Top 10 CAGR stock bar chart
import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))
plt.barh(top10_cagr["fund_symbol"], top10_cagr["cagr_pct"])
plt.xlabel("Annual Compound Return (%)")
plt.title("Top 10 Stocks by CAGR")
plt.gca().invert_yaxis()
plt.show()

# Top 3 CAGR stock line chart
top3_symbols = top10_cagr["fund_symbol"].head(3).tolist()

plt.figure(figsize=(12,6))
for s in top3_symbols:
    temp = df[df["fund_symbol"] == s]
    plt.plot(temp["price_date"], temp["adj_close"], label=s)

plt.title("Top 3 CAGR Stocks Price Trend")
plt.xlabel("Date")
plt.ylabel("Adjusted Close Price")
plt.legend()
plt.show()

# Daily return & volatility
df["daily_return"] = df.groupby("fund_symbol")["adj_close"].pct_change()

volatility = df.groupby("fund_symbol")["daily_return"].std() * np.sqrt(252)
volatility = volatility.reset_index(name="volatility")

# Top 10 volatile stock table
top10_volatility = volatility.sort_values("volatility", ascending=False).head(10)
print("Top 10 volatility stock")
print(top10_volatility)

# Top 10 volatile stock bar chart
plt.figure(figsize=(12,6))
plt.barh(top10_volatility["fund_symbol"], top10_volatility["volatility"])
plt.xlabel("Volatility (Annualized Std Dev)")
plt.title("Top 10 Most Volatile Stocks")
plt.gca().invert_yaxis()
plt.show()

# Risk and return scatter plot
# Merge CAGR + Volatility
risk_return = price_data.reset_index().merge(volatility, on="fund_symbol")

plt.figure(figsize=(10,6))
plt.scatter(risk_return["volatility"], risk_return["cagr_pct"])

plt.xlabel("Volatility (Risk)")
plt.ylabel("CAGR (%)")
plt.title("Risk vs Return of Stocks")

# Label top 5 CAGR stocks
for _, row in top10_cagr.head(5).iterrows():
    v = risk_return[risk_return["fund_symbol"] == row["fund_symbol"]]["volatility"].values[0]
    plt.text(v, row["cagr_pct"], row["fund_symbol"])

plt.show()
