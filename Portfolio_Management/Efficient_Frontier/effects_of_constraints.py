#coding=utf-8

import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
from Efficient_Frontier import Asset_Portfolio

# 4 assets
yield_rate4 = np.array([[0.19, 0.15, 0.12, 0.06]])
std4 = np.array([[0.24, 0.14, 0.13, 0.045]])
corr4 = np.array([[ 1.00, 0.60, 0.30, -0.25],
				  [ 0.60, 1.00, 0.45,  0.10],
				  [ 0.30, 0.45, 1.00,  0.30],
				  [-0.25, 0.10, 0.30,  1.00]])

w_guess4 = np.array([[0.25, 0.25, 0.25, 0.25]])
portfolio4 = Asset_Portfolio(4, yield_rate4, std4, corr4)
res1 = portfolio4.efficient_frontier(w_guess4, 150)
res1.to_csv('portfolio4.csv')


bound = [(0.1, 0.7), (0.1, 0.7), (0.1, 0.7), (0.1, 0.7)]
res2 = portfolio4.efficient_frontier(w_guess4, 150, bound)
res2.to_csv('portfolio4_c.csv')

fig, ax = plt.subplots()
ax.plot(res1.risk, res1.yields, 'r-x', linewidth=2, label=r'$0.0 \leq w_i \leq 1.0$', alpha=0.6)
ax.plot(res2.risk, res2.yields, 'b-+', linewidth=2, label=r'$0.1 \leq w_i \leq 0.7$', alpha=0.6)
ax.legend(loc='upper center')
ax.set_xlabel(r'Risk', fontsize=24)
ax.set_ylabel(r'Return', fontsize=24)
ax.axis([0.00, 0.25, 0.04, 0.22])
for tick in ax.xaxis.get_major_ticks():
    tick.label1.set_fontsize(24)
for tick in ax.yaxis.get_major_ticks():
    tick.label1.set_fontsize(24)
plt.show()