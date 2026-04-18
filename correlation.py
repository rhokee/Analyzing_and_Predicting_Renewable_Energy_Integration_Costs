# Check to see if there is a correlation between retail and wholesale electricity prices

import pandas as pd

df = pd.read_csv('retail_wholesale_prices.csv')
corr_matrix = df.corr()
print(round(corr_matrix['Wholesale price'][0], 2)) # Retail and wholesale electricity prices are uncorrelated