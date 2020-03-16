import configparser as ConfigParser


configdata = {
    'mysql': {'host': 'localhost', 'user': 'root',
              'password': '', 'database': '2018_iptv'},
    '_CFG': {
	'debug':False,
	'debug_post':True,
	'XOR':"yes",
	'XOR_KEY':"KvRmwk5&SuZz",
	'enable_group':'Yes',
	'group_id':1,
	'UseIntroSeries':'No',
	'group_id':1,
	'update_password':"Yes",
	'user_stream_source':'No',
	'vod':"No",
	'cache_type':"RDS",
	'portalName':"PortalName",
	'conf':{}
	}
}


config = ConfigParser.ConfigParser()
config.read_dict(configdata)




