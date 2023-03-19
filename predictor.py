import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Read the data
data = pd.read_csv('test.csv', header=0, sep=', ', engine='python' )

# Extract the open price and create a new DataFrame
open_price = data[["ctm", "open"]]
# take only ctm and open columns and last 1200 rows
open_price2 = open_price.iloc[-1200:, :]



# Create a new column to shift the open prices 1 hour into the future
open_price2["open_shifted"] = open_price2["open"].shift(-60)

# Drop the last 60 rows, which have NaN values in the "open_shifted" column
open_price2 = open_price2[:-60]

# Prepare the data for training
X = open_price2[["ctm"]]
y = open_price2["open_shifted"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a linear regression model and train it on the training data
model = LinearRegression()
model.fit(X_train, y_train)



open_price["open_shifted"] = open_price["open"].shift(-60)
open_price = open_price[:-60]

# Prepare the data for making predictions
X_hist = open_price[["ctm"]]
y_hist = open_price["open_shifted"]

# Make predictions on the historical data
y_pred_hist = model.predict(X_hist)


# Initialize variables for simulation
cash = 10000  # Initial investment
shares = 0
capital = cash

# Iterate through the historical data and simulate buying and selling
for i in range(len(y_pred_hist) - 60):  # Subtract 60 to avoid going beyond the data
    current_price = open_price.iloc[i, 1]
    future_price = y_pred_hist[i + 60]

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


