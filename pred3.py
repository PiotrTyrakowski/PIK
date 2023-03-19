import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor

# Read the data
data = pd.read_csv('test.csv', header=0, sep=', ', engine='python')

# Extract the open price and create a new DataFrame
open_price = data[["ctm", "open"]]
# take only ctm and open columns
open_price2 = open_price.iloc[:, :]

# Create a new column to shift the open prices 1 hour into the future
open_price2["open_shifted"] = open_price2["open"].shift(-60)

# Drop the last 60 rows, which have NaN values in the "open_shifted" column
open_price2 = open_price2[:-60]

# Split the data into the first 90 days and the second 90 days
first_90_days = open_price2.iloc[:90*24, :]
second_90_days = open_price2.iloc[90*24:180*24, :]

# Prepare the data for training
X_train = first_90_days[["ctm"]]
y_train = first_90_days["open_shifted"]

# Create a decision tree regressor and train it on the first 90 days of data
model = DecisionTreeRegressor()
model.fit(X_train, y_train)

# Make predictions on the second 90 days of data
second_90_days["open_shifted_pred"] = model.predict(second_90_days[["ctm"]])

# Initialize variables for simulation
cash = 10000  # Initial investment
shares = 0
capital = cash

# Iterate through the second 90 days of data and simulate buying and selling
for i in range(len(second_90_days) - 60):  # Subtract 60 to avoid going beyond the data
    current_price = second_90_days.iloc[i, 1]
    future_price = second_90_days.iloc[i, -1]

    # Buy shares if the predicted price is higher than the current price
    if future_price > current_price:
        buy_shares = cash // current_price
        shares += buy_shares
        cash -= buy_shares * current_price

    # Sell shares if the predicted price is lower than the current price
    elif future_price < current_price and shares > 0:
        cash += shares * current_price
        shares = 0

    # Update capital (cash + value of shares)
    capital = cash + shares * current_price

print("Final Capital:", capital)
