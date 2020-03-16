import urllib.parse
import json
import hashlib
from app.system import internal_function
import sys
#import pycurl
import requests
import certifi
from io import BytesIO
from django.http import HttpRequest as request_django # remove soon testing mode
from django.db import connection
#import request # remove soon testing mode
import os
import time
import datetime
import math
import MySQLdb
from flask import jsonify, render_template, redirect,flash, request, url_for
import re
from app.models import SqlModel
from django_redis import get_redis_connection
from django.core.cache import cache
is_array = lambda var: isinstance(var, (list, tuple)) 
global _CFG
from app.system import config_parse as configdata
_CFG = configdata.config['_CFG']
g_conf = configdata.config['_CFG']


class Movies:

	CacheFile = ''
	#CacheTime = 3600
	CacheTime = 60
	CasheEnabled = True
	API = ""

	def __init__(self, request, api, mode):
		
	  self.API = api

	  	
	  data = {}
	  data['u'] = self.API.user
	  data['p'] = self.API.password
	  data['e'] = self.API.date_expire
	  data['mode'] = mode
	  data['parent'] = self.API.catid
	  data['catid'] = self.API.catid
	  data['movie_id'] = self.API.movie_id
	  data['series_id'] = self.API.series_id
	  data['search'] = self.API.search
	  data['year'] = self.API.year
	  data['genre'] = self.API.genre
	  
	  self.SetCacheFile(data)
	  
	  #rating
	  cutomData =  {}
	  cutomData['group'] = self.API.DBgroup
	  cutomData['islam_pkg'] = self.API.islam_pkg
	  cutomData['islam_pkg_mov'] = self.API.conf['islam_pkg_mov'].strip()
	  cutomData['islam_pkg_series'] = self.API.conf['islam_pkg_series'].strip()
	  cutomData['ratingPoints'] = request.GET.get('ratingPoints', False)  if  request.GET.get('ratingPoints', False).strip()  else "" 
	  cutomData['code'] = self.API.code
	  cutomData['series_id'] = data['series_id']
	  cutomData['movie_id'] = data['movie_id']
	  cutomData['ip'] = self.API.ip()
	  	  
	  cutomData['title'] = request.GET.get('title', False)  if  request.GET.get('title', False).strip()  else "" 	
	 
	 
	 
	  if cutomData['title'] != "":
		 
		   cutomData['title'] = urllib.parse.quote(cutomData['title'])
	
	
	  cutomData['comment'] = request.GET.get('comment', False)  if  request.GET.get('comment', False).strip()  else "" 		
	  cutomData['name'] = request.GET.get('name', False)  if  request.GET.get('name', False).strip()  else "" 	
	  cutomData['for'] = request.GET.get('for', False)  if  request.GET.get('for', False).strip()  else "" 	
	  cutomData['op'] = request.GET.get('op', False)  if  request.GET.get('op', False).strip()  else "" 	
	 
	
	  data['data'] = json.dumps(cutomData)
	  data['url'] = self.API.conf['remote_movies_url'].strip().replace("|", "/")

	  url = self.API.conf['remote_movies_api'].strip().replace("|", "/")
	  #Json = self.intro_url(url,data)
	  print ( self.intro_url(url , data))

	def  SetCacheFile(self,data):
		self.CacheFile += "./cache/"
		self.CacheFile += "vod_["
		self.CacheFile += data['mode']+"]_"
		if data['catid'] != "": 
			self.CacheFile += "CatID"+data['catid']+"_"
		if data['mode'] == "series_details" and int(data['series_id']) != 0:
			self.CacheFile += "SeriesID"+data['series_id']+"_"
		if data['mode'] == "movies_info" and int(data['movie_id']) != 0:
			self.CacheFile += "MovieID"+data['movie_id']+"_"
		self.CacheFile += internal_function.md5(self.CacheFile+"rareMicra")+".txt"


	
	def intro_curl_url(self,url , data = ""):
		return None
# 		if 'curl' in sys.modules.keys():
# 			buffer = BytesIO()
# 			c = pycurl.Curl()
# 			c.setopt(c.URL, url)
# 			c.setopt(c.WRITEDATA, buffer)
# 			c.perform()
# 			c.close()
# 			body = buffer.getvalue()

			
# 			return body.decode('utf-8')
# #
# ##			
# 		else:
# 			sys.exit('need Curl module')

	def intro_url(self,url,data = []):
		if self.CasheEnabled == True:
			if 	os.path.exists(self.CacheFile) and os.path.getsize(self.CacheFile) > 0 :
				if (int(time.time())- os.path.getctime(self.CacheFile)):
					internal_function.file_get_contents(self.CacheFile)
		output = self.intro_curl_url(url , data)
		
		if re.search("/error:/i", output):
			self.API.insert("maa_logs_sys"),{
  				 'dtime' : internal_function.date(time.time(), "%Y-%m-%d %H:%M:%S"),
  				 'admin_user'   : 'movies_api',
   				 'app': 'movies_api',
   				 'ip': self.API.ip(),
  				 'action'  : 'error',
				 'the_log' : output		  }
		output = self.API.runXOR(output)
		if self.CasheEnabled == True:
			f = open(self.CacheFile, 'w')
			f.write(output)
			f.close()
			#os.unlink(self.CacheFile)
		return output

class API6Core:


	CatOrder = " `category_name` ASC"
	mac = ""
	sn = ""
	chipid = ""
	code = ""
	ip = ""
	conf = g_conf
	free_codes = {}
	mastercodes = {}
	bouquets = None
	link = None
	mac_enable = True
	inputBy = 0
	free = {101,103,107,110}
	user = ""
	password = ""
	date_expire = ""
	limit = 0
	limit_qry = ""
	ost = ""
	debug = 0
	transid = 0
	cache = True
	cache_type = 'FILE'
	cache_time = 60
	catid = ''
	movie_id = 0
	series_id = 0
	code_id = 0
	reply = ''
	raw = ''
	model = ''
	firmware_ver =''
	iptv_stream_host =''
	output ='ts'
	#unset yet
	DBgroup =0
	islam_pkg = 0
	parent_id =0
	pkg_id =0
	genre =''
	year = ''
	search=''
	portal_ul=''
	portal_name='PortalNotSet in cfg'
	prefix = 'maa'
	osd = ''


	

	def insertIP(self):
		file = os.path.basename(__file__)
		SqlModel.objects.raw("insert into " + self.prefix + "_ips (ip,file,type) " + 
			"VALUES('{}','{}',1) ON ON DUPLICATE KEY UPDATE hits=hits+1;".format(self.ip, file))
		return None
			

	def _die(self, msg):
		return self.runXOR(msg)




	def getCache(self,file):
		file = "cache/" + file
		cache_time = 60*10
		if not os.path.isfile(file):
			return None
		if(internal_function.file_mtime(file) < time.time() - cache_time): return None
		data = internal_function.file_get_contents(file)

	
	
	def setCache(self,content,file):
		file = "/cache" + file
		internal_function.file_write(file, content)

	

	def getMasterCodes(self):
		results = SqlModel.objects.raw("SELECT * From maa_codes_master;")
		for row in results:
			code = row.master_code.strip()
			inputBy = int(row.master_by)
			self.MasterCodes[code] = inputBy


	def insertModel(self):
		now = internal_function.date(time.time(), "%Y-%m-%d %H:%M:%S")
		if self.model != "":
			SqlModel.objects.raw("INSERT INTO " + self.prefix + "_model " + "(m_name, m_ver, codeid, hits " 
				+ "VALUES('{}','{}','{}',1)".format(self.model, self.firmware_ver, self.code_id) 
				+ " ON DUPLICATE KEY UPDATE hits=hits+1,lastdate='{}';".format(now))


	def proccess_free_code(self,code,sn,mac,ip):
		qry = ''
		sqlFC = SqlModel.objects.raw("Select * From maa_free_code where code='{}'".format(code))
		rowFC = sqlFC[0]
		if int(sqlFC.status) == 0:
			arrayset = {"status":3, "message":"Sorry: Our Free Code ($code) Available from Monday To Wednesday.", 
			"expire":"", "username":"", "password":""}
			self.msg(arrayset)
		days = int(rowFC.days)
		if days == 0:
			days = 1
		forced_country = rowFC.forced_country
		if self.mac_enable:
			qry = " AND c.mac='{}'".format(mac)

		#CHECK IF DVB EXISTES
		sql_code = SqlModel.objects.raw("SELECT c.code, c.date_expire, c.status, u.username, u.password FROM maa_codes_free c, users u " 
			+ "WHERE c.user=u.username AND c.code='{}' AND c.serial='{}' {}".format(code, sn, qry))
		if len(list(sql_code)) == 0:
			data['code'] = code
			data['days'] = days
			data['user'] = "free" + self.random_number(10)
			data['status'] = 1
			data['bouquets'] = '1'
			data['mac'] = mac
			data['serial'] = sn
			data['date_expire'] = time.time() + (int(data['days']) * 60 * 60 *24)
			self.insert(self.prefix + "_code_free", data)
			dataUser['member_id'] = 1
			dataUser['username'] = data['user']
			dataUser['password'] = internal_function.uniqid()
			dataUser['exp_date'] = data['date_expire']
			dataUser['admin_notes'] = "free code"
			dataUser['admin_enabled'] = 1
			dataUser['enabled'] = 1
			dataUser['bouquet'] = '[1]'
			dataUser['max_connections'] = 1
			dataUser['created_at'] = time.time()
			dataUser['created_by'] = 1
			dataUser['is_trial'] = 1
			dataUser['forced_country'] = forced_country
			id = self.insert("user", dataUser)
			self.insert("user_output", {'user_id':id, 'access_output_id':1})
			self.insert("user_output", {'user_id':id, 'access_output_id':2})
			self.insert("user_output", {'user_id':id, 'access_output_id':3})

			SqlModel.objects.raw("UPDATE {}_free_code Set code_used=code_used+1 Where code='{}'".format(self.prefix, code))

			array = {
			"status":100, 
			"message":"The account has been activated successfully", 
			"osd":self.osd, 
			"expire":self.expire_date(data['date_expire']), 
			"user_agent":self.conf['user_agent'].strip(), 
			"code_id":0 
			}
			self.msg(array, "Free code Activated : User== {}".format(dataUser['username']))

		if len(list(sql_code)) == 1:
			row = sql_code[0]
			array = {
			"status":100,
			"message":"This account has been activated successfully",
			"osd":self.osd,
			"expire":self.expire_date(row.date_expire),
			"user_agent":self.conf['user_agent'].strip(),
			"code_id":0
			}
			self.msg(array)

	
	def proccess_master_code(self):
		qry = ''
		period = int(self.conf['mc_period'])
		if period in self.free:
			dd = period - 100
			exp_date = datetime.datetime.now() + datetime.timedelta(dd)
		else:
			exp_date = internal_function.add_months(datetime.date.today(), period)
			days = period * 30


		sql_code = SqlModel.objects.raw("Select c.code,c.date_expire,c.status,u.username,u.password From maa_codes c,users u " + 
			"WHERE c.username=u.username AND c.code='{}' AND c.serial='{}' AND c.mac='{}';".format(self.code, self.sn, self.mac))
		if len(list(sql_code)) == 0:
			data = {}
			data['code'] = self.code
			data['days'] = days
			data['period'] = period
			data['username'] = "master" + self.random_number(10)
			data['status'] = 1
			data['bouquets'] = ",".join(self.get_bouquets())
			data['mac'] = self.mac
			data['serial'] = self.sn
			data['date_expire'] = exp_date
			data['inputBy'] = 1 #1=mac, 2=serial
			self.insert(self.prefix + "_codes", data)

			##Insert user in Extream
			dataUser = {}
			dataUser['member_id'] = 1
			dataUser['username'] = data['username']
			dataUser['password'] = internal_function.uniqid()
			dataUser['exp_date'] = exp_date
			dataUser['admin_notes'] = "from master code"
			dataUser['admin_enabled'] = 1
			dataUser['enabled'] = 1
			dataUser['bouquet'] = data['bouquets']
			dataUser['max_connections'] = 1
			dataUser['created_at'] = time.time()
			dataUser['created_by'] = 1
			dataUser['is_trial'] = 0
			dataUser['forced_country'] = ""
			id = self.insert("users", dataUser)

			self.insert("user_output", {'user_id':id, 'access_output_id':1})
			self.insert("user_output", {'user_id':id, 'access_output_id':2})
			self.insert("user_output", {'user_id':id, 'access_output_id':3})

			array = {
			"status":100,
			"message":"The account has been activated successfully",
			"osd":self.osd,
			"expire":self.expire_date(exp_date),
			"user_agent":self.conf['user_agent'].strip(),
			"code_id":id
			}

			self.msg(array, "MasterCode User== {}".format(dataUser['username']))

		if len(list(sql_code)) == 1:
			row = sql_code[0]
			self.user = row.username
			self.password = row.password
			self.code_id = row.id
			status = int(row.status)
			expire = internal_function.date(row.data_expire, "%Y-%m-%d")

			if expire < datetime.today().strftime('%Y-%m-%d'):
				status = 4

			if status == 1:
				self.password = internal_function.uniqid()
				SqlModel.objects.raw("UPDATE users set password='{}' Where username='{}';".format(self.password, row.username.strip()))
				array = {
				"status":100,
				"message":"The Code is active",
				"osd":self.osd,
				"expire":self.expire_date(row.data_expire),
				"user_agent":self.conf['user_agent'].strip(),
				"code_id":row.id
				}

				self.msg(array, "ReActivation")

			elif status == 2:
				self.reply(102, "The Code is suspended", "@Suspended")
			elif status == 3:
				self.reply(103, "The Code is Deleted", "@Deleted Code")
			elif status == 4:
				self.reply(104, "The Code is Expired", "@Expired Code")


	def expire_date(self, exp_date):
		exp_date = float(exp_date)
		if self.conf['expire_date_type'] == 'days':
			datediff = exp_date - time.time()
			days = math.ceil(datediff / (60*60*24))
			return "{} Days".format(days)
		else:
			return internal_function.date(exp_date, "%Y-%m-%d")


	def activate_new_code_on_same_box(self, row_new_code):
		sql = SqlModel.objects.raw("Select id,code,days,date_expire From maa_codes " + 
			"WHERE mac='{}' AND serial='{}';".format(self.mac, self.sn))
		if len(list(sql)) > 0:
			row = sql[0]
			old_code = row.code
			date_expire = row.date_expire
			sql_u = SqlModel.objects.raw("SELECT id,username,exp_date FROM users WHERE username='{}'".format(old_code))
			row_u = sql_u[0]
			xlog = "OLdcode=[{}] New Code = [{}]<br/>\n<br/>".format(old_code, self.code)
			xlog += "OLD_CODE_date_expire=[{}] OLD USER exp_date = [{}]<br/>\n".format(date_expire, row_u.exp_date)
			
			self.log(xlog)

			new_expire_date = date_expire + (row_new_code['days']*60*60*24)

			#update new code
			up1 = SqlModel.objects.raw("UPDATE maa_codes SET status=1,mac='{}',serial='{}',date_expire='{}',userid='{}' WHERE code='{}';"
				.format(self.mac, self.sn, new_expire_date, row_u.id, self.code))

			#update olde code
			up2 = SqlModel.objects.raw("UPDATE maa_codes SET status=5,mac='',serial='',code_replaced='{}',date_expire='{}' WHERE code='{}';"
				.format(self.code, new_expire_date, old_code))

			#update extream code
			up3 = SqlModel.objects.raw("UPDATE users set username='{}', exp_date='{}' WHERE username='{}';"
				.format(self.code, new_expire_date, old_code))
			self.log("INSERT CODE on TOP of Code OLD={} NEW={} New Expriy = {}"
				.format(old_code, self.code, internal_function.date(new_expire_date, "%Y-%m-%d")))
			array = {
			"status":100,
			"message":"The account has been activated successfully",
			"osd":self.osd,
			"expire":self.expire_date(new_expire_date)
			}

			self.msg(array, "Success")

	
	
	def boolVerifyFree(self,code):
		sql_code = SqlModel.objects.raw("SELECT c.code, c.date_expire, c.status, u.username, u.password FROM maa_codes_free c, users u "
			+ "WHERE c.user=u.username AND c.code = '{}' AND c.serail='{}' AND c.mac='{}'"
			.format(code, self.sn, self.mac))
		if len(list(sql_code)) == 1:
			self.bouquets = 1
			return True
		return False

	
	def get_bouquets(self):
		sql = SqlModel.objects.raw("SELECT SQL_CACHE id FROM bouquets order by view_order asc;")
		arr = []
		for row in sql:
			arr.append(row.id)
		return arr

	def reply_function(self,status,msg,log): # ------------- Changed
		array = {
		"status":status,
		"message":msg,
		"osd":"",
		"expire":"NULL",
		"user_agent":"NULL",
		"code_id":"NULL"
		}
		self.msg(array, log)


	def osd_dismiss(self):
		code_id = int(self.code)
		SqlModel.objects.raw("UPDATE maa_codes set osd_stat=1,osd_msg='' WHERE id={}".format(code_id))
		self.msg({'status':100, 'message':"success", 'id':''})

	
	def osd_get(self):
		code_id = int(self.code_id)
		read = int(self.read)
		qry = ''

		if code_id == 0:
			sys.exit("error: Please set code_id")

		stat = {2:"مرسلة" , 1:"تمت القراءة"}
		result = SqlModel.objects.raw("SELECT id,osd_msg FROM maa_codes WHERE id={};".format(code_id))
		found = len(list(result))
		if found == 1:
			row = result[0]
			id = row.id
			osd_msg = row.osd_msg
			self.msg({'status':100, 'message':osd_msg})
		else:
			self.msg({status:000, 'message':"no_osd_message"})

	
	def osd(self):
		code_id = int(self.code_id)
		read = int(self.read)
		qry = ''
		stat = {
		2:"مرسلة" , 1:"تمت القراءة"
		}
		if read == 1:
			reply = self.reply.strip()
			if reply != "":
				result = SqlModel.objects.raw("SELECT osd_msg FROM maa_codes WHERE code='{}' AND id={};".format(self.code, code_id))
				row = result[0]
				reply = row.osd_msg + "\n\n\n at" +  internal_function.date(time.time(), "%Y-%m-%d %H:%M:%S") + "\n\n User Reply:\n\n " + reply
				SqlModel.objects.raw("UPDATE maa_codes SET osd_msg='{}' WHERE id={} AND code='{}';".format(reply, code_id, self.code))
			
			SqlModel.objects.raw("UPDATE maa_codes SET osd_stat=1 WHERE id=code_id AND code='{}';".format(code_id, self.code))
			sys.exit('')

		result = SqlModel.objects.raw("id, osd_msg FROM maa_codes WHERE osd_stat=2 AND code='{}' AND id={};".format(self.code, code_id))
		found = len(list(result))
		if found == 1:
			row = result[0]
			id = row.id
			osd_msg = row.osd_msg
			self.msg({'status':100, 'message':osd_msg, 'id':id})
		else:
			sys.exit("Not found in db")


	def insert(self,tablename,insData = {}):
		
		columns = ", ".join(insData.keys())
		filtered = []
		for key, data in insData.items():
			filtered.append("'" + str(data) + "'")
			#sys.exit(filtered)
			
		

		values = ", ".join(filtered)
		
		qry = "INSERT INTO {} ({}) VALUES ({})".format(tablename, columns, values)
		cursor = connection.cursor()
		#sys.exit(cursor)
		cursor.execute(qry,[])

		#SqlModel.objects.raw(qry)
		lastid = cursor.lastrowid
		return lastid


	def get_free_codes(self):
		sql =  SqlModel.objects.raw("SELECT * FROM maa_free_code;");
		for row in sql:
			self.free_codes.append(row.code.strip())

	def config(self):
		self.conf = {}
		replace = False

		if internal_function.isset_dic('strm_url_rep', _CFG['conf']) and _CFG['conf']['strm_url_rep'] != "" and internal_function.isset_dic('strm_url_with', _CFG['conf']) and _CFG['conf']['strm_url_with'] != "":
			replace = True

		sql = SqlModel.objects.raw("SELECT * FROM maa_options")
		for row in sql:
			op_name = row.name.strip()
			val = row.val.strip()
			if replace and (op_name == 'iptv_host' or op_name == 'iptv_host_vods'):
				val = val.replace(_CFG['conf']['strm_url_rep'], _CFG['conf']['strm_url_with'])

			self.conf[op_name] = val



	def log(self,thelog):
		file = os.path.basename(__file__)
		fullDATA = ''
		currentDomain  = self.request.META['HTTP_HOST']
		userAgent = self.request.META['HTTP_USER_AGENT'];

		data = {}


		
		# data['comment'] = ''
		# if internal_function.isset_dic('comment', self.request.GET):
		# 	data['comment'] = self.request.GET['comment']

		
		if internal_function.isset_dic('data',self.request.POST) and is_array(self.request.POST['data']):
			fullDATA = internal_function.var_export(self.request.POST['data'], True)

		data['ver'] = file.replace("API-", "")
		data['dtime'] = math.floor(time.time())
		data['thelog'] = thelog + ""
		data['ip'] = self.ip
		data['code'] = self.code
		data['serial'] = self.sn
		data['mac'] = self.mac
		data['model'] = self.model
		data['adminid'] = 0
		data['uagent'] = userAgent + " | {}<hr>{} ".format(currentDomain, fullDATA)

		self.insert(self.prefix + "_logs", data)


	def connect(self,thelog):

		return None
		
	
	def random_number(self,lenght):
		randval = internal_function.number_format(time.time() * random(),0)
		random = string[0:length]
		return random

	def generateRandomString(self,length = 10):
		characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
		charactersLength = len(characters)
		randomString = ''
		for i in range(0, length):
			randomString += characters[randrange(charactersLength)]

		return randomString
	
	def msg(self,array , msg = '' , cache_file = ''):
		#self.html_header()
		#sys.exit(array)

		data = json.dumps(array)
		if cache_file != '' and self.cache == True:
			if self.cache_type == "FILE":
				self.cache_file(data, cache_file, True)
			elif self.cache_type == "RDS":
				cache.set(cache_file, data, timeout=self.cache_time)

		if msg != "":
			self.log(msg)

		
		#print (self.runXOR(data))
		self.result = self.runXOR(data)
		#sys.exit(data)

		#sys.exit('')


	def html_header(self):
		print ("Content-Type: text/plain; charset=utf-8\n")

	def  capture(self):
		if self.conf['capture_ip'].strip() != "" and self.conf['cature_ip'].strip() == self.ip:
			data = ''
			for key, val in self.request.POST['data'].items():
				data += "<li>{} = ".format(key)
				if is_array(val):
					data += "<ul>"
					for key2, val2 in val.items():
						data += "<li>{} = {}</li>".format(key2, val2)
					data += "</ul>"

				data += "</li>"

			data += "<hr>"

			vars = ["HTTP_HOST","HTTP_USER_AGENT","CONTENT_TYPE","REQUEST_URI","SCRIPT_NAME"]
			for key in vars:
				val = ""
				if internal_function.isset_dic(key, self.request):
					val = self.request.environ[key]
				data += "<li>{} = {}</li>".format(key, val)

			for key, val in self.request.POST.items():
				data += "<li>{} = "

			self.insert("maa_logs_sys", {
				'dtime':internal_function.date(time.time(), "%Y-%m-%d %H:%M:%S"),
				'admin_user':'capture',
				'app':'V6',
				'ip':self.ip,
				'action':'capture',
				'the_log':data
				})



	def error(self,msg,log = ''): 
		array = {
		"status":9,
		"message":msg,
		"osd":"",
		"expire":"",
		"user_agent":"",
		"code_id":0
		}

		self.msg(array, log)
	
	def ip(self):
		ip = ""
		if internal_function.isset_dic('HTTP_CLIENT_IP', self.request.environ) and self.request.environ['HTTP_CLIENT_IP'] != "":
			ip = self.request.environ['HTTP_CLIENT_IP']
		elif internal_function.isset_dic('HTTP_X_FORWARDED_FOR', self.request.environ) and self.request.environ['HTTP_X_FORWARDED_FOR'] != "":
			ip = self.request.environ['HTTP_X_FORWARDED_FOR']
		else:
			ip = self.request.environ['REMOTE_ADDR']

		if ip.find(',') > 0:
			x = ip.split(",")
			ip = x[0].strip()

		return ip


	def runXOR(self,InputString):

		KeyPhrase = _CFG['XOR_KEY']
		if KeyPhrase == "":
			system.exit("Error: Please set XOR KEY.")

		KeyPhraseLength = len(KeyPhrase)
		resString = list(InputString)
		# Loop trough input string
		for i in range(len(InputString)):
			# Get key phrase character position
			rPos = i % KeyPhraseLength
			# Magic happens here:
			r = ord(InputString[i]) ^ ord(KeyPhrase[rPos])
			# Replace character
			resString[i] = chr(r)

		return "".join(resString)

	
	def cache_display(self,file,cache_type,CacheForChannels = False):

		if cache_type == "FILE":
			file = "./cache/" +  file
			# Check that cache file exists and is not too old
			# 60 seconds
			if not os.path.exists(file):

				return False
		
		
			if(math.floor(internal_function.file_mtime(file)) < math.floor(time.time()) - self.cache_time):
				return False
			# If so, display cache file and stop processing.


			if CacheForChannels == True:
				data = internal_function.file_get_contents(file)
				data = internal_function.multiple_replace({
					"{XuserX}":self.user,
					"{XpassX}":self.password
				}, data)
			else:
				data = file_get_contents(file)

			self.result = self.runXOR(data)

			return True

		elif cache_type == "RDS":
			exptime = cache.ttl(file)
			if exptime == 0:
				return False
			elif exptime > 0:
				data = cache.get(file)
				if CacheForChannels == True:
					data = internal_function.multiple_replace({
						"{XuserX}":self.user,
						"{XpassX}":self.password
					}, data)

				self.result = self.runXOR(data)
				return True

		else:
			return False
		

	def cache_file(self,content , file , CacheForChannels = False):

		if CacheForChannels ==  True:
			content = internal_function.multiple_replace({
				self.user:"{XuserX}",
				self.password:"{XpassX}"
				}, content)

			file = "./cache/" + file
			internal_function.file_write(file, content)



	def query(self,sql): #Verified

		#cursor = connection.cursor()
		#res = cursor.execute(sql,[])


		try:
			res = SqlModel.objects.raw(sql)
		except Exception as e:
			err = internal_function.date(time.time(), "%Y-%m-%d %H:%M:%S")
			err += " SQL = sql\n"
			err += " Error = " + e.error
			err += "\n"

			self.logfile(err)
		
		return res

	def logfile(self,data):
		if not os.path.isdir("./cache/"):
			os.mkdir("./cache/")
		if not os.access("./cache/", os.W_OK):
			return None

		date = internal_function.date(time.time(), "%Y-%m-%d %H:%M:%S")
		#print (internal_function.md5(date))
		log_file = "./cache/error_" + internal_function.md5(date + 'HiMama') + ".log"

		data += "\n\n"
		backtrace = ""
		internal_function.file_put_contents(log_file, data)

	def testfunc():
		global _CFG
		content = internal_function.multiple_replace({
				"AAA":"111",
				"BBB":"222"
				}, "AAA BBB")
		print (content)
		print (_CFG['debug'])


		file = "./cache/" +  "error_0e415e1c923aacc91d151eec1ac02c5d.log"
		# Check that cache file exists and is not too old
		# 60 seconds
		if not os.path.exists(file):
			return None
		
		print (internal_function.file_mtime(file))

		print (time.time() - 1)

		CacheForChannels = True

		if internal_function.file_mtime(file) < (time.time() - 1000000):
			return None
		# If so, display cache file and stop processing.

		if CacheForChannels == True:
			data = internal_function.file_get_contents(file)
			data = internal_function.multiple_replace({
				"{XuserX}":"1111",
				"{XpassX}":"2222"
				}, data)
		else:
			data = file_get_contents(file)

		#print (data)
		#print (request.environ['REMOTE_ADDR'])
		apicore = API6Core()

		#print (request.environ)

		#print (apicore.runXOR(data))
		#print (apicore.ip())

		#sys.exit('')

		return None



	


	





	


 







		


 



















	


		
		


		 
	  	  





