# -*- coding:utf-8 -*-
from utils.baseBrowser import BaseBrowser
from webapp.comlogin import test_comLogin
from selenium.webdriver.support.select import Select
from service.gainName import getFullName
from service.districtcode import gennerator
from service.gainPhone import createPhone,telePhone
from service.gainBank import getCCBbankCardNo
import time, os, datetime, unittest
from datadao.loan_intoinfo import custIntoInfo
from service.pageObject import PageObject
from service.loandict import loancode
from service.myglobal import set_value
from utils.baseLog import MyLog as Log
log = Log.get_log()
logger = log.logger

'''
第一步，进件管理-进件申请菜单，操作员11047165，杨元奇
'''
class test_incomApply(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		# 必须使用@classmethod 装饰器,所有test运行前运行一次
		# 得到driver实例
		self.driver = BaseBrowser.getDriver()
		# 初始化页面元素
		self.base = PageObject(self.driver)
		# 生成身份证号
		self.cardId = gennerator()
		# 隐性等待，设置了一个时间，在一段时间内网页是否加载完成，如果完成了，就进行下一步；在设置的时间内没有加载完成，则会报超时加载；等待30s，强制等待time.sleep(3)
		#self.driver.implicitly_wait(30)
		logger.info("第一步************************incomapply.py，进件管理-进件申请，11047165，杨元奇")
	'''
	登录，及打开菜单
	'''
	def openmenu(self):
		# 进入“借款系统”,与哪个环境
		httpname = "LOANJC3"
		systemname = "loan"
		# 根据用户名，密码，登录方法
		test_comLogin.test_login(self.driver, "11038360", "Cs654321", httpname, systemname)
		#self.driver.find_element_by_xpath("//*[@id='firstMenu0']").click()
		# 点击“进件申请菜单”
		self.base.click(("id,firstMenu3"))
		# 点击进入“进件申请”页面
		self.base.click(("xpath,//span[text()=' 进件申请']"))

	'''
	点“新增”按钮，进件申请方法
	'''
	def test_incompartapply(self):
		try:
			#调用“登录”方法
			self.openmenu()
			aflag = self.addicomapply()
			if aflag == True:
				# 调用根据身份证好，查询客户信息与进件信息，写入excle中
				self.intoappId = custIntoInfo().query_sql(self.cardId)
			#调用“上传附件”按钮的方法
			self.uploadattach(self.intoappId)
			#调用“提交”按钮的方法
			self.submitInfo(self.intoappId)
		except Exception as err:
			logger.info("新增进件申请错误信息：")
			logger.error(err)
	'''
	点击“新增”按钮，弹出页面
	'''
	def addicomapply(self):
		try:
			flag = True
			# 进入“进件申请”页面的iframe
			self.base.switchFrame(("iframe,queryLbTIntoInfo"))
			BaseBrowser.get_window_img(self.driver, "incoming")
			# 点“新增”按钮，进入<新增进件信息>页面
			self.base.click(("link_text,新 增"))
			# 退出“进件申请” 页面
			self.base.switchFramedefault()
			# 进入“新增进件”页面的iframe
			self.base.switchFrame(("iframe,addLbTIntoInfo"))
			self.base.send_keys(("id,cardId"), self.cardId)
			# 获取客户姓名
			self.custName = getFullName()
			self.base.send_keys(("id,custName"), self.custName)
			# 项目类型“信贷产品”
			self.base.selectByValue(("id,prodType"), "01")
			# 产品名称
			self.base.selectByValue(("id,prodCode"), loancode["优悦贷A"] + ":4")
			# 信息审核员
			self.base.send_keys(("id,undefined_"), "王鹏丽")
			# 点“确定”按钮，提交，进入下一个页面
			self.base.click(("id,ok"))
			# 调用“新增进件申请”页面
			self.addincom()
			# 退出“新增进件”页面
			self.base.switchFramedefault()
		except Exception as err:
			flag = False
			logger.info("点击“新增”按钮后，保存报错")
			logger.error(err)
		return flag

	'''
	新增进件申请完整信息
	'''
	def addincom(self):
		try:
			'''
			客户借款需求,implicitly_wait() 方法可以方便的实现智能等待
			'''
			time.sleep(5)
			# 家人是否知晓
			Select(self.driver.find_element_by_id("dtofamilyIsKnown")).select_by_value("1")
			# 借款用途
			Select(self.driver.find_element_by_id("dtoloanPrePurpose")).select_by_value("102")
			time.sleep(1)
			Select(self.driver.find_element_by_id("dtoloanPurpose")).select_by_value("13")
			# 申请借款金额
			self.driver.find_element_by_id("dtominAppAmount").send_keys("100000")
			# 月还款能力
			self.driver.find_element_by_id("dtomonthPayment").send_keys("10000")
			# 申请期限
			Select(self.driver.find_element_by_id("dtoapplyPeriod")).select_by_value("36")
			# 申请渠道
			Select(self.driver.find_element_by_id("dtocustomerChannel")).select_by_value("0")
			'''
			客户基本信息
			'''
			# 民族
			self.driver.find_element_by_id("dtonation").send_keys("汉族")
			# 户籍详细地址
			Select(self.driver.find_element_by_id("phometownAreacode")).select_by_value("110000")
			Select(self.driver.find_element_by_id("chometownAreacode")).select_by_value("110100")
			Select(self.driver.find_element_by_id("dtohometownAreacode")).select_by_value("110101")
			self.driver.find_element_by_id("dtohometownAddr").send_keys("北京市东城区银河SOHOD座")
			# 最高学历,选中“本科”
			Select(self.driver.find_element_by_id("dtohDegree")).select_by_value("2")
			# 婚姻状态，选中已婚
			Select(self.driver.find_element_by_id("dtomarrStatus")).select_by_value("2")
			# 有无子女
			Select(self.driver.find_element_by_id("dtohasChild")).select_by_value("0")
			# 您来本市的年份
			self.driver.find_element_by_id("dtoinCityYear").send_keys("2009")
			# 移动电话
			phone = createPhone()
			self.driver.find_element_by_id("dtomobilePhone").send_keys(phone)
			# 有无住宅电话
			Select(self.driver.find_element_by_id("dtohasTelephone")).select_by_value("0")
			# 电子邮件
			self.driver.find_element_by_id("dtoemail").send_keys(phone + "@139.com")
			# 现住址
			Select(self.driver.find_element_by_id("pcurrentAreacode")).select_by_value("110000")
			Select(self.driver.find_element_by_id("ccurrentAreacode")).select_by_value("110100")
			Select(self.driver.find_element_by_id("dtocurrentAreacode")).select_by_value("110102")
			self.driver.find_element_by_id("dtocurrentAddr").send_keys("北京市西城区西四胡同")
			# 住宅类型
			Select(self.driver.find_element_by_id("dtohomeType")).select_by_value("1")
			# 税后月均总收入(元)
			self.driver.find_element_by_id("dtoafterTaxMonthlyIncome").send_keys("20000")
			# 客户来源
			Select(self.driver.find_element_by_id("dtocustomerSource")).select_by_value("9")
			# 调用“个人授权信息，上传文件”方法
			self.uploadfile()
			# 调用“客户工作信息”方法
			self.customerInfo()
			# 调用“联系人信息”方法
			self.linkmanInfo(2)
			# 调用“银行卡信息”方法
			self.bankcardInfo(phone)
			# 调用“流水负债信息”方法
			self.incurdebtsInfo()
			time.sleep(3)
			# 保存
			self.driver.find_element_by_id("doAddInto").click()
		except Exception as err:
			logger.error(err)
	'''
	个人授权信息，上传文件
	'''
	def uploadfile(self):
		try:
			# 人行征信， 账号
			self.driver.find_element_by_id("dtoaccount").send_keys("1010")
			# 密码
			self.driver.find_element_by_id("dtopassword").send_keys("101010")
			# 提取验证码
			self.driver.find_element_by_id("dtocaptcha").send_keys("100000")
			# 上传PDF并解析，弹出“上传PDF并解析”页面
			self.driver.find_element_by_id("pdf_andAnalyze").click()
			# 在该弹出页面中，点“浏览”按钮
			time.sleep(3)
			self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[contains(@src,'toUploadFile')]"))
			self.driver.find_element_by_id("SWFUpload_0").click()
			time.sleep(3)
			# 获取文件路径
			proDir = os.path.split(os.getcwd())[0] + "\\webapp\\uploadfileonly.exe"
			# 调用上传文件exe,可执行程序，基于Autolt实现上传的方法
			os.system(proDir)
			# 退出“上传”页面
			self.driver.switch_to.default_content()
			time.sleep(3)
			self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[contains(@src,'addLbTIntoInfo')]"))
			while 1:
				start = time.clock()
				try:
					self.driver.find_element_by_xpath("//span[text()='解析并关闭']").click()
					print("已定位到元素")
					end = time.clock()
					break
				except:
					print("还未定位到元素!")
				print('定位耗费时间：' + str(end - start))
		except Exception as err:
			logger.info("个人授权信息，上传附件错误信息：")
			logger.error(err)
	'''
	客户工作信息
	'''
	def customerInfo(self):
		#工作单位全称
		self.driver.find_element_by_id("dtojName").send_keys("北京市东城区中粮")
		#单位电话,座机电话
		telphone = telePhone()
		self.driver.find_element_by_id("dtojPhoneAreaCode").send_keys("010")
		self.driver.find_element_by_id("dtojPhone").send_keys(telphone)
		#工作单位地址
		Select(self.driver.find_element_by_id("pjAddrAreacode")).select_by_value("110000")
		Select(self.driver.find_element_by_id("cjAddrAreacode")).select_by_value("110100")
		Select(self.driver.find_element_by_id("dtojAddrAreacode")).select_by_value("110101")
		self.driver.find_element_by_id("dtojAddr").send_keys("北京市东城区中粮广场C座")
		#担任职务
		Select(self.driver.find_element_by_id("dtojPosition")).select_by_value("3")
		time.sleep(3)
		#进入该单位时间
		jEnterT = (datetime.datetime.now() + datetime.timedelta(days=-365)).strftime("%Y-%m-%d %H:%M:%S")
		self.driver.find_element_by_id("dtojEnterT").send_keys(jEnterT)
		#单位性质
		Select(self.driver.find_element_by_id("dtojType")).select_by_value("3")
		#工资发放形式
		Select(self.driver.find_element_by_id("dtojPayType")).select_by_value("1")
	'''
	联系人信息
	'''
	def linkmanInfo(self, lnumber):
		#for循环得到“家庭联系人”，“紧急联系人”
		for i in range(lnumber):
			#点“新建”按钮弹出“联系人-新增”页面
			self.driver.find_element_by_xpath("//*[@id='contact_info']/div/a[text()='新建']").click()
			time.sleep(3)
			if i==0:
				#联系类型，“家庭联系人”
				Select(self.driver.find_element_by_id("dtocontactType")).select_by_value("3")
				#和本人关系,母亲
				Select(self.driver.find_element_by_id("dtoconRelation")).select_by_value("4")
			else:
				# 联系类型，“紧急联系人”
				Select(self.driver.find_element_by_id("dtocontactType")).select_by_value("2")
				# 和本人关系,配偶
				Select(self.driver.find_element_by_id("dtoconRelation")).select_by_value("2")
			#姓名
			conName = getFullName()
			self.driver.find_element_by_id("dtoconName").send_keys(conName)
			#联系电话
			conPhone = createPhone()
			self.driver.find_element_by_id("dtoconPhone").send_keys(conPhone)
			#点“确定”按钮
			self.driver.find_element_by_xpath("//span[text()='确定']").click()
	'''
	银行卡信息
	'''
	def bankcardInfo(self, reservPhone):
		# 点“新建”按钮弹出“新增银行卡”页面
		self.driver.find_element_by_xpath("//*[@id='bank_card_info']/div/a[text()='新建']").click()
		time.sleep(3)
		#银行卡账号
		bankcard = getCCBbankCardNo()
		self.driver.find_element_by_id("dtobankCardAccount").send_keys(bankcard)
		#开户行名称，建设银行
		Select(self.driver.find_element_by_id("dtobankCode")).select_by_value("105")
		#开户行所在省/市
		Select(self.driver.find_element_by_id("dtobankProvAreacode")).select_by_value("110000")
		Select(self.driver.find_element_by_id("dtobankCityAreacode")).select_by_value("110100")
		#支行名称
		self.driver.find_element_by_id("dtosubBranchName").send_keys("北京市海淀区知春路建设支行")
		#银行预留手机号
		self.driver.find_element_by_id("dtobankReservedPhone").send_keys(reservPhone)
		#是否收款/放款银行卡
		Select(self.driver.find_element_by_id("dtoisLoanType")).select_by_value("1")
		# 点“保存”按钮
		self.driver.find_element_by_xpath("//span[text()='保存']").click()
	'''
	流水负债信息
	'''
	def incurdebtsInfo(self):
		self.driver.find_element_by_xpath("//a[text()='流水负债信息']").click()
		time.sleep(3)
		self.driver.find_element_by_id("dtocheMonIncome").send_keys("20000")
	'''
	点击“上传附件”按钮
	'''
	def uploadattach(self, intoappId):
		try:
			# 进入“进件申请”页面的iframe
			#self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[contains(@src,'queryLbTIntoInfo')]"))
			self.base.switchFrame(("iframe,queryLbTIntoInfo"))
			# 查询条件“进件编号”
			self.base.send_keys(("name,intoAppId"), intoappId)
			# 点击“查询”按钮，查询出数据
			self.driver.find_element_by_xpath("//span[text()='查询']").click()
			# 选中该条数据
			self.base.click(("xpath,//input[@type='radio']"))
			# 点“上传附件”按钮
			self.base.click(("link_text,上传附件"))
			# 退出“查询”的iframe
			self.base.switchFramedefault()
			# 进入“上传附件”的iframe
			self.base.switchFrame(("iframe,uploadIntoAttachment"))
			# 点击“批量上传”按钮
			self.base.click(("link_text,批量上传"))
			# 退出“上传附件”的iframe
			self.driver.switch_to.default_content()
			# 在该弹出页面中，点“浏览”按钮
			self.base.switchFrame(("iframe,batchAttachUpload"))
			# 点击“上传”按钮
			self.base.click(("id,SWFUpload_0"))
			time.sleep(3)
			# 获取文件路径
			proDir = os.path.split(os.getcwd())[0] + "\\webapp\\uploadfilebatch.exe"
			# 调用上传文件exe,可执行程序，基于Autolt实现上传的方法
			os.system(proDir)
			time.sleep(15)
			# 退出“批量附件上传”iframe页面
			self.base.switchFramedefault()
			# 系统消息的“关闭”框
			self.base.click(("xpath,//div[@class='ui-widget-content sysMessage']/div[2]/a"))
			# 点“关闭”按钮，关闭批量附件上传页面
			self.base.click(("class,ui_state_highlight"))
			# 再次进入"上传附件"iframe关闭此页面
			self.base.switchFrame(("iframe,uploadIntoAttachment"))
			#点击“关闭”按钮
			self.base.click(("id,doCloseInto"))
			#清空“进件编号”查询条件
			#self.base.clear(("name,intoAppId"))
			# 退出“上传附件”的iframe
			self.base.switchFramedefault()
		except Exception as err:
			logger.info("批量上传附件错误信息：")
			logger.error(err)
	'''
	点击“提交”按钮
	'''
	def submitInfo(self, intoappId):
		try:
			flag = True
			# 进入“进件申请查询”iframe页面
			self.base.switchFrame(("iframe,queryLbTIntoInfo"))
			# 查询条件“进件编号”
			#self.base.send_keys(("name,intoAppId"), intoappId)
			# 点击“查询”按钮查询数据
			self.driver.find_element_by_xpath("//span[text()='查询']").click()
			# 点击选中的数据
			self.base.click(("xpath,//input[@type='radio']"))
			#获取进件编号,设置全局变量
			set_value(intoappId)
			logger.info("进件申请-进件编号-全局变量："+intoappId)
			#点“提交”按钮，提交
			self.base.click(("link_text,提 交"))
			# 审核意见
			self.base.send_keys(("id,dtoremark"), "同意")
			# 点击“系统提示框”关闭按钮
			self.base.click(("xpath,//div[@class='ui-dialog-buttonset']/button[1]/span"))
			# 退出“进件申请查询”iframe页面
			self.base.switchFramedefault()
		except Exception as err:
			flag = False
			logger.info("提交进件申请错误信息：")
			logger.error(err)
		return flag

	@classmethod
	def tearDownClass(self):
		#必须使用 @ classmethod装饰器, 所有test运行完后运行一次
		BaseBrowser.quit_browser(self.driver)
if __name__=='__main__':
	unittest.main()