from dotenv import load_dotenv
import json
import os
import requests
import pandas as pd 
from datetime import datetime


load_dotenv()

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

while True:
	symbol=input('Enter name of stock you want: ')
	if not symbol.isalpha():
		print('please make sure to enter name of stock price')
	else:
		data=requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+symbol+'&apikey='+api_key)

		if 'Error' in data.text:
			print('The stock you are looking for is not here')
		else:
			break



j=data.json()

time,opening,high,low,close,volume=[],[],[],[],[],[]
for key, value in j['Time Series (Daily)'].items():
    time.append(key)
    opening.append(value['1. open'])
    high.append(value['2. high'])
    low.append(value['3. low'])
    close.append(value['4. close'])
    volume.append(value['5. volume'])

result = pd.DataFrame(
{'time':time,
'open':opening,
'high': high,
 'low': low,
 'close': close,
 'volume': volume})

result.to_csv('data/'+ symbol+'.csv')
print('`n')
print('#########################################')
print('The result has been saved successfully')
print('#########################################')

print('\n')
print('Most recent stock data time: '+ result.iloc[0]['time'])
print('DETAILS:')
print('Run at : ', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print('Stock: '+symbol)
print('The latest closing price: '+  "${0:,.2f}".format(float(result.iloc[0]['close'])))
print('The recent average high price: '+ "${0:,.2f}".format(max(result['high'].astype(float))))
print('The recent average low price: '+ "${0:,.2f}".format(min(result['high'].astype(float))))
if float(result.iloc[0]['close'])> result['close'][0:15].astype(float).mean():
	print ('We should buy this stock because its current closing price is higher than the closing average price over the last 15 days')
else:
	print ('We should NOT buy this stock because its current closing price is lower than the closing average price over the last 15 days')

print('#########################################')