#coding=utf-8

import datetime
import calendar
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

def add_months(dt, months):
    month = dt.month - 1 + months
    year = dt.year + month / 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return datetime.datetime(year=year, month=month, day=day)


class Asset_Portfolio(object): 

	def __init__(self):
		columns = ['amount', 'start', 'end', 'rate', 'interests']
		self.Asset = pd.DataFrame(columns=columns)

	def add_asset(self, amount, start, maturity, rate, interests):
		start_date = start.strftime('%Y-%m-%d')
		end_date = add_months(start, maturity).strftime('%Y-%m-%d')
		self.Asset.loc[ len(self.Asset) ] = [amount, start_date, end_date, rate, interests]

	def asset_maturity(self, Date):
		time = Date.strftime('%Y-%m-%d')
		df_tmp = self.Asset[self.Asset.end == time]

		principal = df_tmp.amount.sum()
		interests = df_tmp.interests.sum()
		return (principal, interests)


class Liab_Portfolio(object):

	def __init__(self):
		columns = ['amount', 'start', 'end', 'rate', 'interests']
		self.Liab = pd.DataFrame(columns=columns)

	def add_liab(self, amount, start, maturity, rate, interests):
		start_date = start.strftime('%Y-%m-%d')
		end_date = add_months(start, maturity).strftime('%Y-%m-%d')
		self.Liab.loc[ len(self.Liab) ] = [amount, start_date, end_date, rate, interests]

	def liab_maturity(self, Date):
		time = Date.strftime('%Y-%m-%d')
		df_tmp = self.Liab[self.Liab.end == time]

		principal = df_tmp.amount.sum()
		interests = df_tmp.interests.sum()
		return (principal, interests)


def add_DengBenDengXi(AP, amount, periods, nomial_rate, start):
	principal = amount / periods
	interests = amount * nomial_rate / 12.0
	for ii in range(periods):
		AP.add_asset(principal, start, ii+1, nomial_rate, interests)


def add_Prod(LP, amount, periods, nomial_rate, start, ratio):
	for ii in range( len(periods) ):
		principal = amount * ratio[ii]
		interests = principal * periods[ii] / 12.0 * nomial_rate[ii]
		LP.add_liab(principal, start, periods[ii], nomial_rate[ii], interests)


# Example to show the ReFin requirement
if __name__ == '__main__':
	AP = Asset_Portfolio()
	LP = Liab_Portfolio()

	a_rate = 0.05
	a_periods = 12

	p_periods = [1, 3, 6, 12]
	p_rate = [0.06, 0.07, 0.08, 0.09]
	p_ratio = [1.0, 0.0, 0.0, 0.0]

	new_Asset = 36000
	ReFin = 0.0
	dt = datetime.datetime(2015, 10, 1)
	interests = 0.0
	RF_List = []
	i_List = []
	index = []

	for ii in range(300):
		if (new_Asset + ReFin) > 0:
			add_DengBenDengXi(AP, new_Asset, a_periods, a_rate, dt)
			add_Prod(LP, new_Asset+ReFin, p_periods, p_rate, dt, p_ratio)
		else:
			add_DengBenDengXi(AP, abs(ReFin), a_periods, a_rate, dt)

		(AM_principal, AM_interests) = AP.asset_maturity(dt)
		(PM_principal, PM_interests) = LP.liab_maturity(dt)

		ReFin = PM_principal - AM_principal
		interests += (AM_interests - PM_interests)
		RF_List.append(ReFin + 36000.0)
		i_List.append(interests)
		index.append(ii)

		dt = dt + datetime.timedelta(days = 1)

		print ii, ReFin, interests

	plt.plot(index, i_List)
	plt.show()