#coding=utf-8

import numpy as np 
import pandas as pd 
import datetime

def holidays(start, end, festival_list):
	'''
	return the dates of holidays between start and end
	'''
	nn = (end - start).days
	date = start
	holidays = list()

	for ii in range(nn + 1):
		if (date.weekday() > 4) or (date.strftime('%Y-%m-%d') in festival_list):
			holidays.append(date)
		date += datetime.timedelta(days=1)

	return holidays


def withdraw_no_distribution(df, date_index, value_column, start, end, only_weekdays=False, festival_list=None):
	'''
	counting the number of withdrawing in each hour of a day

	return a DataFrame containing the number of withdrawing in each hour for each day between start and end, 
	as well as the sum_day and sum_hour information
	'''
	if only_weekdays == False:
		ndays = (end - start).days + 1
	else:
		if festival_list == None:
			print 'Error :: festival_list is not given in withdraw_time_distribution'
		else:
			close_days = holidays(start, end, festival_list)
			ndays = (end - start).days + 1 - len(close_days)
	
	result = np.zeros(25 * (ndays+1)).reshape((ndays+1), 25)

	date = start
	df_index = list()
	kk = 0
	for ii in range((end-start).days + 1):
		if (only_weekdays == False) or (date not in close_days):
			tmp = df[ df[date_index]==date ][ value_column ]
			index = tmp.index
			for jj in range(len(tmp)):
				result[kk][ tmp[index[jj]].hour ] += 1
			kk += 1
			df_index.append( date.strftime('%Y-%m-%d') )

		date += datetime.timedelta(days=1)

	df_index.append('sum_hour')
	df_columns = [str(ii)+'h-'+str(ii+1)+'h' for ii in range(24)]
	df_columns.append('sum_day')

	sum_hour = result.sum(0)
	result[-1][:] = sum_hour
	sum_day = result.sum(1)
	result[:, -1] = sum_day
	
	res_df = pd.DataFrame(result, index=df_index, columns=df_columns)
	return res_df


def time_interval_distribution(df, date_index, value_column, start, end, t1=0, t2=24, only_weekdays=False, festival_list=None):
	'''

	'''
	if only_weekdays:
		if festival_list == None:
			print 'Error :: festival_list is not given in time_interval_distribution'
		else:
			close_days = holidays(start, end, festival_list)

	date = start
	ndays = (end - start).days + 1
	interval_list = list()
	for ii in range(ndays+1):
		if (only_weekdays == False) or (date not in close_days):
			tmp = df[ df[date_index]==date ][ value_column ]
			tmp = tmp.sort_values(ascending=True, kind='mergesort')
			index = tmp.index
			for ii in range(len(tmp)-1):
				if (tmp[index[ii]].hour >= t1) and (tmp[index[ii+1]].hour < t2):
					interval_time = (tmp[index[ii+1]] - tmp[index[ii]]).seconds
					interval_list.append(interval_time)
		date += datetime.timedelta(days=1)

	return interval_list

def hist_counting(data_list, bins=11, normed=True):
	'''
	'''
	upper = max(data_list)
	lower = 0.0
	#lower = min(data_list)
	data_list = np.array(data_list)

	bounds = np.linspace(lower, upper, bins+1)
	res = np.zeros( 2 * bins ).reshape(bins, 2)
	gap = float(bounds[1] - bounds[0])
	for ii in range(bins):
		tmp1 = data_list[ data_list <= bounds[ii+1] ]
		if ii == 0:
			tmp2 = tmp1[ tmp1 >= bounds[ii] ]
		else:
			tmp2 = tmp1[ tmp1 > bounds[ii] ]

		if normed==True:
			res[ii, 1] = len(tmp2)/gap/len(data_list)
		else:
			res[ii, 1] = len(tmp2)

		if len(tmp2)==0:
			res[ii, 0] = bounds[ii+1]
		else:
			res[ii, 0] = tmp2.mean()

	return res

def hist_counting_int(data, normed=True):
	'''
	'''
	data_list = np.array(data)
	lower = data_list.min()
	upper = data_list.max()
	N = int(upper - lower) + 1
	res = np.zeros( 2*N ).reshape(N, 2)
	for ii in range(N):
		tmp1 = data_list[ data_list < (lower + ii + 0.5) ]
		tmp2 = tmp1[ tmp1 > (lower + ii - 0.5) ]
		if normed == True:
			res[ii, 1] = float(len(tmp2))/len(data_list)
		else:
			res[ii, 1] = len(tmp2)

		res[ii, 0] = lower + ii

	return res


def no_of_uids():
	'''
	'''


def withdraw_amount_distribution():
	'''
	'''

def remaining_amount_distribution():
	'''
	'''

if __name__ == '__main__':
	data_list = [1, 4, 6, 3, 7, 9, 10, 8, 5, 2, 0]
	result = hist_counting(data_list, 4)
	print result




