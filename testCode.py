#coding:utf8
import fire
import datetime

def cal_days(date_str1, date_str2):
	'''计算两个日期之间的天数'''
	date_str1 = str(date_str1)
	date_str2 = str(date_str2)

	d1 = datetime.datetime.strptime(date_str1, '%Y%m%d')
	d2 = datetime.datetime.strptime(date_str2, '%Y%m%d')
	delta = d1 -d2
	return delta.days

def days2today(date_str):
	'''计算某个距离今天的天数'''

	date_str = str(date_str)
	d = datetime.datetime.strptime(date_str, '%Y%m%d')
	delta = datetime.datetime(now) - d
	
	return delta.days

if __name__ == '__main__':
	# fire.Fire(cal_days)  # 单个函数的情况下，可以使用fire.Fire()结果一样     python testCode.py 20170401
	fire.Fire()            # 多个函数的情况下，需要指定使用那个函数，否则会报错   python testCode.py cal_days 20170422 20170401