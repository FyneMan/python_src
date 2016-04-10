#coding=utf-8

import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
from Efficient_Frontier import Asset_Portfolio

# Diversification effects
# 4 assets
yield_rate4 = np.array([[0.19, 0.15, 0.12, 0.06]])
std4 = np.array([[0.24, 0.14, 0.13, 0.045]])
corr4 = np.array([[ 1.00, 0.60, 0.30, -0.25],
				  [ 0.60, 1.00, 0.45,  0.10],
				  [ 0.30, 0.45, 1.00,  0.30],
				  [-0.25, 0.10, 0.30,  1.00]])

w_guess4 = np.array([[0.25, 0.25, 0.25, 0.25]])
portfolio4 = Asset_Portfolio(4, yield_rate4, std4, corr4)
res4 = portfolio4.efficient_frontier(w_guess4, 150)
res4.to_csv('portfolio4.csv')

# 3 assets
yield_rate3 = np.array([[0.19, 0.12, 0.06]])
std3 = np.array([[0.24, 0.13, 0.045]])
corr3 = np.array([[ 1.00, 0.30, -0.25],
				  [ 0.30, 1.00,  0.30],
				  [-0.25, 0.30,  1.00]])
w_guess3 = np.array([[0.33, 0.34, 0.33]])
portfolio3 = Asset_Portfolio(3, yield_rate3, std3, corr3)
res3 = portfolio3.efficient_frontier(w_guess3, 150)
res3.to_csv('portfolio3.csv')

# 2 assets
yield_rate2 = np.array([[0.19, 0.06]])
std2 = np.array([[0.24, 0.045]])
corr2 = np.array([[ 1.00, -0.25],
				  [-0.25,  1.00]])
w_guess2 = np.array([[0.5, 0.5]])
portfolio2 = Asset_Portfolio(2, yield_rate2, std2, corr2)
res2 = portfolio2.efficient_frontier(w_guess2, 150)
res2.to_csv('portfolio2.csv')

# plot the figure
fig, ax = plt.subplots()
ax.plot(res4.risk, res4.yields, 'r-x', linewidth=2, label=r'Portfolio of asset 1, 2, 3, 4', alpha=0.6)
ax.plot(res3.risk, res3.yields, 'b-x', linewidth=2, label=r'Portfolio of asset 1, 3, 4', alpha=0.6)
ax.plot(res2.risk, res2.yields, 'g-x', linewidth=2, label=r'Portfolio of asset 1, 4', alpha=0.6)
ax.legend(loc='upper center')
ax.set_xlabel(r'Risk', fontsize=24)
ax.set_ylabel(r'Return', fontsize=24)
ax.axis([0.00, 0.25, 0.04, 0.22])
for tick in ax.xaxis.get_major_ticks():
    tick.label1.set_fontsize(24)
for tick in ax.yaxis.get_major_ticks():
    tick.label1.set_fontsize(24)
plt.show()
