#coding=utf-8

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import datetime
from scipy.optimize import curve_fit
from scipy.stats import poisson

from Withdraw_Data_Anal import withdraw_no_distribution
from Withdraw_Data_Anal import time_interval_distribution
from Withdraw_Data_Anal import hist_counting
from Withdraw_Data_Anal import hist_counting_int

def func(x, a, b):
	return  a * x + b

def func2(x, a):
	return a * np.exp(-a*x)

def func3(x, a):
	return a / (x + a)**2

festival_list = ['2015-01-01',
				 '2015-01-02',
				 '2015-01-03',
				 '2015-02-18',
				 '2015-02-19',
				 '2015-02-20',
				 '2015-02-21',
				 '2015-02-22',
				 '2015-02-23',
				 '2015-02-24',
				 '2015-04-05',
				 '2015-04-06',
				 '2015-05-01',
				 '2015-05-02',
				 '2015-05-03',
				 '2015-06-20',
				 '2015-06-21',
				 '2015-06-22',
				 '2015-08-18',
				 '2015-09-03',
				 '2015-09-04',
				 '2015-09-27',
				 '2015-10-01',
				 '2015-10-02',
				 '2015-10-03',
				 '2015-10-04',
				 '2015-10-05',
				 '2015-10-06',
				 '2015-10-07']

df = pd.read_excel('./example/JCM_Withdraw_Data.xlsx', u'资金赎回记录')
#d0 = datetime.datetime(2015, 1, 9)
d0 = datetime.datetime(2015, 3, 23)
d1 = datetime.datetime(2015, 10, 11)

## Number of Withdrawing in each hour of a day
no_distribution = withdraw_no_distribution(df, u'日期', u'回款时间', d0, d1, only_weekdays=True, festival_list=festival_list)
no_distribution.to_csv('withdraw_no_distribution_weekdays_323.csv')
#no_distribution2 = withdraw_no_distribution(df, u'日期', u'回款时间', d0, d1, only_weekdays=False, festival_list=festival_list)
#no_distribution2.to_csv('withdraw_no_distribution_all_323.csv')
#no_distribution = withdraw_no_distribution(df, u'日期', u'回款时间', d0, d1)
#no_distribution.to_csv('withdraw_no_distribution_all.csv')


## Correlations between no of withdrawing in each hour ##
#df = pd.DataFrame(no_distribution.values[:-1, :], dtype=float)
#corr_mat = df.corr()
#plt.imshow(corr_mat.values[:-1, :-1], interpolation='nearest')
#plt.colorbar()
#plt.show()


## Plot the error bar ##
#columns = no_distribution.columns
#lower = int((len(no_distribution.index) - 1)*0.025) - 1
#upper = int((len(no_distribution.index) - 1)*0.975) - 1
#upper_bound = list()
#lower_bound = list()
#mean = list()
#for ii in range(len(columns)-1):
#	tmp = no_distribution[columns[ii]].values[:-1]
#	tmp.sort()
#	m = tmp.mean()
#	mean.append(m)
#	lower_bound.append(m - tmp[lower])
#	upper_bound.append(tmp[upper] - m)
#asymmetric_error = [lower_bound, upper_bound]
#
#x = [ii for ii in range(len(columns) -1)]
#fig, ax = plt.subplots()
#ax.errorbar(x, mean, yerr=asymmetric_error, fmt='o-', label="Working Days", linewidth=2.0, alpha=0.8)
#ax.legend()
#ax.set_xlabel(r'Hours', fontsize=24)
#ax.set_ylabel(r'Number of Withdrawing', fontsize=24)
#ax.axis([-0.1, 23.1, 0, 200])
#for tick in ax.xaxis.get_major_ticks():
#	tick.label1.set_fontsize(24)
#for tick in ax.yaxis.get_major_ticks():
#	tick.label1.set_fontsize(24)
#plt.show()


## distribution of number of withdrawing in each day ##
x = np.array([ii for ii in range(200)])
y = poisson.pmf(x, 100.32)
tmp = no_distribution['8h-9h'][:-1]
#tmp.sort()
#print tmp
#nn = int(len(tmp)*0.01)
#mm = len(tmp) - nn

res = hist_counting_int(tmp[:], normed=True)

fig, ax = plt.subplots()
ax.plot (res[:, 0], res[:, 1], 'r+-')
ax.plot(x, y, 'ko-')
ax.plot()
plt.show()


## Waiting Time Distribution ##
#t1 = 0
#t2 = 1
#interval_distribution = time_interval_distribution(df, u'日期', u'回款时间', d0, d1, t1, t2, only_weekdays=True, festival_list=festival_list)
#interval_distribution.sort()
#nn = int(len(interval_distribution) * 0.005)
#(res, gap) = hist_counting(interval_distribution[:-nn], bins=53)
#y = res[:, 1] / res[:, 1].sum() * 0.995
#print y.sum()
#y = y / gap
#popt, pcov = curve_fit(func, res[:27, 0], np.log(y[:27]) )
#popt, pcov = curve_fit(func3, res[:, 0], y[:])
#print popt
#fig, ax = plt.subplots()
##ax.plot(res[:,0], np.log(y[:]), 'ko', label="Original Noised Data")
##ax.plot(res[:,0], func(res[:,0], *popt), 'r-', label="Fitted Curve")
#ax.plot(res[:,0], y[:], 'ko', label="0:00-1:00", linewidth=2.0, alpha=0.8)
#ax.plot(res[:,0], np.exp(func(res[:,0], *popt)), 'r-', label="Fitted Curve", linewidth=2.0, alpha=0.8)
##ax.plot(res[:,0], func3(res[:,0], *popt), 'r-', label="Fitted Curve", linewidth=2.0, alpha=0.8)
#ax.set_xlabel(r'Waiting Time (s)', fontsize=24)
#ax.set_ylabel(r'Probability Density', fontsize=24)
#ax.axis([0, 750, 0, 0.016])
#ax.text(200, 0.011, r'$\ln{y}= -0.010632*x - 4.6664$', fontsize=24)
#for tick in ax.xaxis.get_major_ticks():
#	tick.label1.set_fontsize(24)
#for tick in ax.yaxis.get_major_ticks():
#	tick.label1.set_fontsize(24)
#ax.legend()
#plt.show()