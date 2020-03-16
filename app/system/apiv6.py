import urllib.parse
import json
import hashlib
from app.system import internal_function
import sys
import requests
import platform
import certifi
from io import BytesIO
from django.http import HttpRequest as request_django # remove soon testing mode
from django.db import connection
from django.utils.html import strip_tags
from flask import jsonify, render_template, redirect,flash, url_for
import os
import string
import time
import datetime
import math
import MySQLdb
from app.system import core
from app.system import config_parse as configdata
import urllib.parse as parse_str
import re
from django_redis import get_redis_connection
from django.core.cache import cache
from app.models import SqlModel
is_array = lambda var: isinstance(var, (list, tuple)) 

 
global reqdata, reqmode
global _CFG

time_start = internal_function.microtime()
os.environ['TZ'] = 'Asia/Gaza'
if platform.system() != 'Windows':
	time.tzset()

_CFG = configdata.config['_CFG']

print ("============TEST FUNCTION=================")

r = get_redis_connection("default")  # Use the name you have defined for Redis in settings.CACHES
print("RDS connection status: %s" % r.flushall())
#cache.set("packages-cache", "", timeout=25)


#print (_CFG['debug'])
#print ("XORTEST: {}".format(core.API6Core.runXOR(None,"Wow!!!Great!!!This Django APi")))
#res =  core.API6Core.query(None, "SELECT * FROM users")
#for val in res:
#	print (val.username + "\n")
#core.API6Core.logfile(None, "test file making")
#core.API6Core.testfunc()





print ("\n============END TEST FUNCTION=================")

print ("\n\n============START=================")
if internal_function.isset_dic('debug', _CFG) and _CFG['debug'] == True:
	data = "------------------------POST----------------------------\n"
	for key, val in request.POST:
		data += "{}=>{}\n".format(key, val)
	data += "-----------------------REQUEST-----------------------\n"
	for key, val in request:
		data += "{}=>{}\n".format(key, val)

	data += "-------------------------PHP/INPUT=" + internal_function.file_get_contents('php://input') + "\n"
	data += "-------------------------END---POST---------------------------\n"
	data += "-------------------------SERVER--------------------\n"
	for key, val in request.environ:
		data += "{]=>{}".format(key, val)
	data += "=========================END=======================REQUEST=======================\n\n"
	internal_function.file_put_contents("./logs/" + request.environ['REMOTE_ADDR'] + "_.log", data)
	#sys.exit('YES')



class APIv6(core.API6Core):

	def __init__(self, request):
		#internal_function.die('')
		if not internal_function.isset(request.POST):
			parse_str.parse_qs(internal_function.file_get_contents('php://input'), request.POST)

			if internal_function.isset_dic('debug_post', _CFG) and _CFG['debug_post'] == True:
				internal_function.file_put_contents("./logs/post_is_empty.log", "{} | new post = {} \n".format(self.ip(), internal_function.var_export(request.POST)))
		if not internal_function.isset_dic('json', request.POST):
			input = internal_function.file_get_contents('php://input')
			if re.search("/json/", input):
				request.POST['json'] = input.replace('json=', input)
				if internal_function.isset_dic('debug_post', _CFG) and _CFG['debug_post'] == True:
					internal_function.file_put_contents("./logs/post_not_set_json.log", "{} = {}\n".format(self.ip(), input))
			else:
				if internal_function.isset('debug_post',_CFG) and _CFG['debug_post'] == True:
					internal_function.file_put_contents("./logs/post_is_vital.log", "{} = {}\n".format(self.ip(), input))

				internal_function.die("error: You seems did not send the POSTFILEDS: json=base64(xor_data)")
		base64 = request.POST['json']
		#internal_function.urldecode(request.POST['json']).replace(" ","+")
		#print (base64)
		#base64 = internal_function.urldecode(request.POST['json'])
		base64 = internal_function.base64_decode(base64)
		jsonRow = self.runXOR(base64)
		json = internal_function.json_decode(jsonRow)
		

		if not is_array(json):
			self._die("error: converting json data. Data you sent is: {} \n\r".format(jsonRow))
		if not internal_function.isset_dic('mode', json):
			self._die("error: no mode")
		if not internal_function.isset_dic('code', json):
			self._die("error: no code")
		if not internal_function.isset_dic('mac', json):
			self._die("error: no mac")
		if not internal_function.isset_dic('sn', json):
			self._die("error: no sn")
		self.osd = ""	

		#isseted...
		if internal_function.isset_dic('model', json):
			self.model = json['model']
		if internal_function.isset_dic('chipid', json):
			self.chipid = json['chipid']
		if internal_function.isset_dic('firmware_ver', json):
			self.firmware_ver = json['firmware_ver']
		if internal_function.isset_dic('catid', json):
			self.catid = json['catid']
		if internal_function.isset_dic('movie_id', json):
			self.movie_id = json['movie_id']
		if internal_function.isset_dic('series_id', json):
			self.series_id = int(json['series_id'])
		if  internal_function.isset_dic('code_id', json):
			self.code_id = json['code_id']
		if internal_function.isset_dic('read', json):
			self.read = json['read']
		if internal_function.isset_dic('reply', json):
			self.reply = json['reply']
		if internal_function.isset_dic('osd_test', json):
			self.osd_test = json['osd_test']
		if internal_function.isset_dic('pkg_id', json):
			self.pkg_id = int(json['pkg_id'])
		if internal_function.isset_dic('limit', json):
			self.limit = int(json['limit'])
		if internal_function.isset_dic('osd', json):
			self.osd = json['osd']

		if self.limit > 0:
			self.limit_qry = " LIMIT 0, {}".format(self.limit)

		reqdata = json
		reqmode = json['mode']

		self.result = ""

		self.jsondata = json
		self.cache_type = _CFG['cache_type']

		self.mac_enable = True
		self.config()

		self.code = json['code']
		self.mac = json['mac']
		self.sn = json['sn']

		self.chipid = json['chipid']
		self.model = json['model']
		self.firmware_ver = json['firmware_ver']
		self.request = request

		self.ip = self.ip()
		self.MasterCodes = {}

		

		self.get_free_codes()
		self.getMasterCodes()

		self.capture()

		self.iptv_stream_host = self.conf['iptv_host'].strip()

		if os.path.isdir("../cache/"):
			self.cache = False

		if reqmode == 'active':
			self.active()
		elif reqmode == 'packages':
			self.packages()
		elif reqmode == 'movies_cat':
			self.movies_cat()
		elif reqmode == 'movies_list':
			self.movies_list()
		elif reqmode == 'series_cat':
			self.series_cat()
		elif reqmode == 'myMusic':
			self.myMusic()
		elif reqmode == 'movies_filters':
			self.movies_filters()
		elif reqmode == 'movies_info':
			self.movies_info()
		elif reqmode == 'series_cartoon':
			self.series_cartoon()
		elif reqmode == 'series_list':
			self.series_list()
		elif reqmode == 'series_info':
			self.series_info()



	def active(self):
		self.ProcessActivation(self.code, self.sn, self.mac, self.ip)

	def ProcessActivation(self, code, sn, mac, ip):

		if code in self.free_codes:
			self.proccess_free_code(code, sn, mac, ip)

		why_worng_code = ''
		qry = sql_grp = ''
		txt = 'byCode'

		codeMacQry = "c.userid=u.id"
		if internal_function.isset_dic(code, self.MasterCodes):
			if self.MasterCodes[code] == 1:
				qry = " AND mac='{}'".format(self.mac)
				txt = "byMAC"
				codeMacQry = "c.userid=u.id"
			elif self.MasterCodes[code] == 2:
				qry = " AND serial='{}'".format(self.sn)
				txt = "bySerial"
				codeMacQry = "c.userid=u.id"

		if internal_function.isset_dic('enable_group', _CFG) and _CFG['enable_group'] == 'Yes':
			sql_grp = ",(SELECT group_id from maa_admin adm where adm.adminid=cod.adminid) AS groupID"

		sql_query = "Select * {} From {}_codes cod where cod.code='{}' {};".format(sql_grp, self.prefix, code, qry)
		sql_code = self.query(sql_query)

		if len(list(sql_code)) == 1:
			row_code = sql_code[0]
			code_status = row_code.status
			code_replaced = row_code.code_replaced
			groupID = int(row_code.groupID)

			if groupID != 0 and internal_function.isset('enable_group', _CFG) and _CFG['enable_group'] == 'Yes' and int(GROUP) != 0:
				if groupID != GROUP:
					self.reply(119, "This code is not for this Brand.", "@CodeNotForBrand")


			if code_status == 1:
				if self.mac != row_code.mac:
					why_worng_code = " Mac not match "
				if self.sn != row_code.serial:
					why_worng_code = " SN not match "


			if row_code.inputBy == 0:
				#is normal code
				if row_code.mac == 'reset_me' and row_code.serial == 'reset_me':
					self.query("Udate {}_codes set mac=='{}',serial='{}' Where id='{}';".format(self.prefix, mac, sn, row_code.id))

				if code_replaced != "" and code_status == 5:
					self.reply(115, "Code is replaced. Please use this code: {}".format(code_replaced), "@Replaced")


			if code_status == 0:
				self.activate_new_code(row_code)
				sys.exit('')
			elif code_status == 2:
				self.reply(102, "The Code is suspended", "@Suspended {}".format(txt))
			elif code_status == 3:
				self.reply(103, "The Code is Deleted!", "@Deleted {}".format(txt))
		else:
			self.insertIP('notfound')
			self.reply(103, "The Code is not Found!", "@Wrong {}".format(txt))

		
		qry = "SELECT c.id, c.code, c.userid, c.date_expire,c.status,c.osd_msg,u.username,u.password FROM maa_codes c, users u WHERE c.userid=u.id AND c.code='{}' AND c.mac='{}' AND c.serial='{}';".format(code, self.mac, self.sn)


		result = self.query(qry)
		if len(list(result)) == 0:
			self.reply(103, "The Code is Not valid for this device.", "@NotValidForDevice {} {}".format(txt, why_worng_code))

		row = result[0]
		username = row.username
		password = row.password

		self.user = row.username
		self.password = row.password
		self.code_id = row.id
		userid = int(row.id)

		status = int(row.status)
		expire = internal_function.date(row.date_expire, "%Y-%m-%d")
		if expire < internal_function.date(time.time(), "%Y-%m-%d"):
			status = 4

		if status == 1:
			if internal_function.isset_dic('update_password', _CFG) and _CFG['update_password'] == 'yes':
				password = self.generateRandomString(10)
				self.query("UPDATE `users` set `password`='{}' WHERE `id`={};".format(password, userid))

			self.query("UPDATE maa_codes set protocol=6 WHERE id={};".format(self.code_id))

			if self.osd == "":
				self.osd = row.osd_msg

			array = {
			"status":100,
			"message":"The Code is active",
			"osd":self.osd,
			"expire":self.expire_date(row.date_expire),
			"user_agent":self.conf['user_agent'].strip(),
			"code_id":self.code_id
			}

			self.insertModel()

			self.msg(array, "ReActivation")
		
		elif status == 2:
			self.reply(102, "The Code is suspended", "@Suspended")

		elif status == 3:
			self.reply(103, "The Code is Deleted", "@Deleted Code")

		elif status == 4:
			self.reply(104, "The Code is Expired", "@Exipred Code")



	def activate_new_code(self, row):
		#if the code is used on the same box, add days to old code based on Serial/Mac
		if self.conf['multi_code'] == 1:
			self.activate_new_code_on_same_box(row)

		days = int(row['days'])
		period = int(row['period'])
		free_days = int(row['free_days'])
		code = row['code'].strip()
		fullname = row['fullname'].strip()
		forced_country = row['forced_country'].strip()
		codeID = intval(row['id'])

		#Setup expire date.
		if period in self.free:
			dd = period - 100
			exp_date = datetime.datetime.now() + datetime.timedelta(dd)
		else:
			exp_date = internal_function.add_months(datetime.date.today(), period)
			if free_days > 0:
				exp_date = exp_date + datetime.timedelta(free_days)

		#Check if code is Code or MAC or Serial and correct username
		if row['inputBy'] == 0:
			username = code
		else:
			username = row['username'].strip()

		data['member_id'] = 1
		data['username'] = username
		data['password'] = internal_function.uniqid() + self.random_number(1000)
		data['exp_date'] = exp_date
		intputVal = ""
		if row['inputBy'] == 1:
			intputVal = " MAC"
		elif row['inputBy'] == 2:
			inputVal = " SN"
		data['admin_notes'] = "{}".format(fullname) + inputVal
		data['admin_enabled'] = 1
		data['enabled'] = 1
		data['bouquet'] = '[' + row['bouquets'] + ']'
		data['max_connection'] = 1
		data['created_at'] = time.time()
		data['create_by'] = 1
		data['forced_country'] = forced_country

		if row['allowed_uagent'] != '':
			UA_json = row['allowed_uagent'].strip().split(",")
			data['allowed_ua'] = json.dumps(UA_json)

		sql = self.query("SELECT id,username FROM users WHERE username='{}' LIMIT 1".format(username))
		if len(list(sql)) == 0:
			xtID = self.insert("users", data)

			self.insert("user_output", {'user_id':xtID, 'access_output_id':1})
			self.insert("user_output", {'user_id':xtID, 'access_output_id':2})
			self.insert("user_output", {'user_id':xtID, 'access_output_id':3})
		else:
			xrow = sql[0]
			xtID = xrow.id

		if row['inputBy'] == 0:
			whatToUpdate = "mac='{}', serila='{}'".format(self.mac, self.sn)
			txt = "Code"
		elif row['inputBy'] == 1:
			whatToUpdate = "serial='{}'".format(self.sn)
		elif row['inputBy'] == 2:
			whatToUpdate = "mac='{}'".format(self.mac)
			txt = "Serial"

		now = time.time()

		up = self.query("Update maa_codes set status=1, {}, date_start='{}', date_expire='{}', userid='{}',protocol=6,model='{}' WHERE id={}"
			.format(whatToUpdate, now, exp_date, xtID, self.model, codeID))

		self.log("Activate By {} |expire = " +  internal_function.date(exp_date, "%Y-%m-%d %H:%M:%S"))

		array = {
		"status":100,
		"message":"The Code has been activated successfully",
		"osd":self.osd,
		"expire":self.epxire_date(exp_date),
		"user_agent":self.conf['user_agent'],
		"code_id":codeID
		}

		self.code_id = codeID
		self.insertModel()

		self.msg(array, "Success {}".format(txt))


	def boolVerifyUser(self, func=''):

		sql = "SELECT 1 as id, c.code, c.adminid, c.transid, c.date_expire, c.status, c.bouquets, c.output, u.username, u.password FROM maa_codes c, users u WHERE c.userid=u.id AND c.code='{}' AND c.mac='{}' AND c.serial='{}' LIMIT 1;".format(self.code, self.mac, self.sn)
		

		result = self.query(sql)

		num = len(list(result))

		if num == 1:
			row = result[0]
			self.adminid = int(row.adminid)
			self.transid = int(row.transid)
			self.user = row.username.strip()
			self.password = row.password.strip()
			self.date_expire = row.date_expire.strip()
			self.output = row.output.strip()

			if row.bouquets != "":
				self.bouquets = row.bouquets

			return True

		self.error("Error: Something Wrong with code. Check MAC/Serial.", "Code Not found in boolVerifyUser() from : {}".format(func))
		return False

	################################
	## Note: ID =1 , is ALL (download all channels + Baqutes)
	## if i choose Arabic + SKY (i must see only Arabic and Sky)
	## if i choose ALL - I must see newly added Baquotes Automatically
	################################

	def packages(self):
		
		CacheFile = ''
		self.boolVerifyUser("packages")
		if self.bouquets == "":
			self.error("Error: no Packages for this code.", "Err Packages in Empty")

		#sys.exit(self.cache)

		if self.cache == True:

			CacheFile = "pkgs_{}_".format(self.output) + internal_function.md5(self.bouquets.replace(",","_")) + ".txt"


			if self.cache_display(CacheFile, self.cache_type, True):
				return None
			

		ar = {}


		
		bq = self.bouquets.split(",")

		if len(self.conf['exclude_movies_pkg']) >= 1:
			ex = self.conf['exclude_movies_pkg'].split(",")
			bq = bq - ex


		if is_array(bq):
			strVal = "id IN ({})".format(",".join(bq)) + " Order by view_order asc;"
			if len(self.bouquets) == 1 and self.bouquets == 1:
				strVal = "id!=1"

			qry = "SELECT * FROM bouquets " + "WHERE {}".format(strVal)
			
			

			sql = self.query(qry)
			ar = []

			for row in sql:
				icon = row.bouquet_icon.strip()
				if icon == "":
					icon = "http://intro.ps/uploads/logo/tv.png"

				ar.append({
				"pkg_id":row.id,
				"pkg_name":row.bouquet_name,
				"pkg_type":0,
				"pkg_icon":icon,
				"pkg_order":row.view_order,
				"pkg_parent":0,
				"pkg_channels":self.channels(row.bouquet_channels, row.id)
				})

			self.msg({"packages":ar},'', CacheFile)
			#sys.exit(math.floor(internal_function.file_mtime("./cache/"+ CacheFile)))

	def lite_packages(self):

		CacheFile = ''
		self.boolVerifyUser("lite_packages")

		if self.cache ==  True:
			CacheFile = "lite_pkgs_" + internal_function.md5(self.bouquets.replace(",","_")) + ".txt"
			self.cache_display(CacheFile)

		ar = []
		bq = self.bouquets.split(",")

		if is_array(bq):
			if len(self.conf['exclude_movies_pkg']) > 1:
				ex = self.conf['exclude_movies_pkg'].split(",")
				bq = bq - ex

			qry = "SELECT SQL_CACHE * FROM bouquets "
			+" WHERE id in({}) ORDER BY view_order ASC".format(bq.join(","))

			sql = self.query(qry)

			for row in sql:
				bouquet_channels = json.loads(row.bouquet_channels)
				ch_count = len(bouquet_channels)

				ar.append(
					{
					"pkg_id":row.id,
					"pkg_name":row.bouquet_name,
					"pkg_icon":row.bouquet_icon.strip()
					})

			self.msg(ar, '', CacheFile)


	def lite_channels(self):
		CacheFile = ''
		ar = []

		pkg_id = self.pkg_id
		if pkg_id == 0:
			ar.append({
				"stream_id":0,
				"stream_name":"error: Package ID is 0",
				"stream_pkg_id":0,
				"stream_icon":'',
				"stream_order":0,
				"stream_url":''
				})

			self.msg(ar)

		self.boolVerifyUser("lite_packages")

		if self.cache ==  True:
			CacheFile = "lite_chans_" + pkg_id +  ".txt"
			self.cache_display(CacheFile, True)

		sql = self.query("SELECT SQL_CACHE * FROM bouquets WHERE id={};".format(pkg_id))
		row = sql[0]

		ar.append(self.channels(row.bouquet_channels, row.id))

		self.msg(ar, '', CacheFile)

	def sat2iptv(self):
		ar = []
		qry = ''
		self.isSatToIPTV = True

		if int(self.conf['enable_sat2iptv']) == 0:
			sys.exit('')

		self.boolVerifyUser("sat2iptv")

		if  internal_function.isset(self.stb_groups) and len(self.stb_groups) >= 1:
			qry = " WHERE stb_groups IN({})".format(",".join(self.stb_groups))

		if self.cache == True:
			CacheFile = "sat2iptv.txt"
			self.cache_display(CacheFile, True)

		sql =  self.query("SELECT SQL_CACHE * FROM {}_stb_to_iptv stb {} order by angle asc, stb_ch_name ASC;").format(self.prefix, qry)

		for row in sql:
			stream = internal_function.multiple_replace({
				"{type}":"live",
				"{user}":self.user,
				"{pass}":self.password,
				"{ch}":row.ch_id
				}, self.conf['iptv_host'].strip())

			ar.append({
				'channel_name':row.stb_ch_name,
				'angle':row.angle,
				'tp':row.tp,
				'pol':row.pol,
				'sid':row.sid,
				'stream_url':stream
				})

		self.msg(ar, '', CacheFile)


	def channels(self, data, bq_id):
		ar = []
		
		data = json.loads(data)
		i = 0


		for ch in data:
			++i

			invalidChars = set(string.punctuation.replace("_", ""))
			if any(char in invalidChars for char in str(ch)):
				continue


			ch = int(str(ch))

			qry = "SELECT SQL_CACHE id, stream_display_name,stream_source, stream_icon, streams.`order` as view_order, movie_subtitles,notes FROM streams  WHERE `type`!=2 AND id={} AND stream_display_name NOT LIKE '%%*%%' AND stream_display_name NOT LIKE '%%===%%';".format(ch)

			sql_ch = self.query(qry)


			if len(list(sql_ch)) == 1:
				row = sql_ch[0]
				if self.output == "":
					self.output == "ts"

				#For vod only protocols
				if internal_function.isset_dic('vod', _CFG) and _CFG['vod'] == 'Yes':
					stream = json.loads(row.stream_source)
					if is_array(stream):
						stream = strean[0]

					if stream == "":
						stream = row.stream_source.strip()
				else:

					stream = internal_function.multiple_replace(
						{
						"{type}":"live",
						"{user}":self.user,
						"{pass}":self.password,
						"{ch}":str(row.id),
						".ts":"." + self.output
						}, self.conf['iptv_host'].strip())

				if internal_function.isset_dic('user_stream_source', _CFG) and _CFG['user_stream_source'] == 'Yes':
					stream = json.loads(row.stream_source)

					if is_array(stream):
						stream = stream[0]

					if stream == "":
						stream =  row.stream_source.strip(0)

				stream_display_name = internal_function.multiple_replace({
					"{":" ",
					"}":" "
					}, row.stream_display_name)

				icon = row.stream_icon.strip()
				if re.search("/base64/", icon):
					icon = ""

				ar.append({
					"stream_id":ch,
					"stream_name":stream_display_name,
					"stream_pkg_id":bq_id,
					"stream_icon":icon,
					"stream_order":i,
					"stream_url":stream
					})

				if internal_function.isset_dic('vod', _CFG) and _CFG['vod'] == 'Yes':
					ar[len(ar) - 1]['subtitle'] = row.movie_subtilte
					ar[len(ar) - 1]['color'] = row['notes']

		return ar


	def series_cat(self):
		if internal_function.isset_dic('UseIntroSeries',_CFG) and _CFG['UseIntroSeries'] == 'Yes':
			self.IntroSeriesCat()
			sys.exit('die')

		if internal_function.isset_dic('remote_series_use', _CFG) and int(self.conf['remote_series_use']) == 1:
			self.boolVerifyUser("series_cat")
			mv = core.Movies(self, "series_cat")
			sys.exit('die')

		self.movies_cat('series')


	def movies_kids(self):
		ex1 = self.conf['vod_music'].split(",")
		em = ex1.split(",")
		self.movie_cat('movie', " AND id IN ({}) ".format(em))


	def music(self):
		ex1 = self.conf['vod_music'].split(",")
		ids = ",".join(ex1)
		if ids == '':
			ids = 0

		self.boolVerifyUser("music")

		qry = parent = ''

		if internal_function.isset_dic('CategoriesOrder', self.conf) and self.conf['CategoriesOrder'] != "":
			self.CatOrder = self.conf['CategoriesOrder'].replace(":"," ")

		ar = []

		qry = "SELECT SQL_CACHE * FROM stream_categories WHERE category_type LIKE 'movie' "
		+ " AND parent_id IN ({}) ORDER BY {};".format(ids, self.CatOrder)

		sql = self.query(qry)
		i = 0

		for row in sql:
			++i
			category_icon = row.category_icon.strip()
			icon = category_icon
			if category_icon == "":
				icon = "http://intro.ps/uploads/logo/movie.png"
			ar.append({
				"cat_id":row.id,
				"cat_name":row.category_name,
				"cat_icon":icon,
				"music_files":self.getMusicFiles(row.id, row, icon)
				})

		self.msg(ar)


	def getMusicFiles(self, catid, rowFather, icon):
		ar = []

		sql = self.query("SELECT SQL_CACHE id, stream_display_name,stream_source, "
			+ " strea_icon, streams.`order` as view_order, target_container FROM streams "
			+ " WHERE category_id={} AND stream_display_name NOT LIKE '%%*%%' ".format(catid)
			+ " AND stream_display_name NOT LIKE '%%===%%' ORDER BY id DESC;")

		i = 0
		for row in sql:
			target_container = "." + internal_function.preg_replace("/[^A-Za-z0-9]/", "", row.target_container)

			stream = internal_function.multiple_replace({
				"{type}":"movie",
				"{user}":self.user,
				"{pass}":self.password,
				"{ch}":row.id,
				".ts":target_container,
				".m3u8":target_container,
				"{container}":target_container
				}, self.conf['iptv_host_vod'].strip())

			ar.append({
				"id":row.id,
				"title":row.stream_display_name,
				"catid":"{}".format(catid),
				"icon":row.stream_icon.strip(),
				"stream_url":stream
				})

		return ar

	def lite_vod_cat(self, category_type='movie'):
		self.boolVerifyUser("movies_cat")

		if internal_function.isset_dic('CategoriesOrder', self.conf) and self.conf['CategoriesOrder'] != "":
			self.CatOrder = self.conf['CategoriesOrder'].replace(":", " ")

		ar = []
		qry = "SELECT SQL_CACHE * FROM stream_categories WHERE category_type LIKE '{}'"
		+" AND parent_id=0 ORDER BY {} LIMIT 50".format(category_type, self.CatOrder)

		sql = self.query(qry)

		i = 0

		for row in sql:
			++i
			#id category_type category_name parent_id cat_order

			category_icon = row.category_icon.strip()
			icon = category_icon
			if icon == "":
				icon = ""

			ar.append({
				"cat_id":row.id,
				"cat_name":row.category_name,
				"cat_icon":icon,
				"cat_view_order":i
				})

		self.msg(ar)	


	def movies_cat(self, category_type = 'movie', qryVod = ''):

		self.boolVerifyUser("movies_cat")

		if internal_function.isset_dic('remote_movies_use',self.conf) and int(self.conf['remote_movies_use']) == 1 and category_type == 'movie':
			mv = cor.Movies(self, "movies_cat")
			sys.exit("die")

		qry = parent = ''

		if qryVod == "" and internal_function.isset_dic('remote_movies_use', self.conf) and self.conf['remote_movies_use'] == 1:

			# exclude kids, series, music categories from movies cat
			ex1 = self.conf['vod_kids'].split(",")
			ex2 = self.conf['vod_series'].split(",")
			excludeIds = internal_function.array_merge(ex1, ex2)

			if len(excludeIds) > 0:
				ids = ",".join(excludeIds)
				if ids != '':
					qryVod = " AND id NOT IN ({}) ".format(ids)
					# AND parent_id NOT IN ($ids)

		if internal_function.isset_dic('CategoriesOrder', self.conf) and self.conf['CategoriesOrder'] != "":
			self.CatOrder = self.conf["CategoriesOrder"].replace(":", " ")

		catsBouqts = ''

		if internal_function.isset_dic('CatFromBouquets', _CFG) and _CFG['CatFromBouquets'] == 'Yes':

			bq = self.bouquets.split(",")
			sqlB = self.query("SELECT SQL_CACHE * FROM bouquets "
				+ " WHERE id IN ({}) ORDER BY view_order asc;".format(",".join(bq)))
			chans = []
			for rowB in sqlB:
				bouquet_channels = json.loads(rowB.bouquet_channels)
				for ch in bouquet_channels:
					chans.append(ch)

			catsBouqts = " AND id in (select category_id FROM streams where id IN({}))".format(','.join(chans))

		#View Order
		ar = []
		qry = "SELECT SQL_CACHE * FROM stream_categories WHERE category_type LIKE '{}' AND parent_id=0 {} {} ORDER BY {}".format(category_type, qryVod, catsBouqts, self.CatOrder)

		sql = self.query(qry)

		i = 0
		for row in sql:
			++i
			# id category_type category_name parent_id cat_order 

			category_icon = row.category_icon.strip()
			icon = category_icon
			if icon == "":
				icon = "http://intro.ps/uploads/logo/movie.png"

			if row.cat_order == 0:
				row.cat_order = i

			ar.append({
				"cat_id":row.id,
				"cat_name":row.category_name,
				"cat_icon":icon,
				"cat_view_order":row.cat_order,
				"sub_cats":self.subMoviesCat(row.id, row, icon)
				})

		if len(list(sql)) == 0:
			ar.append({
				"cat_id":0,
				"cat_name":"error no-series-cat",
				"cat_icon":"{}".format(qry),
				"cat_view_order":0,
				"sub_cats":[]
				})

		self.msg(ar)



	def subMoviesCat(self, parent, rowFather, iconFather):

		parent = int(parent)

		ar = []
		qry = "SELECT * FROM `stream_categories` WHERE category_type LIKE 'movie' AND parent_id={} order by {} ".format(parent, self.CatOrder)


		sql = self.query(qry)
		i = 0

		for row in sql:
			++i
			# id category_type category_name parent_id cat_order 

			category_icon = row.category_icon.strip()
			icon = category_icon
			if icon == "":
				icon = "http://intro.ps/uploads/logo/movie.png"

			if row.cat_order == 0:
				row.cat_order = i

			ar.append(
				{
				"sub_id":row.id,
				"sub_name":row.category_name,
				"sub_icon":icon,
				"sub_view_order":row.cat_order
				})

		if i == 0:

			ar.append(
				{
				"sub_id":rowFather.id,
				"sub_name":rowFather.category_name,
				"sub_icon":iconFather,
				"sub_view_order":rowFather.cat_order
				})

		return ar


	def movies_list(self):
		ar = []

		self.boolVerifyUser("movies_list")

		if internal_function.isset_dic('remote_movies_use', self.conf) and int(self.conf['remote_movies_use']) == 1:
			mv = core.Movies(self, "movies_list")
			sys.exit('die')

		qry = ''

		if self.catid == 'all':
			qry = ''
		else:
			qry = " AND category_id={}".format(self.catid)

		if int(self.catid) == 0 and self.catid != 'all':
			ar.append({
				"id":"",
				"title":"Error: you must pass (catid) in url.",
				"catid":"",
				"icon":"",
				"view_order":"",
				"stream_url":""
				})
			self.msg(ar)

		if internal_function.isset_dic('MoviesOrder', self.conf) and self.conf['MoviesOrder'] != "":
			movies_order = self.conf['MoviesOrder']
		else:
			movies_order = "streams.`order` ASC"

		self.SetLimitForBadBox('bad_stb_tot_vod')

		sql_ch = self.query("SELECT id, stream_display_name, category_id, stream_source, stream_icon, streams.`order` as view_order, movie_propeties, target_container FROM `streams`"
		+ " WHERE `type`=2 {} ORDER BY {} {};".format(qry, movies_order, self.limit_qry))

		i = 0
		for row in sql_ch:
			++i

			target_container = "." + internal_function.preg_replace('/[^A-Za-z0-9]/', "", row.target_container)

			if internal_function.isset('vod', _CFG) and _CFG['vod'] == 'Yes':
				stream = json.loads(row.stream_source)
				if is_array(stream):
					stream = stream[0]

				if stream == "":
					stream = row.stream_source.strip()

			else:
				stream = internal_function.multiple_replace({
					"{type}":"movie",
					"{user}":self.user,
					"{pass}":self.password,
					"{ch}":row.id,
					".ts":target_container,
					"m3u8":target_container,
					".{container}":target_container
					}, self.conf['iptv_host_vod'].strip())

			movie_properties = json.loads(row.movie_properties)

			if internal_function.isset(movie_properties['movie_image']) and movie_properties['movie_image'] != "":
				stream_icon = movie_properties['movie_image'].strip()
			else:
				stream_icon = row.stream_icon.strip()

			ar.append({
			"id":row.id,
			"title":row.stream_display_name,
			"catid":row.category_id,
			"icon":stream_icon,
			"view_order":i,
			"stream_url":stream
			})

		if i == 0:
			ar.append({
			"id":0,
			"title":"empty category: this is sample",
			"catid":0,
			"icon":"https://www.sample-videos.com/images/imgw.png",
			"view_order":0,
			"stream_url":"https://www.sample-videos.com/video/mp4/720/big_buck_bunny_720p_5mb.mp4"
			})


		self.msg(ar)


	def series_latest(self):

		self.boolVerifyUser("series_lastest")

		if internal_function.isset_dic('remote_series_use', self.conf) and int(self.conf['remote_series_use']) == 1:
			mv = core.Movies(self, "series_lastest")
			sys.exit('die')


	def series_details(self):

		self.boolVerifyUser("series_details")

		if internal_function.isset('remote_series_use', self.conf) and int(self.conf['remote_series_use']) == 1:
			mv = core.Movies(self, "series_details")
			internal_function.die()



	def episode_info(self):

		self.boolVerifyUser("episode_info")

		if internal_function.isset('remote_series_use', self.conf) and int(self.conf['remote_series_use']) == 1:
			mv = core.Movies(self, "episode_info")
			internal_function.die()


	def movies_info(self):

		self.boolVerifyUser("movies_info")

		if internal_function.isset_dic('remote_series_use', self.conf) and int(self.conf['remote_series_use']) == 1:
			mv = core.Movies(self, "movies_info")
			internal_function.die()

		qry = ''

		ar = []

		id = int(self.movie_id)

		sql = self.query("SELECT SQL_CACHE id, stream_display_name,category_id,stream_icon,movie_propeties,target_container FROM `streams`"
			+ " WHERE `type`=2 AND id={}".format(id))

		if len(list(sql)) == 1:
			row = sql[0]
			target_container = "." + internal_function.preg_replace("/[^A-Za-z0-9]/", "", row.target_container)
			#//http://hahaiptv.net:7777/{type}/{user}/{pass}/{ch}.ts
			stream = internal_function.multiple_replace({
					"{type}":"movie",
					"{user}":self.user,
					"{pass}":self.password,
					"{ch}":str(row.id),
					".ts":target_container,
					"m3u8":target_container,
					".{container}":target_container
					}, self.conf['iptv_host_vod'].strip())

			movie_properties = json.loads(row.movie_propeties)

			if internal_function.isset('movie_image', movie_properties) and movie_properties['movie_image'] != "":
				stream_icon = movie_properties['movie_image'].strip()
			else:
				stream_icon = row.stream_icon.strip()

			genre = movie_propeties['genre'].strip()
			plot = movie_propeties['plot'].strip()
			cast = movie_propeties['cast'].strip()
			duration = movie_propeties['duration'].strip()
			bitrate = movie_propeties['bitrate'].strip()
			rating = movie_propeties['rating'].strip()

			if genre == "":
				genre = "Genre: N/A"
			if plot == "":
				plot = "Plot: N/A"
			if cast == "":
				cast = "Cast: N/A"
			if duration == "":
				duration = "Duration: N/A"
			if bitrate == "":
				bitrate = "Bitrate: N/A"
			if rating == "":
				rating = "Rating: N/A"

			ar.append({
					"id":row.id,
					"stream_display_name":row.stream_display_name,
					"category_id": int(row.category_id),
					"stream_icon":stream_icon,
					"stream_url":stream,
					"movie_image":movie_propeties['movie_image'],
					"genre":genre,
					"plot":plot,
					"cast":internal_function.substr(cast,0,250),
					"duration":duration,
					"bitrate":bitrate,
					"rate":rating,
					"rating":rating
					#"movie_propeties" => json_decode($row['movie_propeties'] , true)
			});
		elif len(list(sql)) == 0:
			ar.append({
					"id":None,
					"stream_display_name":None,
					"category_id": 0,
					"stream_icon":"",
					"stream_url":"",
					"movie_image":None,
					"genre":"N/A",
					"plot":"N/A",
					"cast":"N/A",
					"duration":"N/A",
					"bitrate":"N/A",
					"rate":"N/A",
					"rating":"N/A"
					#"movie_propeties" => json_decode($row['movie_propeties'] , true)
			});


		self.msg(ar)


	def series_netflix(self):

		catids = self.conf['vod_series']
		self.catid = catids

		self.series_list()

	def series_cartoon(self):

		catids = self.conf['vod_kids']
		self.catid = catids

		self.series_list()


	def SetLimitForBadBox(self, bad_stb_tot):

		if internal_function.isset_dic('bad_stb_limit_trans', self.conf) and self.conf['bad_stb_limit_trans'] != "" and internal_function.isset_dic(bad_stb_tot, self.conf):
			trans = self.conf['bad_stb_limit_trans'].split(",")
			if self.transid in trans:
				self.limit_qry = " LIMIT " +  int(self.conf[bad_stb_tot])


	def series_list(self):
		self.boolVerifyUser('seres_list')
		if(internal_function.isset_dic('UseIntroSeries', _CFG)) and _CFG['UseIntroSeries'] == "Yes":
			self.IntroSeriesList()
			internal_function.die()

		err = ''
		ar = []

		if internal_function.isset_dic('remote_series_use', self.conf) and int(self.conf['remote_series_use']) == 1:
			mv = core.Movies(self, "seriesForBOX")
			internal_function.die()

		self.SetLimitForBadBox('bad_stb_tot_series')

		qry = ''

		if self.catid == 'all':
			qry = ''
		elif int(self.catid) > 0:
			catID = int(self.catid)
			qry = " AND category_id={}".format(catID)
		else:
			err = " Error: you must pass the catid like: \"catid\":\"xx\" or \"catid\":\"all\" "

		sql_ch = SqlModel.objects.raw("SELECT * FROM `series` WHERE TRUE {} ORDER BY category_id ASC,id DESC {};".format(qry, self.limit_qry))

		genre = ''
		for row in sql_ch:

			#internal_function.extract(row)
			# id 	title 	category_id 	cover 	cover_big 	genre 	plot 	cast 	
			# rating 	director 	releaseDate 	last_modified 	tmdb_id 	seasons
			# cover = cover_big = 'http://intro.ps/uploads/logo/movie.png';

			ar.append({
				"id":row.id,
				"title":row.title,
				"icon":row.cover,
				"catid":row.category_id,
				"icon_big":row.cover_big,
				"genre":row.genre,
				"plot":row.plot,
				"cast":row.cast,
				"rating":row.rating,
				"director":row.director,
				"releaseDate":row.releaseDate
				})
		if err == '':
			err = 'No Series'

		if len(list(sql_ch)) == 0:

			ar.append({
				"id":0,
				"title":err,
				"icon":'',
				"catid":'',
				"icon_big":'',
				"genre":'',
				"plot":'',
				"cast":'',
				"rating":'',
				"director":'',
				"releaseDate":''
				})

		self.msg(ar)



	def series_info(self):
		self.series_episodes()


	def series_episodes(self):

		self.boolVerifyUser("series_episodes")

		if internal_function.isset_dic('UseIntroSeries', _CFG) and _CFG['UseIntroSeries'] == "Yes":
			self.IntroSeriesGetDetails()
			internal_function.die()

		if internal_function.isset_dic('remote_series_use', self.conf) and int(self.conf['remote_series_use']) == 1:
			mv = core.Movies(self, "series_details")
			internal_function.die()

		err = ''
		ar = []
		qry = ''

		series_id = int(self.series_id)
		if series_id == 0:
			err = " Error: you must pass the series_id=xx"

		# id season_num 	series_id 	stream_id 	sort

		sql_ch = self.query("SELECT s.id, s.stream_display_name, s.stream_source,s.redirect_stream "
			+ ", s.stream_icon, s.movie_propeties,s.target_container,ep.season_num "
			+ "FROM `streams` s ,`series_episodes` ep WHERE s.id=ep.stream_id "
			+ " AND ep.series_id={} ORDER BY  season_num ASC, ep.`sort` ASC;".format(series_id))

		i = 0
		row = {}
		for row in sql_ch:
			++i
			target_container = "." + internal_function.preg_replace('/[^A-Za-z0-9]/', "", row.target_container)
			# http://hahaiptv.net:7777/{type}/{user}/{pass}/{ch}.ts

			if row.redirect_stream == 1:
				stream = json.loads(row.stream_source)
				if is_array(stream):
					stream = stream[0]
			else:
				stream = internal_function.multiple_replace({
					"{type}":"series",
					"{user}":self.user,
					"{pass}":self.password,
					"{ch}":row.id,
					".{container}":target_container
					}, self.conf['iptv_host_vod'])
			ar.append({
				"season_num":row.season_num,
				"episode_num":i,
				"episode_name":row.stream_display_name,
				"stream_url":stream,
				"stream_icon":row.stream_icon
				})
		if err == '':
			err = 'No Episodes'

		if len(list(sql_ch)) == 0:
			ar.append({
				"season_num":0,
				"episode_num":0,
				"episode_name":err,
				"stream_url":'',
				"stream_icon":None
				})

		self.msg(ar)


	def getList(self):

		self.boolVerifyUser("getList")

		if internal_function.isset_dic('remote_movies_use', self.conf) and int(self.conf['remote_movies_use']) == 1:
			mv = core.Movies(self, "getList")
			internal_function.die()



	def myQuran(self, vfor="Quran"):

		self.boolVerifyUser(vfor)

		if internal_function.isset('remote_movies_use', self.conf) and int(self.conf['remote_movies_use']) == 1:
			mv = core.Movies(self, vfor)
			internal_function.die()


	def myRadio(self):

		self.myQuran('Radio')


	def myKids(self):

		self.myQuran('Kids')


	def myMusic(self):

		self.myQuran('Music')


	def myClip(self):

		self.myQuran('Clip')


	def restore(self):

		if self.sn.lower() == "null" or self.mac.lower() == "null" or self.mac.lower() == "02:00:00:00:00:00" or self.mac.lower() == "nu:ll:00:00:00:00" or len(self.sn) < 10 or len(self.sn) < 10:
			self.msg(
				{
				'status':200,
				'message':" Error 2001: We can\'t restore your code. Your Device is not Readable. Please contact Reseller.",
				'code': ''
				})

			internal_function.die()

		qry = "SEELCT code FROM maa_codes WHERE serial='{}' AND mac='{}';".format(self.sn, self.mac)
		result = self.query(qry)
		found = len(list(result))

		if found == 1:
			row = result[0]
			code = row.code.strip()

			self.msg({
				'status':100,
				'message':'Success',
				'code':code
				})
		elif found == 0:
			self.msg({
				'status':200,
				'message':'Error 2002: Your device is not found!',
				'code':''
				})
		elif found > 1:
			self.msg({
				'status':200,
				'message':'Error 2003: we found many devices like yours!',
				'code':''
				})


	def IntroSeriesCat(self):

		qry = parent = ''
		ar = {}

		sql = self.query("SELECT * FROM {}._series_cat WHERE true order by w asc".format(self.prefix))
		i = 0
		for row in sql:
			++i
			#internal_function.extract(row)

			if catimage == "":
				catimage = "http://intro.ps/uploads/logo/movie.png"

			ar.append(
				{
				"cat_id":row.catid,
				"cat_name":row.catname,
				"cat_icon":row.catimage,
				"cat_view_order":str(w)
				})

		self.msg(ar)



	def IntroSeriesList(self):

		qry = ''
		if self.catid == 'all':
			qry = ''
		else:
			qry = " WHERE `catid`=" + int(self.catid)

		ar = []

		sql = self.query("SELECT * FROM {}_series {} order by catid asc, sid desc".format(self.prefix, qry))

		genre = ''
		i = 0
		for row in sql:
			++i
			#internal_function.extract(row)
			if s_photo == "":
				s_photo = "http://intro.ps/uploads/logo/movie.png"

			JSON = json.loads(s_jsondata)
			plot = "n/a"
			cast = "n/a"
			rating = "n/a"
			date = "n/a"

			if internal_function.isset_dic('serial_Plot', JSON):
				plot = strip_tags(JSON['serial_Plot'])
			if internal_function.isset_dic('series_Cast', JSON):
				cast = strip_tags(JSON['series_Cast'])
			if internal_function.isset('series_Rating', JSON):
				rating = strip_tags(JSON['series_Rating'])
			if internal_function.isset('series_Year',JSON):
				date = strip_tags(JSON['series_Year'])

			ar.append({
				"id":row.sid,
				"title":row.s_title,
				"icon":row.s_photo,
				"icon_big":row.s_photo,
				"catid":row.catid,
				"genre":row.genre,
				"plot":plot,
				"cast":cast,
				"rating":rating,
				"director":"n/a",
				"releaseDate":date
				})

		self.msg(ar)



	def IntroSeriesGetDetails(self):

		qry = parent = ''

		sid = intval(self.series_id)

		self.query("UPDATE {}_series SET hits=hits+1 WHERE sid={};".format(self.prefix, sid))

		sqlSeries = self.query("SELECT * FROM {}_series se WHERE sid={}".format(self.prefix, sid))

		row = sqlSeries[0]

		#internal_function.extract(row)
		JSON = json.loads(s_jsondata)

		if s_photo == "":
			s_photo = "http://intro.ps/uploads/logo/movie.png"

		ar = {}

		ar['id'] = row.sid
		ar['title'] =  row.s_title
		ar['trailer'] = row.trailer
		ar['user_rating'] = 0
		ar['likes'] = row.likes
		ar['dislikes'] = row.dislikes

		ar['icon'] = row.s_photo
		ar['plot'] = "n/a"
		ar['cast'] = "n/a"
		ar['rating'] = "n/a"
		ar['date'] = "n/a"

		if internal_function.isset_dic('serial_Plot', JSON):
			ar['plot'] = strip_tags(JSON['serial_Plot'])
		if internal_function.isset('series_Cast', JSON):
			ar['cast'] = strip_tags(JSON['series_Cast'])
		if internal_function.isset('series_Rating', JSON):
			ar['rating'] = strip_tags(JSON['series_Rating'])
		if internal_function.isset('series_Year', JSON):
			ar['date'] = strip_tags(JSON['series_Year'])

		sql = self.query("SELECT * FROM {}_series_seasons WHERE seriesid={} ORDER BY s_num asc;".format(self.prefix, sid))

		i = 0
		arSeasons = []

		if len(list(sql)) == 0:
			arSeasons.append({
				"id":0,
				"title":"Soon...",
				"episodes": self.IntroSeriesGetEpisodes(0)
				})
			arSeasons.append({
				"id":0,
				"title":"Soon...",
				"episodes": self.IntroSeriesGetEpisodes(0)
				})
		else:
			for row in sql:
				++i
				#internal_function.extract(row)

				arSeasons.append({
					"id":row.seasonid,
					"title":row.season_name,
					"episodes":self.IntroSeriesGetEpisodes(int(row.seasonid))
					})

		ar['seasons'] = arSeasons

		self.msg(ar)



	def IntroSeriesGetEpisodes(self, seasonid):

		seasonid = int(seasonid)
		ar = []
		sql = self.query("SELECT * FROM {}_seriesepisodes WHERE seasonid={} ORDER BY epnum ASC;".format(self.prefix, seasonid))

		if len(list(sql)) == 0:
			ar.append({
				"id":0,
				"title":"Soon..." , 
				"episode_name":"Soon...",
				"stream_url":"" ,
				"streams":{"480p":'' , "720p":'', "1080p":'', "4k":''}
				})
			ar.append({
				"id":0,
				"title":"Soon..." , 
				"episode_name":"Soon...",
				"stream_url":"" ,
				"streams":{"480p":'' , "720p":'', "1080p":'', "4k":''}
				})
			return ar
		for row in sql:

			#internal_function.extract(row)

			stream = ''
			stream_480p = internal_function.preg_replace("/\r\n|\r|\n/", '', row.stream_480p)
			stream_720p = internal_function.preg_replace("/\r\n|\r|\n/", '', row.stream_720p)
			stream_1080p = internal_function.preg_replace("/\r\n|\r|\n/", '', row.stream_1080p)
			stream_4k = internal_function.preg_replace("/\r\n|\r|\n/", '', row.stream_4k)

			if stream_4k != "":
				stream = stream_4k
			if stream_1080p != "":
				stream = stream_1080p
			if stream_720p != "":
				stream = stream_720p
			if stream_480p != "":
				stream = stream_480p

			ar.append({
				"id":row.epid,
				"title":"Episode {} {}".format(row.epnum, row.epname),
				"episode_name":"{}".format(row.epname),
				"stream_url":stream ,
				"streams":{"480p":stream_480p , "720p":stream_720p, "1080p":stream_1080p, "4k":stream_4k}
				})


		return ar


	def __del__(self):

		return None


	###Class End

# tClass = core.API6Core()

# def get_post(index = ''):
# 	if not internal_function.isset(request.POST.get("mode", False)):
# 		return request.GET.get("mode", False)
# 	else:
# 		return request.POST.get("mode", False)

# mode = get_post("mode")

# if mode != '' and (hasattr(tClass, mode) and callable(getattr(tClass, mode))):
# 	tClass.mode()
# else:
# 	tClass._die("Error: mode {} not defined.".format(mode))
# 	sys.exit('')













