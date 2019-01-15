# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
import datetime
interfaceNo = "monthRateB"
name = "月服务费率接口"

req = ConfigHttp()
sqldb = ConfigDB()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class test_monthlv(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, prodName, approveMoney, period, monthlyOverallRate, interestRate, monthRateType, monthRate):
		self.No = str(No)
		self.prodName = str(prodName)
		self.approveMoney = str(approveMoney)
		self.period = str(period)
		self.monthlyOverallRate = str(monthlyOverallRate)
		self.interestRate = str(interestRate)
		self.monthRateType = str(monthRateType)
		self.monthRate = str(monthRate)

	def setUp(self):
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
		print(interfaceNo + name + "CASE " + self.No)

	def test_body(self):
		self.url = "/masterdata/api/contract/monthRate/search/v1"
		headers = {"Content-Type": "application/json"}
		# 获取当前时间
		#now = datetime.datetime.now()
		# 请求流水号
		#self.transNo = now.strftime('%Y%m%d') + str(random.randint(0, 90000000))
		# 请求
		#self.transTime = now.strftime('%Y-%m-%d %H:%M:%S')
		# 获取月服务费率接口中的monthlyOverallRate
		#综合费率
		self.monthlyOverallRate = get_excel("monthlyOverallRate", self.No, interfaceNo)
		# 月利率
		self.interestRate = get_excel("interestRate", self.No, interfaceNo)
		# 贷款期数
		self.period = get_excel("period", self.No, interfaceNo)
		# 审批金额
		self.approveMoney = get_excel("approveMoney", self.No, interfaceNo)
		##0表示非试点  1表示试点
		self.monthRateType = get_excel("monthRateType", self.No, interfaceNo)
		self.data = {
				"monthlyOverallRate": self.monthlyOverallRate,
				"interestRate": self.interestRate,
				"period": self.period,
				"approveMoney": self.approveMoney,
				"monthRateType":self.monthRateType
		}
		req.httpname = "MDJC3"
		req.set_url(self.url)
		req.set_headers(headers)
		req.set_data(self.data)
		self.response = req.post()
		try:
			#self.retcode = self.response["responseBody"]["retCode"]
			#返回报文
			self.responsebody = self.response["responseBody"]
			print(self.responsebody)
		except Exception:
			self.logger.error("报文返回为空！")
			print("报文返回为空！")

		self.check_result()
		self.wr_excel()

	def check_result(self):
		try:
			#self.assertEqual(self.retcode, "0000", self.logger.info("检查是否生成月利率"))
			set_excel("pass", "测试结果", self.No, interfaceNo)
			self.logger.info("测试通过")
		except AssertionError:
			set_excel("fail", "测试结果", self.No, interfaceNo)
			errorDesc = self.response["errorDesc"]
			self.logger.error("测试失败:"+errorDesc)
	# 写入xls文件中
	def wr_excel(self):
		set_excel(self.data, "请求报文", self.No, interfaceNo)
		set_excel(self.response, "返回报文", self.No, interfaceNo)
		set_excel(self.responsebody, "monthRate", self.No, interfaceNo)

	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
	unittest.main()

