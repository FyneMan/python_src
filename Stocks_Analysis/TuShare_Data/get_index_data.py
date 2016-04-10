#coding=utf-8

import tushare as ts
import datetime

df = ts.get_index()
df.to_csv('Index_data.csv')

#d0 = datetime.datetime.today()
#d1 = d0 + datetime.timedelta(days = -730)
#tmp = ts.get_h_data('000001', index=True, start=d1.strftime('%Y-%m-%d'), end=d0.strftime('%Y-%m-%d'))
#while True:
#	d0 = d1 + datetime.timedelta(days = -1)
#	d1 = d0 + datetime.timedelta(days = -730)
#	final = ts.get_h_data('000001', index=True, start=d1.strftime('%Y-%m-%d'), end=d0.strftime('%Y-%m-%d'))
#	try:
#		tmp = tmp.append(final)
#	except:
#		break
#tmp.to_csv('IN000001.csv')
for index, row in df.iterrows():
	print index, df.ix[index]['code'], df.ix[index]['name']

final = ts.get_h_data('000001', index=True, start='1991-01-01', end='2016-02-20')
final.to_csv('IN000001.csv')
