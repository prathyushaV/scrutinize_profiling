import httplib
import os

def send_request():
    os.chdir('stats')
    list_dirs = os.listdir('.')
    #list_dirs = [name for name in list_dirs if 'req' in name]
    httpServ = httplib.HTTPConnection("127.0.0.1", 8989)
    httpServ.connect()

    httpServ.request('GET', '/')
    response = httpServ.getresponse()

    httpServ.request('GET', '/rally')
    response = httpServ.getresponse()
   
    for i in range(0,len(list_dirs)):
	httpServ.request('GET', '/req/'+list_dirs[i])
	response = httpServ.getresponse()		

send_request()
