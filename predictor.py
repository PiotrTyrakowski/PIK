import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Read the data
data = pd.read_csv('test.csv', header=0, sep=', ', engine='python' )

# Extract the open price and create a new DataFrame
open_price = data[["ctm", "open"]]

# Create a new column to shift the open prices 5 days into the future
open_price["open_shifted"] = open_price["open"].shift(-5*6)

# Drop the last 5 rows, which have NaN values in the "open_shifted" column
open_price = open_price[:-30]

# Prepare the data for training
X = open_price[["ctm"]]
y = open_price["open_shifted"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a linear regression model and train it on the training data
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Calculate the mean squared error
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# Predict the open price 5 days into the future
latest_ctm = X.iloc[-1, 0]
future_ctm = latest_ctm + (5 * 24 * 60 * 60 * 1000)  # Add 5 days in milliseconds
future_open_price = model.predict([[future_ctm]])

print("Predicted open price 5 days into the future:", future_open_price[0])
