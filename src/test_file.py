import pandas as pd
from datetime import datetime
import requests
import json

# file_path = r'C:\Users\baste\Desktop\EURUSD_tick_UTC+0_00_2010-Parse.csv'

# handler = pd.read_csv(file_path, sep=',')

# fecha = datetime.strptime(handler.UTC[0], '%Y-%m-%dT%H:%M:%S.%f%z')

# print(fecha)

response = requests.get('https://www.freeforexapi.com/api/live?pairs=EURUSD,GBPUSD,USDCAD').json()

for pair, info in response['rates'].items():
    print(pair, info['rate'])