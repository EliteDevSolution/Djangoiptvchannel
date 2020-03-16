"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from app.system import core
from app.system import apiv6
from django.http import JsonResponse
import json
import sys

def api(request):
        
    m_method = ''
    if request.method == 'GET':
        m_method ="GET"
  
    elif request.method == 'POST':
        m_method ="POST"

    if request.META.get('HTTP_AUTHORIZATION',False):
        response = request.META.get('HTTP_AUTHORIZATION')
    else:
        response = {'data': 1}

    if m_method == 'GET' and not core.internal_function.isset_dic('json', request.GET):
        return HttpResponse('Key Error')
    elif m_method == 'POST' and not core.internal_function.isset_dic('json', request.POST):
        return HttpResponse('Key Error')






    #tClass = apiv6.APIv6(request)

    #print (request.POST['json'])
    #print (request.environ['REMOTE_ADDR'])
    tClass = apiv6.APIv6(request)

    str_encode = tClass.result
    str_decode = core.API6Core.runXOR(request, str_encode)
    #print ("encode: " + str_encode + "\n")
    #print ("decode: " + str_decode)
    json_decode = json.loads(str_decode)
    #sys.exit(json_decode)


    #return JsonResponse(json_decode, safe=False)
    return HttpResponse(str_encode)


def curl_api(request):
        
    apitest =  core.internal_function.microtime(True)
    print(apitest)

    data = {
    'url':'http://localhost:8081/API-V6.php',
    'xor':'KvRmwk5&SuZz',
    'code':'114097222516',
    'mac':'02:03:10:03:11',
    'sn':'1234512345',
    'chipid':'000000',
    'model':'000000',
    'firmware_ver':'000000'
    }

    url = data['url']
    XOR_key = data['xor']
    mode = {}
    #mode['active'] = {}
    mode['packages'] = {}
    #mode['movies_cat'] = {}
    #mode['movies_list'] = {'catid':'35'}
    #mode['series_cat'] = {}
    
    ###---------------Second step modules------------------###
    #mode['movies_info'] = {'movie_id':70};
    #mode['series_cartoon'] = {};
    #mode['series_list'] = {'catid':-1};
    #mode['series_info'] = {'series_id':538};


    res = ''

    for theMode, vars in mode.items():
        newData = {}
        newData['mode'] = theMode
        newData.update(data)
        if len(vars) > 0:
            newData.update(vars)
        jsonval = json.dumps(newData)
        encrypted_data = core.API6Core.runXOR(request, jsonval)
        encrypted_data = core.internal_function.base64_encode(encrypted_data)
        encrypted_data = str(encrypted_data, "utf-8")

        #encrypted_data.decode('utf-8')

        #Python request
        res = encrypted_data
        #jsonRow = core.API6Core.runXOR(None, encrypted_data);
        #json1 = core.internal_function.json_decode(jsonRow);




        print (res)






    #if core.internal_function.isset(request.GET):
    #    print(header)
    #Here Logic API
    #apiprocess = Apicore()
    #print(apiprocess.username)

    #print (request.environ)
    #print (request.method)


    
    if request.method == 'GET':
        a ="GET"
    
  
  
    elif request.method == 'POST':
        a ="POST"


    if request.META.get('HTTP_AUTHORIZATION',False):
        response = request.META.get('HTTP_AUTHORIZATION')
    else:
        response = {'data': 1}
    #print (res) 
    #return JsonResponse(response);
   # if request.GET.get('a', False):

   #     response = '{status: True}'
   # else:
   #     response = '{status: False}'
    

    # response = "hola"
  
    
   
    
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render( # here Send Message
        request,
        'app/api.html',
        {   
            'response' :  response,
            'res' : res,
            'title':'API',
            'year':datetime.now().year,
        }
    )


def home(request):

    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
   
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

@ensure_csrf_cookie


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
