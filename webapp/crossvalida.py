# -*- coding:utf-8 -*-
from utils.baseBrowser import BaseBrowser
from webapp.comlogin import test_comLogin
from selenium.webdriver.support.select import Select
import time, unittest
from service.myglobal import get_value
from utils.baseLog import MyLog as Log
from service.pageObject import PageObject
from utils.baseUtils import *

log = Log.get_log()
logger = log.logger
'''
第二步，进件管理-交叉质检菜单，10011403苗双伟
'''


class test_crossValida(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		# 必须使用@classmethod 装饰器,所有test运行前运行一次
		# 得到driver实例
		self.driver = BaseBrowser.getDriver()
		# 初始化页面元素
		self.base = PageObject(self.driver)
		logger.info("第二步************************crossvalida.py，进件管理-交叉质检，10011403，苗双伟")

	'''
	用另外一个角色进行“交叉质检”
	'''

	def test_crossValida(self):
		try:
			# 通过第一步进件申请，得到进件编号
			self.intoappId = get_excel("intoAppId", "1", "loanopenbank")
			# intoappId = get_value()
			logger.info("通过第一步进件申请，得到进件编号：" + self.intoappId)
			# 进入“借款系统”,与哪个环境
			httpname = "LOANJC3"
			systemname = "loan"
			# 根据用户名，密码，登录方法
			test_comLogin.test_login(self.driver, "10012746", "Cs654321", httpname, systemname)
			# 关闭第一个菜单“客户管理”菜单
			self.base.click(("id,firstMenu0"))
			# 打开需要展示的“进件管理”菜单
			self.base.click(("id,firstMenu2"))
			# 点击“交叉质检”菜单
			self.base.click(("xpath,//span[text()=' 交叉质检']"))
			# 进入“交叉质检”iframe页面
			self.base.switchFrame(("iframe,queryEachCheckLbTIntoInfo"))
			# 输入进件编号
			self.base.send_keys(("name,intoAppId"), self.intoappId)
			# 点“查询”按钮
			self.base.click(("xpath,//span[text()='查询']"))
			# 选中第一条数据
			self.base.click(("xpath,//input[@type='radio']"))
			# 点击“质检”按钮
			self.base.click(("link_text,质检"))
			# 退出“交叉质检”iframe
			self.base.switchFramedefault()
			# 通过质检按钮，进入另外一个“交叉质检”iframe
			self.base.switchFrame(("iframe,eachCheckLbTIntoInfo"))
			# 质检结果“通过”
			self.base.selectByValue(("id,eachCheckResultCode"), "10")
			# 点“提交”按钮
			self.base.click(("id,doSubmitInto"))
			# 退出该“交叉质检”iframe
			self.base.switchFramedefault()
		except Exception as err:
			logger.info("交叉质检错误信息：")
			logger.error(err)

	@classmethod
	def tearDownClass(self):
		# 必须使用 @ classmethod装饰器, 所有test运行完后运行一次
		BaseBrowser.quit_browser(self.driver)


if __name__ == '__main__':
	unittest.main()
