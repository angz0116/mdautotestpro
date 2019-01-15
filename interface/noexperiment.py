# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
import datetime

#非试点A，试点B
interfaceNo = "试点B"
name = "获取还款计划接口"

req = ConfigHttp()
sqldb = ConfigDB()
# 根据接口类型判断应该写入哪个sheet页
if interfaceNo == "非试点A":
	setmonthlv = "monthRateA"
	setplan = "非A-还款计划"
	# 算法方式,非试点-AC10105，试点-AC10104
	interestType = "AC10105"
	cooperate = "02"
else:
	setmonthlv = "monthRateB"
	setplan = "试B-还款计划"
	# 算法方式,非试点-AC10105，试点-AC10104
	interestType = "AC10104"
	# 算法编码
	cooperate = "02"
@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class test_noexperiment(unittest.TestCase):
	def setParameters(self, No, 测试结果, 请求报文, 返回报文, 产品名称prodName, 期数period,月还款金额, 合同金额approveMoney, 原放款金额loanAmount, 服务费serviceFee,
					  信用保证金lenderGuaranteeFund, 咨询服务费consultingFee,信用审核费auditFee, 信用管理费managementFee,担保费assureFee, 到手金额, 实际到手金额loanAmount,
					  抵用金额dyAmount,开始抵用期数dyPeriod, 基础保费,保费费率fixRate,保费totalinsuranceFee  ):
		self.No = str(No)
		self.prodName = str(产品名称prodName)
		self.period = str(期数period)
		self.monthAmount = str(月还款金额)
		self.approveMoney = str(合同金额approveMoney)
		self.oldloanAmount = str(原放款金额loanAmount)
		self.serviceFee = str(服务费serviceFee)
		self.lenderGuaranteeFund = str(信用保证金lenderGuaranteeFund)
		self.consultingFee = str(咨询服务费consultingFee)
		self.auditFee = str(信用审核费auditFee)
		self.managementFee = str(信用管理费managementFee)
		self.assureFee = str(担保费assureFee)
		self.dsAmount = str(到手金额)
		self.loanAmount = str(实际到手金额loanAmount)
		self.dyAmount = str(抵用金额dyAmount)
		self.dyPeriod = str(开始抵用期数dyPeriod)
		self.jcFee = str(基础保费)
		self.fixRate = str(保费费率fixRate)
		self.insuranceFee = str(保费totalinsuranceFee)

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
			#返回报文
			self.responsebody = self.response["responseBody"]
			#月还款金额
			#self.monthAmount = periodMoney
			self.approveMoney = self.responsebody["approveMoney"]
			#服务费==合同金额*月服务费率*期限-月还
			self.serviceFee = self.responsebody["serviceFee"]
			# 为什么得到的信用保证金为0？？？？？？
			#self.lenderGuaranteeFund = self.responsebody["lenderGuaranteeFund"]
			self.consultingFee = self.responsebody["consultingFee"]
			self.auditFee = self.responsebody["auditFee"]
			self.assureFee = self.responsebody["assureFee"]
			#实际到手金额（扣保费）=到手金额-保费
			self.loanAmount = self.responsebody["loanAmount"]
			self.dyAmount = self.responsebody["dyAmount"]
			self.dyPeriod = self.responsebody["dyPeriod"]
			self.jcFee = 0
			self.fixRate = self.responsebody["fixRate"]
			# 保费
			self.insuranceFee = self.responsebody["insuranceFee"]
			self.plans = self.responsebody["plans"]
		except Exception:
			self.logger.error("报文返回为空！")
			print("报文返回为空！")

		self.check_result()
		self.wr_excel()

	def check_result(self):
		try:
			#self.assertEqual(self.retcode, "0000", self.logger.info("检查是否生成月利率"))
			#set_excel("pass", "测试结果", self.No, interfaceNo)
			self.logger.info("测试通过")
		except AssertionError:
			set_excel("fail", "测试结果", self.No, interfaceNo)
			errorDesc = self.response["errorDesc"]
			self.logger.error("测试失败:"+errorDesc)
	# 写入xls文件中
	def wr_excel(self):
		#set_excel(self.data, "请求报文", self.No, interfaceNo)
		#set_excel(self.response, "返回报文", self.No, interfaceNo)
		self.prodName = get_excel("prodName", self.No, setmonthlv)
		set_excel(self.prodName, "产品名称prodName", self.No, interfaceNo)
		set_excel(self.period, "期数period", self.No, interfaceNo)
		set_excel(self.approveMoney, "合同金额approveMoney", self.No, interfaceNo)
		set_excel(self.serviceFee, "服务费serviceFee", self.No, interfaceNo)
		set_excel(self.consultingFee, "咨询服务费consultingFee", self.No, interfaceNo)
		set_excel(self.auditFee, "信用审核费auditFee", self.No, interfaceNo)
		set_excel(self.assureFee, "担保费assureFee", self.No, interfaceNo)
		set_excel(self.loanAmount, "实际到手金额loanAmount", self.No, interfaceNo)
		set_excel(self.dyAmount, "抵用金额dyAmount", self.No, interfaceNo)
		set_excel(self.dyPeriod, "开始抵用期数dyPeriod", self.No, interfaceNo)
		set_excel(self.jcFee, "基础保费", self.No, interfaceNo)
		set_excel(self.fixRate, "保费费率fixRate", self.No, interfaceNo)
		set_excel(self.insuranceFee, "保费totalinsuranceFee", self.No, interfaceNo)
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
		#试点与非试点，当金额，分位为 奇数项时，5入，当分位为 偶数项时，6入，5舍
		# 原放款金额=合同金额-服务费
		self.oldloanAmount = round(float(self.approveMoney) - float(self.serviceFee),2)
		if interfaceNo == "非试点A":
			# 到手金额 =原放款金额-月还
			self.dsAmount = round(self.oldloanAmount - float(self.periodMoney),2)
			# 信息管理费=月还（信用保证金）
			self.managementFee = self.periodMoney
		else:
			# 到手金额 = 原放款金额
			self.dsAmount = self.oldloanAmount
			# 信息管理费 = 0
			self.managementFee = 0
		# 信用保证金，月还款金额=信用保证金
		self.lenderGuaranteeFund = self.periodMoney
		# 需要获取月还款金额，固放在最下面得到该值，信用管理费，信用保证金，到手金额
		set_excel(self.oldloanAmount, "原放款金额loanAmount", self.No, interfaceNo)
		set_excel(self.periodMoney, "月还款金额", self.No, interfaceNo)
		set_excel(self.managementFee, "信用管理费managementFee", self.No, interfaceNo)
		set_excel(self.lenderGuaranteeFund, "信用保证金lenderGuaranteeFund", self.No, interfaceNo)
		set_excel(self.dsAmount, "到手金额", self.No, interfaceNo)

	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
	unittest.main()
