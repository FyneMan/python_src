#coding=utf-8

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

if __name__ == '__main__':
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
					 '2015-09-27',
					 '2015-10-01',
					 '2015-10-02',
					 '2015-10-03',
					 '2015-10-04',
					 '2015-10-05',
					 '2015-10-06',
					 '2015-10-07']
	#print datetime.datetime(2015, 2, 19).strftime('%Y-%m-%d') in festival_list
	start = datetime.datetime(2015, 1, 9)
	end = datetime.datetime(2015, 3, 1)
	close_days = holidays(start, end, festival_list)
	print close_days
