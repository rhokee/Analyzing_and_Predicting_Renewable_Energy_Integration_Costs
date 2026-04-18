import pandas as pd

def clean_price_hub(x):
    if len(x) > 7 and x[0:7] == 'Indiana':
        return 'MISO'
    elif len(x) > 6 and x[0:6] in ['Nepool', 'NEPOOL']:
        return 'ISONE'
    elif x[0:2] in ['NP', 'SP']:
        return 'CAISO'
    elif x == 'ERCOT North 345KV Peak':
        return 'ERCOT'
    else:
        return 'PJM'

doc_names = ['ice_electric-historical/Indiana Hub.xls', 'ice_electric-historical/Mass Hub.xls', 'ice_electric-historical/NP 15 Hub.xls', 
             'ice_electric-historical/PJM West Hub.xls', 'ice_electric-historical/SP 15_1 Hub.xls', 'ice_electric-historical/SP 15_2 Hub.xls', 
             'ice_electric-2014final.xls', 'ice_electric-2015final.xls', 'ice_electric-2016final.xls', 'ice_electric-2017final.xlsx', 'ice_electric-2018final.xlsx', 
             'ice_electric-2019final.xlsx', 'ice_electric-2020final.xlsx', 'ice_electric-2021final.xlsx', 'ice_electric-2022final.xlsx', 'ice_electric-2023final.xlsx', 
             'ice_electric-2024final.xlsx', 'ice_electric-2025.xlsx']

docs = []

for i in range(0, len(doc_names)):

    # Read in each file
    doc = pd.read_excel(f'{doc_names[i]}')

    # Standardize column names
    if i < 6:
        doc = doc.rename(columns = {'Price Hub':'Price hub', 'Trade Date':'Trade date', 'Delivery Start Date':'Delivery start date', 
                                    'Delivery End Date':'Delivery \nend date', 'High Price $/MWh':'High price $/MWh', 'Low Price $/MWh':'Low price $/MWh', 
                                    'Wtd Avg Price $/MWh':'Wtd avg price $/MWh', 'Daily Volume MWh':'Daily volume MWh', 'Number of Trades':'Number of trades'})
    if i in [0, 2]:
        doc = doc.rename(columns = {'Number of Counterparties':'Number of counterparties'})
    if i in [1, 3, 4, 5]:
        doc = doc.rename(columns = {'Number of Companies':'Number of counterparties'})

    # Remove unnecessary data
    doc = doc.drop(columns = ['Trade date', 'Delivery start date', 'High price $/MWh', 'Low price $/MWh', 'Change', 'Daily volume MWh', 'Number of trades', 
                              'Number of counterparties'])
    doc = doc[doc['Price hub'] != 'Mid C Peak']
    doc = doc[doc['Price hub'] != 'Mid Columbia Peak']
    doc = doc[doc['Price hub'] != 'Palo Verde Peak']
    doc = doc[doc['Price hub'] != 'Palo Verde']

    # Extract useful information
    doc['Price hub'] = doc['Price hub'].apply(clean_price_hub)
    doc['Year'] = doc['Delivery \nend date'].dt.year
    doc['Month'] = doc['Delivery \nend date'].dt.month
    doc = doc.drop(columns = 'Delivery \nend date')
    doc['Wtd avg price $/MWh'] = round((((doc['Wtd avg price $/MWh'] // 1) * 60) + (doc['Wtd avg price $/MWh'] % 1)) / 1000, 2)
    doc = doc.rename(columns = {'Price hub':'Region', 'Wtd avg price $/MWh':'Wholesale price'})

    # Collect all clean files in a list so they can be combined at the end
    docs.append(doc)

# Combine all files and return combined file
final_doc = pd.concat(docs)
final_doc.to_csv('wholesale_prices.csv')