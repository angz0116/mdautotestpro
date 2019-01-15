# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
import datetime

#向上非6%
interfaceNo = "向上非6%"
name = "获取还款计划接口"

req = ConfigHttp()
sqldb = ConfigDB()
# 根据接口类型判断应该写入哪个sheet页
if interfaceNo == "向上非6%":
	setmonthlv = "monthRateB"
	setplan = "向上非6%-还款计划"
	# 算法方式,向上非6%
	interestType = "AC10124"
	# 算法编码
	cooperate = "XS"
else:
	cooperate = "XQ"
@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class test_noexperiment(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, 产品名称, 期数,月还款金额, 合同金额, 原放款金额, 服务费,
					  信用保证金, 向上平台服务费, 到手金额, 实际到手金额,抵用金额,开始抵用期数,保费):
		self.No = str(No)
		self.prodName = str(产品名称)
		self.period = str(期数)
		self.monthAmount = str(月还款金额)
		self.approveMoney = str(合同金额)
		self.oldloanAmount = str(原放款金额)
		self.serviceFee = str(服务费)
		self.lenderGuaranteeFund = str(信用保证金)
		self.xxserviceFee = str(向上平台服务费)
		self.dsAmount = str(到手金额)
		self.loanAmount = str(实际到手金额)
		self.dyAmount = str(抵用金额)
		self.dyPeriod = str(开始抵用期数)
		self.insuranceFee = str(保费)

	def setUp(self):
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
		print(interfaceNo + name + "CASE " + self.No)

	def test_body(self):
		self.url = "/masterdata/api/contract/repaymentPlan/search/v1"
		headers = {"Content-Type": "application/json"}
		# 获取当前时间
		now = datetime.datetime.now()
		# 请求
		self.loanDate = now.strftime('%Y-%m-%d %H:%M:%S')
		# 获取月服务费率接口中的monthlyOverallRate
		#综合费率
		self.monthlyOverallRate = get_excel("monthlyOverallRate", self.No, setmonthlv)
		# 月利率
		self.interestRate = get_excel("interestRate", self.No, setmonthlv)
		# 贷款期数
		self.period = get_excel("period", self.No, setmonthlv)
		# 审批金额
		self.approveMoney = get_excel("approveMoney", self.No, setmonthlv)
		# 月利率
		self.monthRate = get_excel("monthRate", self.No, setmonthlv)
		self.data = {
				"monthRate": self.monthRate,
				"monthlyOverallRate":self.monthlyOverallRate,
				"opSystem": "S001",
				"costCode": "F001",#费用编码
				"urgentRate": "0",#加急费率
				"interestRate": self.interestRate,
				"period": self.period,
				"interestType": interestType,
				"cooperate": cooperate,
				"approveMoney": self.approveMoney,
				"loanDateCalculation": "A10116", #还款日计算方式
				"loanDate": self.loanDate,
				"insuranceRate": "0" #保险费率
			}
		print(self.data)
		req.httpname = "MDJC3"
		req.set_url(self.url)
		req.set_headers(headers)
		req.set_data(self.data)
		self.response = req.post()
		try:
			print(self.response)
			# 返回报文
			self.responsebody = self.response["responseBody"]
			# 合同金额
			self.approveMoney = self.responsebody["approveMoney"]
			#服务费==合同金额*月服务费率*期限-月还
			self.serviceFee = self.responsebody["serviceFee"]
			# 向上平台服务费
			self.xxserviceFee = self.responsebody["serviceFee"]
			# 实际到手金额（扣保费）=到手金额-保费
			self.loanAmount = self.responsebody["loanAmount"]
			# 抵用金额
			self.dyAmount = self.responsebody["dyAmount"]
			# 开始抵用期数
			self.dyPeriod = self.responsebody["dyPeriod"]
			# 还款计划列表
			self.plans = self.responsebody["plans"]
		except Exception:
			self.logger.error("报文返回为空！")
			print("报文返回为空！")

		self.check_result()
		self.wr_excel()

	def check_result(self):
		try:
			self.logger.info("测试通过")
		except AssertionError:
			set_excel("fail", "测试结果", self.No, interfaceNo)
			errorDesc = self.response["errorDesc"]
			self.logger.error("测试失败:"+errorDesc)
	# 写入xls文件中
	def wr_excel(self):
		self.prodName = get_excel("prodName", self.No, setmonthlv)
		set_excel(self.prodName, "产品名称", self.No, interfaceNo)
		set_excel(self.period, "期数", self.No, interfaceNo)
		set_excel(self.approveMoney, "合同金额", self.No, interfaceNo)
		set_excel(self.serviceFee, "服务费", self.No, interfaceNo)
		set_excel(self.xxserviceFee, "向上平台服务费", self.No, interfaceNo)
		set_excel(self.loanAmount, "实际到手金额", self.No, interfaceNo)
		set_excel(self.dyAmount, "抵用金额", self.No, interfaceNo)
		set_excel(self.dyPeriod, "开始抵用期数", self.No, interfaceNo)

		#还款计划大于0时
		if len(self.plans)>0:
			#循环得到每一个还款计划信息
			for i in range(len(self.plans)):
				#期数
				persiod = i+1
				#应还日期
				repaymentDate = self.plans[i]["repaymentDate"]
				#月还本金
				principalMoney = self.plans[i]["principalMoney"]
				#月还利息
				periodInterestMoney = self.plans[i]["periodInterestMoney"]
				#月还款额
				self.periodMoney = self.plans[i]["periodMoney"]
				#借款余额
				surplusMoney = self.plans[i]["surplusMoney"]
				#提前结清退还服务费
				refundServiceFee =  self.plans[i]["refundServiceFee"]
				#提前还款应还款总额
				refundTotal = self.plans[i]["refundTotal"]
				set_excel(persiod, "期数", persiod, setplan)
				set_excel(repaymentDate, "应还日期", persiod, setplan)
				set_excel(principalMoney, "月还本金", persiod, setplan)
				set_excel(periodInterestMoney, "月还利息", persiod, setplan)
				set_excel(self.periodMoney, "月还款额", persiod, setplan)
				set_excel(surplusMoney, "借款余额", persiod, setplan)
				set_excel(refundServiceFee, "提前结清退还服务费", persiod, setplan)
				set_excel(refundTotal, "提前还款应还款总额", persiod, setplan)
		# 原放款金额=合同金额-服务费
		self.oldloanAmount = round(float(self.approveMoney) - float(self.serviceFee), 2)
		# 信用保证金，月还款金额=信用保证金
		self.lenderGuaranteeFund = self.periodMoney
		# 到手金额 = 原放款金额 - 信用保证金
		self.dsAmount = round(self.oldloanAmount - float(self.lenderGuaranteeFund), 2)
		# 保费 = 到手金额 - 实际到手金额
		self.insuranceFee = round(self.dsAmount - float(self.loanAmount), 2)
		# 需要获取月还款金额，固放在最下面得到该值，信用管理费，信用保证金，到手金额
		set_excel(self.periodMoney, "月还款金额", self.No, interfaceNo)
		set_excel(self.oldloanAmount, "原放款金额", self.No, interfaceNo)
		set_excel(self.lenderGuaranteeFund, "信用保证金", self.No, interfaceNo)
		set_excel(self.dsAmount, "到手金额", self.No, interfaceNo)
		set_excel(self.insuranceFee, "保费", self.No, interfaceNo)

	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
	unittest.main()
