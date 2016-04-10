#coding=utf-8

import numpy as np 

class portfolio(object):
	def __init__(self, price, number, ratio):
		self.price = price.copy()
		self.number = number.copy()
		self.ratio = ratio.copy()
		self.cash = np.array([[0.0]])
		self.pv = np.dot(self.price, self.number.T)

	def test_rebalance(self, current_price, threshold=0.03):
		current_ratio = current_price * self.number / (np.dot(current_price, self.number.T) + self.cash)
		gap = abs(current_ratio - self.ratio)
		if gap.max() > threshold:
			return True
		else:
			return False

	def fix_ratio(self, current_price):
		current_pv = np.dot(current_price, self.number.T) + self.cash
		self.number = np.array((current_pv * self.ratio) / current_price, dtype=int)
		self.cash = current_pv - np.dot(current_price, self.number.T)
		self.price = current_price.copy()

	def cppi(self, current_price, alpha=0.25):
		current_pv = np.dot(current_price, self.number.T) + self.cash

		delta_price = (current_price - self.price) / self.price
		self.price = current_price.copy()

		delta_ratio = alpha * (delta_price - delta_price.mean())
		self.ratio += delta_ratio
		self.ratio /= self.ratio.sum()
		
		self.number = np.array(current_pv * self.ratio / self.price, dtype=int)
		self.cash = current_pv - np.dot(self.price, self.number.T)
		


if __name__ == '__main__':
	price = np.array([[5.0, 10.0, 15.0, 20.0]])
	number = np.array([[4000, 2000, 2000, 1500]])
	ratio = np.array([[0.2, 0.2, 0.3, 0.3]])
	increment = np.array([[1.01, 1.008, 1.002, 1.003], [1.002, 1.003, 1.01, 1.008]])
	portfolio1 = portfolio(price, number, ratio)
	nn = 0
	for ii in range(200):
		price *= increment[nn % 2]         # Oscilation
		#price *= increment[0]              # Trend
		if portfolio1.test_rebalance(price):
			nn += 1
			portfolio1.cppi(price, 0.4)
			#portfolio1.fix_ratio(price)
			#print "rebalance", ii, portfolio1.price, portfolio1.number, portfolio1.cash, np.dot(portfolio1.price, portfolio1.number.T) + portfolio1.cash


		print ii, ',', np.dot(price, portfolio1.number.T)[0][0] + portfolio1.cash[0][0], ',', np.dot(price, number.T)[0][0]
