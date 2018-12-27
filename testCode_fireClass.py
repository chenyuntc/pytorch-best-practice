#coding:utf8
import fire
import datetime

class DateStr(object):
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
	# fire.Fire()          # 多个函数的情况下，需要指定使用那个函数，否则会报错   python testCode.py cal_days 20170422 20170401
	fire.Fire(DataStr)     # 传入类名，调用可以按照多个函数的情况下调用

'''
备注： 
fire 默认使用 - 作为参数分隔符，所以如果你要在命令行传入类似 2017-04-22 的参数时，那么程序接收到的参数就肯定不是 2017-04-22 了
你需要使用 --separator 来改变分隔符，参考 Changing the Separator
fire 会自动区分你在命令行传入的参数的类型，例如 20170422 会自动识别成 int，hello 会自动识别成 str，'(1,2)' 会自动识别成 tuple，'{"name": "Alan Lee"}' 会自动识别成 dict。
但是你如果想要传入一个字符串类型的 20170422 怎么办？那就需要这样写：'"20170422"' 或者 "'20170422'" 或者 \"20170422\"，总之呢，就是加一个转义，因为命令行默认会吃掉你的引号
'''