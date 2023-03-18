import pandas as pd

# read the CSV file into a DataFrame
#df = pd.read_csv('test.csv')
df = pd.read_csv('test.csv', header=0)
# df = df[["ctm", "open"]]


# print the first five rows of the DataFrame to check that it was read correctly
print(df.columns)