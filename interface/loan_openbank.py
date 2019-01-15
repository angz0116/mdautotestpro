# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
import datetime
from service.gainHtml import savehtml,openbindBank

interfaceNo = "loanopenbank"

name = "贷款绑定银行卡接口2062"

req = ConfigHttp()
sqldb = ConfigDB()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class test_loanbindbank(unittest.TestCase):
	def setParameters(self, No, 测试结果, custCode, cardNo, bankMobile, bankAcctNo, custName, bankCode, intoAppId):
		self.No = str(No)
		self.custCode = str(custCode)
		self.cardNo = str(cardNo)
		self.bankMobile = str(bankMobile)
		self.bankAcctNo = str(bankAcctNo)
		self.bankAcctName = str(custName)
		self.bankCode = str(bankCode)
		self.intoAppId = str(intoAppId)

	def setUp(self):
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
		print(interfaceNo + name + "CASE " + self.No)

	def test_body(self):
		req.httpname = "CORELJC3"
		self.url = "/core-interface/api/loan/2118/v1"
		headers = {"Content-Type": "application/json"}
		# 获取客户编号
		self.custCode = get_excel("custCode", self.No, interfaceNo)
		# 获取身份证号
		self.cardNo = get_excel("cardNo", self.No, interfaceNo)
		# 获取银行卡号
		self.bankAcctNo = get_excel("bankAcctNo", self.No, interfaceNo)
		# 根据银行卡号，获取银行代码
		self.bankCode = get_excel("bankCode", self.No, interfaceNo)
		# 获取客户姓名
		self.bankAcctName = get_excel("custName", self.No, interfaceNo)
		# 获取预留手机号
		self.mobile = get_excel("bankMobile", self.No, interfaceNo)
		# 获取当前时间
		now = datetime.datetime.now()
		# 请求流水号
		self.transNo = now.strftime('%Y%m%d') + str(random.randint(0, 90000000))
		# 绑定银行流水号
		self.bindCardSid = now.strftime('%Y%m%d') + str(random.randint(0, 20000000))
		# 请求
		self.transTime = now.strftime('%Y-%m-%d %H:%M:%S')
		self.data = {
			"interfaceNo": "2118",
			"bankCardNo": self.bankAcctNo,
			"bankCardType": "10", #银行卡类型 10-个人借记 20-个人贷记
			"bankCode": self.bankCode,
			"busiCode": "LBB118", #业务编码
			"callPageUrl": "http://172.18.100.39:8081/fintech-appbiz/deposit/appCashRecordCallback",
			"certId": self.cardNo,
			"certType": "1",
			"checkFlag": "0",
			"custCode": self.custCode,
			"custName": self.bankAcctName,
			"custType": "0",
			"depositCode": "02", #存管渠道 00-非存管01-华瑞（存管）02-恒丰（存管）03-向上（存管）
			"frontTransNo": self.transNo,
			"frontTransTime": self.transTime,
			"isAppFlg": "0",
			"phone": self.mobile,
			"serialNumber": self.bindCardSid,
			"subsidiaryCode": "JYJF",#开户主体
			"sysSource": "2"
		}
		req.set_url(self.url)
		req.set_headers(headers)
		req.set_data(self.data)
		self.response = req.post()
		print("贷款--绑定银行卡接口**==" + "手机号：" + self.mobile + "**==客户编号：" + self.custCode + "**==银行卡号：" + self.bankAcctNo + "**==银行代码：" + self.bankCode)
		try:
			print(self.response)
			self.retcode = self.response["retCode"]
			# 从返回报文中截取html文本
			returnMsg = self.response["responseBody"]["returnMsg"]
			# 把获取的html文本保存到程html文件
			savehtml("bindBank", returnMsg, self.No)
			# 打开绑定银行页面
			openbindBank("bindBank", self.No)
		except Exception:
			self.errorDesc = self.response["errorDesc"]
			self.logger.error("报文返回为空！失败原因："+self.errorDesc)
			print("报文返回为空！失败原因："+self.errorDesc)

		#.check_sql()
		self.check_result()
		#self.wr_excel()

	def check_result(self):
		try:
			self.assertEqual(self.retcode, "0000", self.logger.info("检查是否绑定银行卡成功"))
			set_excel("pass", "测试结果", self.No, interfaceNo)
			self.logger.info("测试通过")
		except AssertionError:
			set_excel("fail", "测试结果", self.No, interfaceNo)
			errorDesc = self.response["errorDesc"]
			self.logger.error("测试失败:"+errorDesc)

	# 检验sql是否插入数据库中
	def check_sql(self):
		sqldb.dbname = "LC1DB"
		self.SQL = get_sql("LCDB", "wm_t_bank_info", "customerID") % self.customerID
		cursor = sqldb.executeSQL(self.SQL)
		try:
			self.res = sqldb.get_one(cursor)
			#bindtxt = str(self.res[17])
		except Exception:
			print("SQL查询结果为空！")
			self.logger.exception("SQL查询结果为空！")
		sqldb.closeDB()

	# 写入xls文件中
	def wr_excel(self):
		set_excel(self.data, "请求报文", self.No, interfaceNo)
		set_excel(self.custCode, "custCode", self.No, interfaceNo)
		set_excel(self.customerID, "customerID", self.No, interfaceNo)
		set_excel(self.cardNo, "cardNo", self.No, interfaceNo)
		set_excel(self.mobile, "bankMobile", self.No, interfaceNo)
		set_excel(self.bankAcctName, "bankAcctName", self.No, interfaceNo)
		set_excel(self.bankAcctNo, "bankAcctNo", self.No, interfaceNo)
		set_excel(self.bankCode, "bankCode", self.No, interfaceNo)

	def tearDown(self):
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)

if __name__ == '__main__':
	unittest.main()

