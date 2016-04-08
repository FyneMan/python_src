#coding=utf-8

import numpy as np 
import pandas as pd 

def excel_to_csv(filename, sheet_name, sep=',', code='utf-8'):
	df = pd.read_excel(filename, sheet_name)   # pandas读取excel文件，结果都会以unicode的编码进行存储
	#print df['日期']    # 不能正确输出，因为这里的‘日期’是utf-8编码，与读入的unicode不同
	#print df[u'日期']    # 可以正确输出，因为‘日期’前面的u将字符串转换成了unicode，与读入的数据相同
	df.to_csv(filename+'.csv', index=False, sep=sep, encoding=code)  # 对于有中文字符的文件，写入文件需要对unicode编码进行编码，不然不能正确输出


if __name__ == '__main__':
	excel_to_csv('./example/test.xlsx', u'工作表1', sep='$', code='utf-8')   # 将excel文件读入，然后以utf-8的编码形式写入csv文件
	#data = pd.read_csv('./example/test.xlsx.csv', sep='$', encoding='utf-8')  # pandas读取csv文件，将原文件的utf-8编码解码成unicode形式。
	#print data[u'日期']
	#data.to_csv('./example/test.xlsx.csv', index=False, sep='$', encoding='utf-8')   # 这里必须要给encoding这个参数
	data = pd.read_csv('./example/test.xlsx.csv', sep='$')  # pandas读取csv文件，保持原csv文件的编码模式
	print data['日期']
	data.to_csv('xxx.csv', index=False, sep='$')   # 这里不能给encoding这个参数
