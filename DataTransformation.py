import pandas as pd

def SalesCalulation(data):
    data['price'] = data['price'].str.replace('$','')
    data['sales'] = data['price'].astype(float)*data['quantity']
    data.sort_values(by='date')
    return data
