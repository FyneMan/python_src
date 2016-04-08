#coding=utf-8

import tushare as ts
import datetime

df = ts.get_stock_basics()
df.to_csv('stock_information.csv')
for index, row in df.iterrows():
	time = str( df.ix[index]['timeToMarket'] )
	if len(time) > 1:
		year = time[0:4]
		month = time[4:6]
		date = time[6:8]
		#print index, year, month, date
		


#s002292_1 = ts.get_h_data('002292', autype='hfq', start='2009-09-10', end='2010-09-09')
#s002292_2 = ts.get_h_data('002292', autype='hfq', start='2010-09-10', end='2011-09-09')
#s002292_3 = s002292_2.append(s002292_1)
#s002292_3.to_csv('s002292_3.csv')
#s002292 = ts.get_h_data('002292', autype='hfq', start='2009-09-10', end='2011-09-09')
#s002292.to_csv('s002292.csv')

