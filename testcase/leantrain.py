# -*- coding:utf-8 -*-
from selenium import webdriver
import  re, time, os
class leantrain():
	def getdriver(self):
		self.driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
		self.driver.maximize_window()
	def pageElement(self):
		driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
		driver.maximize_window()
		driver.get("http://home.baidu.com/contact.html")
		doc = driver.page_source
		emails = re.findall(r'[\w]+@[\w\.-]+', doc)  # 利用正则，找出 xxx@xxx.xxx 的字段，保存到emails列表
		# 循环打印匹配的邮箱
		for email in emails:
			print(email)
	#获取页面中的源码
	def pagesource(self):
		driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
		driver.get("http://www.cnblogs.com/yoyoketang/")
		page = driver.page_source
		# print page
		# "非贪婪匹配,re.S('.'匹配字符,包括换行符)"
		url_list = re.findall('href=\"(.*?)\"', page, re.S)
		url_all = []
		for url in url_list:
			if "http" in url:
				#print(url)
				url_all.append(url)
		# 最终的url集合
		print(url_all)
	# 保存图片
	def get_window_img(self):
		self.driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
		self.driver.maximize_window()
		print(os.path.abspath("."))
		file_path = os.path.dirname(os.path.abspath("."))+"\screenshots\\"
		self.driver.get("http://home.baidu.com/contact.html")
		rs = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
		screen_name = file_path + rs +".png"
		try:
			self.driver.get_screenshot_as_file(screen_name)
		except NameError as e:
			self.get_window_img()
if __name__ =='__main__':
	lr = leantrain()
	lr.pagesource()

