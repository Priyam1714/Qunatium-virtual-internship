import pandas as pd
from DataTransformation import SalesCalulation

dataframe = pd.read_csv('combined_data_full.csv')

print(SalesCalulation(dataframe))