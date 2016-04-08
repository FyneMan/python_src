#coding=utf-8

from scipy.optimize import brentq

class DengBenDengXi(object):
	"""
	At the end of each period, the borrower repays the same amount of principal
	and interests. The principal are reinvested, while the interests are not.

	"""

	def __init__(self, total_amount, nn, nomial_R):
		self.total_amount = total_amount
		self.nn = nn
		self.nomial_R = nomial_R
		self.principal = self.total_amount / self.nn
		self.interest = self.total_amount * self.nomial_R / 12.0

	# Interests of both the Asset and the Liability are not reinvested	
	def interest_gap_function_by_month(self, r):
		x = 0.0
		for ii in range(self.nn):
			x += self.principal * (ii + 1) * r
		x -= self.interest * self.nn
		return x

	def earning_rate_by_month(self):
		return brentq(self.interest_gap_function_by_month, 0.0, 0.3)

	def earning_rate_by_year(self):
		return 12.0 * self.earning_rate_by_month()

	# Interests of Asset are not reinvested, while that of Liability are reinvested
	# Because, in fact, interests of Liability are reinvested by investors when the maturity 
	# of products are short
	def interest_gap_function_by_month2(self, r):
		x = 0.0
		tmp = 1.0
		for ii in range(self.nn):
			tmp *= (1 + r)
			x += self.principal * (tmp - 1.0)
		x -= self.interest * self.nn
		return x

	def earning_rate_by_month2(self):
		return brentq(self.interest_gap_function_by_month2, 0.0, 0.3)
	
	def earning_rate_by_year2(self):
		return (1 + self.earning_rate_by_month2())**12 - 1	


x = DengBenDengXi(26400, 12, 0.034)
print x.earning_rate_by_month()
print x.earning_rate_by_month2()
print x.earning_rate_by_year()
print x.earning_rate_by_year2()
