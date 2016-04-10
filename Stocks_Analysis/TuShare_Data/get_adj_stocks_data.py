#coding=utf-8

import tushare as ts
import datetime
import os

def get_adj_price_data(stocks_index, timeToMarket):
	'''
	stocks_index ::  a string of the stock number like '002292'
	timeToMarket ::  a string of the IPO date like '20120229'

	return :: a DataFrame containing the adj. price data
	'''
	year = int( timeToMarket[0:4] )
	month = int( timeToMarket[4:6] )
	date = int( timeToMarket[6:8] )
	d0 = datetime.datetime(year, month, date)
	d1 = d0 + datetime.timedelta(days = 730)    # getting data of 2 years each time
	today = datetime.datetime.today()
	if (today - d1).days > 0:
		final = ts.get_h_data(stocks_index, autype='hfq', start=d0.strftime('%Y-%m-%d'), end=d1.strftime('%Y-%m-%d'))
	else:
		final = ts.get_h_data(stocks_index, autype='hfq', start=d0.strftime('%Y-%m-%d'), end=today.strftime('%Y-%m-%d'))
		return final

	while (today - d1).days > 0:
		d0 = d1 + datetime.timedelta(days = 1)
		d1 = d0 + datetime.timedelta(days = 730)
		if (today - d1).days > 0:
			tmp = ts.get_h_data(stocks_index, autype='hfq', start=d0.strftime('%Y-%m-%d'), end=d1.strftime('%Y-%m-%d'))
			try:
				final = tmp.append(final)
			except:
				pass
		else:
			tmp = ts.get_h_data(stocks_index, autype='hfq', start=d0.strftime('%Y-%m-%d'), end=today.strftime('%Y-%m-%d'))
			try:
				final = tmp.append(final)
			except:
				pass
			return final


df = ts.get_stock_basics()
df.to_csv('stock_information.csv')

for index, row in df.iterrows():
	timeToMarket = str( df.ix[index]['timeToMarket'])
	if len(timeToMarket) > 1 and (not os.path.exists('./s' + str(index) + '.csv')):
		result = get_adj_price_data(str(index), timeToMarket)
		result.to_csv('s' + str(index) + '.csv')
	print index

#stock_index = '000001'
#timeToMarket = str( df.ix[stock_index]['timeToMarket'] )
#result = get_adj_price_data(stock_index, timeToMarket)
#result.to_csv('s' + stock_index + '.csv')

#for index, row in df.iterrows():
#	time = str( df.ix[index]['timeToMarket'] )
#	if len(time) > 1:
#		year = int( time[0:4] )
#		month = int( time[4:6] )
#		date = int( time[6:8] )
#		d0 = datetime.datetime(year, month, date)
#		d1 = datetime.datetime(year+1, month, date) + datetime.timedelta(days = -1)
#		if (datetime.datetime.today() - d1).days > 0:
#			tmp = ts.get_h_data(str(index), autype='hfq', start=d0.strftime('%Y-%m-%d'), end=d1.strftime('%Y-%m-%d'))
#			year += 1
#		else:
#			final = ts.get_h_data(str(index), autype='hfq', start=d0.strftime('%Y-%m-%d'))
#			final.to_csv('s' + str(index) +'.csv')
#
#		while (datetime.datetime.today() - d1).days > 0:
#			d0 = datetime.datetime(year, month, date)
#			d1 = datetime.datetime(year+1, month, date) + datetime.timedelta(days = -1)
#			if (datetime.datetime.today() - d1).days > 0:
#				final = ts.get_h_data(str(index), autype='hfq', start=d0.strftime('%Y-%m-%d'), end=d1.strftime('%Y-%m-%d'))
#				try:
#					tmp = final.append(tmp)
#				except:
#					pass
#				year += 1
#			else:
#				final = ts.get_h_data(str(index), autype='hfq', start=d0.strftime('%Y-%m-%d'))
#				try:
#					tmp = final.append(tmp)
#				except:
#					pass
#				tmp.to_csv('s' + str(index) + '.csv')
#
#s002292_1 = ts.get_h_data('002292', autype='hfq', start='2009-09-10', end='2010-09-09')
#s002292_2 = ts.get_h_data('002292', autype='hfq', start='2010-09-10', end='2011-09-09')
#s002292_3 = s002292_2.append(s002292_1)
#s002292_3.to_csv('s002292_3.csv')
#s002292 = ts.get_h_data('002292', autype='hfq', start='2009-09-10', end='2011-09-09')
#s002292.to_csv('s002292.csv')

