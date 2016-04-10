#coding=utf-8

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
import tushare as ts 

def calc_daily_return(data_df):
	newindex = data_df.index.delete(-1)
	new_df = pd.DataFrame(data_df.close.values[1:], index=newindex, columns=['close'])
	return data_df.close / new_df.close - 1.0


shzs = ts.get_h_data('000001', index=True, start='1990-12-19', end='2016-02-24')
zjhj = ts.get_h_data('600489', autype='hfq', start='2003-08-14', end='2016-02-24')

yperc_shzs = calc_daily_return(shzs)
yperc_zjhj = calc_daily_return(zjhj)

plt.plot(yperc_shzs)
plt.show()