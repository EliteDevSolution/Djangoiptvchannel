#files.py
from django import forms
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
import hashlib

 
class Apicore:
    
    CacheFile = ''
    CacheTime = 3600
    CacheEnabled = True
    API = None

    def __init__(self, API, mode):
    	
    	self.API = API
    	data = []
    	data['u'] = API.user
    	data['p'] = API.passwd
    	data['e'] = API.data_expire
    	data['mode'] = mode
    	data['parent'] = API.catid
    	data['catid'] = API.catid
    	data['movie_id'] = API.movie_id
    	data['series_id'] = API.series_id
    	data['search'] = API.search
    	data['year'] = API.year
    	data['gener'] = API.gener
    	self.SetCacheFile(data)

    	#Rating
    	cutomData = []


    
    def SetCacheFile(data):

    	self.CacheFile = "./cache/"
    	self.CacheFile = "vod_["
    	self.CacheFile = data['mode'] + "]_"

    	if data['catid'] != "":
    		self.CacheFile += "CatID" + data['catid'] + "_"

    	if data['mode'] == "series_details" and int(data['series_id']) != 0:
    		self.CacheFile += "SeriesID" + data['series_id'] + "_"

    	self.CacheFile += hashlib.md5(self.CacheFile + "rareMicra") + ".txt"


			



			























		

