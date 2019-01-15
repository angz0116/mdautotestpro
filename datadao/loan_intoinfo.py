# -*- coding:utf-8 -*-
from utils.baseDB import ConfigDB
from utils.baseUtils import *
import datetime
sqldb = ConfigDB()
No = 1
interfaceNo = "loanopenbank"
'''
贷款-根据身份ID查询客户信息与进件信息，写入excel中，用于客户绑卡开户
'''
class custIntoInfo():
	'''
	根据身份证Id查询贷款信息
	'''
	def query_sql(self, cardNo):
		sqldb.dbname = "LOANL3DB"

		self.SQL = get_sql("LOANDB", "lb_t_customter_info", "cardId") % (cardNo)

		cursor = sqldb.executeSQL(self.SQL)
		try:
			self.res = sqldb.get_all(cursor)
			#查询到空，则不进行插入excle中
			if(len(self.res)!=0):
				self.intoAppId = self.res[0][6]
				self.wr_excel(self.res)
			else:
				print("未查询到贷款进件信息")
		except Exception:
			print("SQL查询结果为空！")
			#self.logger.exception("SQL查询结果为空！")
		sqldb.closeDB()
		return self.intoAppId

	# 把查询出的数据信息写入excle中
	def wr_excel(self, data):
		self.bankAcctName = data[0][0]
		self.cardId = data[0][1]
		self.mobile = data[0][2]
		self.bankCode = data[0][3]
		self.bankAcctNo = data[0][4]
		self.custCode = data[0][5]
		self.intoAppId = data[0][6]
		set_excel(data, "测试结果", No, interfaceNo)
		set_excel(self.bankAcctName, "custName", No, interfaceNo)
		set_excel(self.cardId, "cardNo", No, interfaceNo)
		set_excel(self.mobile, "bankMobile", No, interfaceNo)
		set_excel(self.bankCode, "bankCode", No, interfaceNo)
		set_excel(self.bankAcctNo, "bankAcctNo", No, interfaceNo)
		set_excel(self.custCode, "custCode", No, interfaceNo)
		set_excel(self.intoAppId, "intoAppId", No, interfaceNo)

if __name__== '__main__':
	custinfo = custIntoInfo()
	#custinfo.query_sql()