import hashlib
import urllib.request as urllib2
import datetime
import os
import platform
import time
import datetime
import calendar
import urllib.parse
import base64
import json
import re 
import locale
import inspect
import sys
from django.db import connection
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

def md5(s, raw_output=False):
    """Calculates the md5 hash of a given string"""
    res = hashlib.md5(s.encode())
    if raw_output:
        return res.digest()
    return res.hexdigest()

def file_get_contents(filename, use_include_path = 0, context = None, offset = -1, maxlen = -1):
    if (filename.find('://') > 0):
        ret = urllib2.urlopen(filename).read()
        if (offset > 0):
            ret = ret[offset:]
        if (maxlen > 0):
            ret = ret[:maxlen]
        return ret.decode("utf-8")
    else:
        fp = open(filename,'rb')
        try:
            if (offset > 0):
                fp.seek(offset)
            ret = fp.read(maxlen)
            return ret.decode("utf-8")
        finally:
            fp.close( )		

def file_mtime(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getmtime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_mtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def file_write(filename, content):
    f = open(filename, 'w')
    f.write(content)
    f.close()



def date(unixtime, format = '%m/%d/%Y %H:%M'):
    d = datetime.datetime.fromtimestamp(int(unixtime))
    return d.strftime(format)

def isset(variable):
    if variable:
        return True
    else:
        return False
    
	#return variable in locals() or variable in globals()



# str_replace for dictionary

def isset_dic(val, dic):
    if str(val) in dic:
        return True
    else:
        return False


def multiple_replace(dic, text): 
    pattern = "|".join(map(re.escape, dic.keys()))
    return re.sub(pattern, lambda m: dic[m.group()], text) 

def uniqid(prefix = ''):
    return prefix + hex(int(time()))[2:10] + hex(int(time()*1000000) % 0x100000)[2:7]

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

def get_domain(url):
    return urlparse.urlparse(url).netloc

# This seems to work ok
def var_export(obj, ret_val = False) :
    import os,sys,pprint
    if ret_val == False :
        pprint.pprint(obj)
        return None
    fn = '/path/to/temp/file'
    temp = sys.stdout             # store original stdout object for later
    sys.stdout = open(fn, 'w')    # redirect all prints to temp file
    pprint.pprint(obj)
    sys.stdout.close()
    sys.stdout = temp             # restore print commands to interactive prompt
    return open(fn, 'r').read()

def number_format(num, places=0):
    return locale.format("%.*f", (places, num), True)

def file_put_contents(filename, data):
    #All  versions of Python

    f = open(filename, 'a+')
    f.write(data)
    f.close()

def microtime(get_as_float = False) :
    d = datetime.datetime.now()
    t = time.mktime(d.timetuple())
    if get_as_float:
        return t
    else:
        ms = d.microsecond / 1000000.
        return '%f %d' % (ms, t)

def urldecode(data):
    return urllib.parse.unquote_plus(data)

def base64_decode(data):

    return base64.b64decode(data).decode('utf-8')

def base64_encode(data):
    #return base64.encodestring(data)

    return base64.encodebytes(data.encode('utf-8')).strip()

def json_decode(data):
    return json.loads(data)

def preg_replace(pattern, replacement, subject):
    return re.sub(pattern, replacement, subject)

def array_merge( first_array , second_array ):
    if isinstance( first_array , list ) and isinstance( second_array , list ):
        return first_array + second_array
    elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
        return dict( list( first_array.items() ) + list( second_array.items() ) )
    elif isinstance( first_array , set ) and isinstance( second_array , set ):
        return first_array.union( second_array )
    return False

def die(str='die'):
    sys.exit(str)

def substr (s, start, length = None):
    if len(s) >= start:
        if start > 0:
            return False
        else:
            return s[start:]

    if not length:
        return s[start:]
    elif length > 0:
        return s[start:start + length]
    else:
        return s[start:length]

def extract(vars):
    caller = inspect.stack()[1][0] # caller of extract()
    for n, v in list(vars).items():
        caller.f_locals[n] = v   # NEVER DO THIS ;-)

def real_qry_res(qry):
    cursor = connection.cursor()
    cursor.execute(qry)
    return cursor.fetchall()
