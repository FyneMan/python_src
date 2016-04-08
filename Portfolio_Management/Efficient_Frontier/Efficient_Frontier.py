#coding=utf-8

import numpy as np 
import scipy.optimize as opt
import pandas as pd 
import matplotlib.pyplot as plt

class Asset_Portfolio(object):

	def __init__(self, N, yield_rate, std, corr):
		'''
		N            ::  number of assets in the portfolio, an integer
		yield_rate   ::  return of each asset, a ndarray with a shape of 1 x N (a row vector)
		std          ::  standard deviations of each asset, a ndarray with a shape of 1 x N (a row vector)
		corr         ::  correlation coefficient matrix, a ndarray with a shape of N x N
		'''
		self.N = N
		self.yield_rate = yield_rate.copy()
		self.std = std.copy()
		self.corr = corr.copy()

		self.cov = np.dot(self.std.T, self.std) * self.corr


	def portfolio_variance(self, w):
		'''
		w            ::  weights of each asset in the portfolio, a ndarray with a shape of 1 x N (a row vector)
		return       ::  variance of the portfolio
		'''
		tmp = np.dot(w, self.cov)
		return np.dot(tmp, w.T)


	def opt_weight(self, w0, r0, bounds=None):
		'''
		w0           ::  initial weights vector by guessing, a ndarray with a shape of 1 x N (a row vector)
		r0           ::  return requirement of the portfolio
		bounds       ::  bound for each weight element, a list of (min, max) pairs for each element
		'''
		if (bounds == None):
			bounds = list()
			for ii in range(self.N):
				bounds.append((0.0, 1.0))

		cons = ({'type' : 'eq',
				 'fun' : lambda w0 : np.sum(w0) - 1.0},    # sum of all the weights is 1
				{'type' : 'eq',
				 'fun' : lambda w0 : np.dot(w0, self.yield_rate.T) - r0})    # return of the portfolio is r0

		res = opt.minimize(self.portfolio_variance, w0, bounds=bounds, constraints=cons, method='SLSQP')

		if (not res.success):
			print res.message
			print r0, 'failed'
			print res.x
		return res.x


	def return_range(self, w0, bounds=None):
		'''
		Calculte the range of the return of the portfolio with the constraints of bound
		'''
		if (bounds == None):
			bounds = list()
			for ii in range(self.N):
				bounds.append((0.0, 1.0))

		cons = ({'type' : 'eq',
				 'fun' : lambda w0 : np.sum(w0) - 1.0})

		f1 = lambda w0 : np.dot(w0, self.yield_rate.T)
		f2 = lambda w0 : -np.dot(w0, self.yield_rate.T)
		min_r = opt.minimize(f1, w0, bounds=bounds, constraints=cons, method='SLSQP')
		max_r = opt.minimize(f2, w0, bounds=bounds, constraints=cons, method='SLSQP')

		return (min_r.fun[0], -max_r.fun[0])


	def efficient_frontier(self, w_guess, nn=100, bounds=None):
		'''
		Calculte the efficient frontier of the portfolio.
		w_guess      ::   initial guess of the optimized weights, a ndarray with shape of 1 x N (a row vector)
		nn           ::   number of points to calculate, an integer
		bounds       ::   bound for each weight element, a list of (min, max) pairs for each element
		return       ::   DataFrame containing the return and the risk
		'''
		if (bounds == None):
			bounds = list()
			for ii in range(self.N):
				bounds.append((0.0, 1.0))

		result = np.zeros(nn * (self.N + 2)).reshape(nn, self.N + 2)
		columns = ['risk', 'yields']
		for ii in range(self.N):
			name = 'weight' + str(ii)
			columns.append(name)

		(lower, upper) = self.return_range(w_guess, bounds)
		r0 = np.linspace(lower, upper, nn)
		for ii in range(nn):
			weights = self.opt_weight(w_guess, r0[ii], bounds)
			weights.shape = w_guess.shape
			variance = np.sqrt( self.portfolio_variance(weights)[0,0] )
			result[ii][0] = variance
			result[ii][1] = r0[ii]
			result[ii][2:] = weights

		df = pd.DataFrame(result, columns=columns)
		return df

		
# An example with four assets
if __name__ == '__main__':
	yield_rate = np.array([[0.06, 0.12, 0.15, 0.19]])
	std = np.array([[0.04, 0.14, 0.14, 0.24]])
	corr = np.array([[ 1.00, 0.60, 0.30, -0.25],
					 [ 0.60, 1.00, 0.45,  0.10],
					 [ 0.30, 0.45, 1.00,  0.30],
					 [-0.25, 0.10, 0.30,  1.00]])

	w_guess = np.array([[0.25, 0.25, 0.25, 0.25]])

	portfolio = Asset_Portfolio(4, yield_rate, std, corr)
	res = portfolio.efficient_frontier(w_guess, 150)
	res.to_csv('portfolio.csv')
	#res_s = res.sort(columns=['risk', 'weight3'], ascending=True, inplace=True)

	bound = [(0.1, 0.7), (0.1, 0.7), (0.1, 0.7), (0.1, 0.7)]
	yield_rate2 = yield_rate
	#yield_rate2 = np.array([[0.07, 0.11, 0.16, 0.18]])
	portfolio2 = Asset_Portfolio(4, yield_rate2, std, corr)
	res2 = portfolio2.efficient_frontier(w_guess, 100, bound)

	fig, ax = plt.subplots()
	#ax.plot(res.risk, res.yields, 'r-x', linewidth=2, label=r'$0.0 \leq w_i \leq 1.0$', alpha=0.6)
	#ax.plot(res2.risk, res2.yields, 'b-+', linewidth=2, label=r'$0.1 \leq w_i \leq 0.7$', alpha=0.6)
	#ax.plot(res.risk, res.yields, 'r-x', linewidth=2, label=r'Portfolio 1', alpha=0.6)
	#ax.plot(res2.risk, res2.yields, 'b-+', linewidth=2, label=r'Portfolio 2', alpha=0.6)
	ax.stackplot(res2.yields, res2.weight0, res2.weight1, res2.weight2, res2.weight3, alpha=0.5)
	ax.legend()
	#ax.legend(('weight1', 'weight2', 'weight3', 'weight4'))
	ax.set_xlabel(r'Return', fontsize=24)
	#ax.set_ylabel('Return', fontsize=20)
	ax.set_ylabel(r'Weights', fontsize=24)
	ax.axis([0.088, 0.166, 0.0, 1.0])
	for tick in ax.xaxis.get_major_ticks():
		tick.label1.set_fontsize(24)
	for tick in ax.yaxis.get_major_ticks():
		tick.label1.set_fontsize(24)
	plt.show()


