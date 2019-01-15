# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
'''
页面公共元素
'''
class PageObject(object):
	# 初始化数据
	def __init__(self, driver):
		self.driver = driver
	'''
	elementWait
	设置元素等待时间
	'''
	def elementWait(self, locator, timeout=10):
		# 判断表达式是否包含指定字符
		if "," not in locator:
			raise NameError("输入的元素未包含','.")
		by = locator.split(",")[0]
		value = locator.split(",")[1]
		# 提取元素定位方式和定位表达式 ,
		#presence_of_element_located这两个人条件验证元素是否出现，传入的参数都是元组类型的locator，如(By.ID, 'kw')
		#一个只要一个符合条件的元素加载出来就通过
		if by == "id":
			#等待页面加载完成，找到某个条件发生后再继续执行后续代码，如果超过设置时间检测不到则抛出异常
			WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located((By.ID, value)))
		elif by == "name":
			WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located((By.NAME, value)))
		elif by == "class":
			WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located((By.CLASS_NAME, value)))
		elif by == "link_text":
			WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located((By.LINK_TEXT, value)))
		elif by == "xpath":
			WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located((By.XPATH, value)))
		elif by == "locator":
			WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located((By.locator_SELECTOR, value)))
		elif by == "iframe":
			iframeto = "//iframe[contains(@src,'" + value + "')]"
			WebDriverWait(self.driver, timeout, 1).until(EC.presence_of_element_located((By.XPATH, iframeto)))
		else:
			raise NameError("请输入对应的元素名称：'id','name','class','link_text','xpath','locator'.")

	'''
	获取指定元素对象
	表达式：  by=>value （by为定位方式,value为定位方式的表达式,例如:按照id定位某个元素,id=>"#"）
	'''
	def find_element(self, locator):
		# 判断表达式是否包含指定字符
		if "," not in locator:
			raise NameError("输入的元素未包含,")
		by = locator.split(",")[0]
		value = locator.split(",")[1]
		# 提取元素定位方式和定位表达式 ,
		#presence_of_element_located这两个人条件验证元素是否出现，传入的参数都是元组类型的locator，如(By.ID, 'kw')
		#顾名思义，一个只要一个符合条件的元素加载出来就通过
		if by == "id":
			element = self.driver.find_element_by_id(value)
		elif by == "name":
			element = self.driver.find_element_by_name(value)
		elif by == "class":
			element = self.driver.find_element_by_class_name(value)
		elif by == "link_text":
			element = self.driver.find_element_by_link_text(value)
		elif by == "xpath":
			element = self.driver.find_element_by_xpath(value)
		elif by == "locator":
			element = self.driver.find_element_by_locator_selector(value)
		elif by == "iframe":
			iframeto = "//iframe[contains(@src,'" + value + "')]"
			element = self.driver.find_element_by_xpath(iframeto)
		else:
			raise NameError("请输入对应的元素名称：'id','name','class','link_text','xpath','locator'.")
		return element

	'''
	鼠标单击
	'''
	def click(self, locator):
		time.sleep(5)
		self.elementWait(locator)
		self.find_element(locator).click()

	'''
	封装一个send_keys
	'''
	def send_keys(self, locator, text):
		self.elementWait(locator)
		self.find_element(locator).send_keys(text)

	'''
	清空input中的文本
	'''
	def clear(self, locator):
		self.elementWait(locator)
		self.find_element(locator).clear()
	
	'''
	 鼠标左键点击链接文本
	'''
	def partialLinkTextClick(self, text):
		self.driver.find_element_by_partial_link_text(text).click()
	
	'''
	获取指定元素的文本内容,即value属性值
	'''
	def getText(self, locator):
		self.elementWait(locator)
		self.find_element(locator).text

	'''
	判断元素是否可见
	'''
	def isDisplay(self, locator):
		self.elementWait(locator)
		return self.find_element(locator).is_displayed()

	'''
	判断元素是否启用
	'''
	def isEnabled(self, locator):
		self.elementWait(locator)
		return self.find_element(locator).is_enabled()

	'''
	判断元素是否选中,一般用于验证checkbox和radio
	'''
	def isSelected(self, locator):
		self.elementWait(locator)
		return self.find_element(locator).is_selected()

	'''
	根据指定的值选中相应的下拉列表中的选项
	--如果没有指定的值则抛出异常
	'''
	def selectByValue(self, locator, value):
		time.sleep(2)
		self.elementWait(locator)
		Select(self.find_element(locator)).select_by_value(value)

	'''
	弹框警告-确认
	'''
	def alertAccept(self):
		self.driver.switch_to.alert.accept()

	'''
	弹框警告-取消
	'''
	def alertDismiss(self):
		self.driver.switch_to.alert.dismiss()

	'''
	切换到指定的iframe
	'''
	def switchFrame(self, locator):
		# implicitly_wait() 方法就可以方便的实现智能等待,智能等待5s，隐式等待
		time.sleep(5)
		self.elementWait(locator)
		self.driver.switch_to.frame(self.find_element(locator))

	'''
	切换到上一级(iframe)
	'''
	def switchFramedefault(self):
		self.driver.switch_to.default_content()
	'''
	打开新页面,并切换当前句柄为新页面的句柄
	(每个页面对应一个句柄handle,可以通过self.driver.window_handles查看所有句柄)
	'''
	def openNewWindow(self, current_window):
		#获取所有窗口handle name
		all_windows = self.driver.window_handles
		# 切换window，如果window不是当前window，则切换到该window
		for window in all_windows:
			# 新打开的window不等于当前window时
			if window != current_window:
				# 则打开新的window
				self.driver.switch_to.window(window)

	'''
	等待元素,10秒,每1秒检查一次
	如果超时,返回false
	'''
	def waitEleAndExceptionForTimeout(self, locator):
		try:
			self.elementWait(locator, secs=10)
			return True
		except Exception:
			return False

	'''
	鼠标右键单击
	'''
	def rightClick(self, locator):
		self.elementWait(locator)
		ActionChains(self.driver).context_click(self.find_element(locator)).perform()

	'''
	移动鼠标到指定元素(默认在元素的中间位置)
	'''
	def moveToTarfind_element(self, locator):
		self.elementWait(locator)
		ActionChains(self.driver).move_to_element(self.find_element(locator)).perform()
		
	'''
	鼠标左键双击
	'''
	def doubleClick(self, locator):
		self.elementWait(locator)
		ActionChains(self.driver).double_click(self.find_element(locator)).perform()

	'''
	拖拽元素到指定元素处
	'''
	def dragAndDropToElement(self, sourcelocator, targetlocator):
		self.elementWait(sourcelocator)
		self.elementWait(targetlocator)
		ActionChains(self.driver).drag_and_drop(self.find_element(sourcelocator),self.find_element(targetlocator)).perform()

	'''
	拖拽元素指定偏移(该偏移是相对于当前鼠标的坐标偏移量)
	'''
	def dragAndDropToOffset(self, sourcelocator, xoffset, yoffset):
		self.elementWait(sourcelocator)
		ActionChains(self.driver).drag_and_drop_by_offset(self.find_element(sourcelocator), xoffset, yoffset).perform()

	'''
	判断元素是否被定位到
	'''
	def is_exists(self, locator, timeout=20):
		try:
			# 不需要*,这里跟*locator不是一个参数
			WebDriverWait(self.driver, timeout, 0.5).until(EC.presence_of_element_located(locator))
			return True
		except:
			return False


if __name__=='__main__':
	driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
	driver.maximize_window()
	driver.get("http://www.baidu.com")
	po = PageObject(driver)
	kwId =("id,kw")
	po.send_keys(kwId,"WebDriverWait的用法")
	btn = ("id,su")
	po.click(btn)