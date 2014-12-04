import StringIO
import collections
import os
import shutil
import pstats
import json
from scrutinize import config

#path = '/home/prathyusha/scrutinize/stats-dump'  # remove the trailing '\'
#print os.path.split(os.getcwd())
path = config.path
print path

file_data = {}
file_names = []
file_dict = {}
file_dict1 = {}

def time(self):
    stream = StringIO.StringIO()
    stats = pstats.Stats(p, stream=stream)
    opt_stats = stats.print_stats('opt')   
    
entry_points = ["show","show","create","show","show","show","external_instance_event","create","run_instance"]
for dir_entry in os.listdir(path):
    file_names.append(dir_entry)
#print file_names

mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
file_dict1 = list(sorted(os.listdir(path), key=mtime))

#print file_dict1
i = 0
count = 1
for fname in file_dict1:
    if entry_points[i] in fname:
        if not os.path.exists(os.path.split(os.getcwd())[0]+'/stats/req_%s'%str(count)):
            os.makedirs(os.path.split(os.getcwd())[0]+'/stats/req_%s'%str(count))
        shutil.copy(os.path.split(os.getcwd())[0]+'/stats-dump/'+fname, \
                       os.path.split(os.getcwd())[0]+'/stats/req_%s/%s'%(str(count),fname))
    i=i+1
    if i == len(entry_points):
        count = count+1
        i = 0
    
    

def explore(starting_path):
  alld = {'': {}}

  for dirpath, dirnames, filenames in os.walk(starting_path):
    d = alld
    dirpath = dirpath[len(starting_path):]
    for subd in dirpath.split(os.sep):
      based = d
      d = d[subd]
    if dirnames:
      for dn in dirnames:
        d[dn] = {}
    else:
      based[subd] = filenames
  return alld['']

def get_folder():
    result_lst = list()
#    dir_list = explore('/home/prathyusha/scrutinize/stats')
    dir_list = explore('/opt/stack/new/scrutinize/stats')
    for key in dir_list.keys():
        total_time = 0
        request_list = dict() 
        for fname in dir_list[key]:
#            p = '/home/prathyusha/scrutinize/stats/%s/%s'%(key,fname)
            p = '/opt/stack/new/scrutinize/stats/%s/%s'%(key,fname)
            stream = StringIO.StringIO()
            stats = pstats.Stats(p)
            stats.sort_stats('cum')
            time = stats.stats[stats.fcn_list[0]][3]
            total_time = total_time+float(time)
        request_list["request_id"] = key
        request_list["time"] = total_time
        result_lst.append(request_list)
    print result_lst
    return {'body' : result_lst }


#get_folder()


def get_request_data(req_id):
#    dir_list = explore('/home/prathyusha/scrutinize/stats')
    dir_list = explore('/opt/stack/new/scrutinize/stats')
    service_list = list()
    #print dir_list
    for key in dir_list.keys():
        total_time = 0
        if key == req_id:
        #print dir_list[key] 
            for fname in dir_list[key]:
                service_names = dict()
#                p = '/home/prathyusha/scrutinize/stats/%s/%s'%(key,fname)
                p = '/opt/stack/new/scrutinize/stats/%s/%s'%(key,fname)
                stream = StringIO.StringIO()
                stats = pstats.Stats(p)
                stats.sort_stats('cum')
                time = stats.stats[stats.fcn_list[0]][3]
                #fname = fname.split("#")[0] 
                service_names["fname"] = fname 
                service_names["time"] = float(time)
                service_list.append(service_names) 
    print service_list
    return {'body' : service_list }




get_request_data("req_1")








#p  ='./stats_stump/'
#stream = StringIO.StringIO()
#stats = pstats.Stats(p, stream=stream)
#opt_stats = stats.print_stats('opt')

"""
    p = fname
    stream = StringIO.StringIO()
    stats = pstats.Stats(p, stream=stream)
    tottime = stats.print_stats('tottime')
    time_list = tottime.splitline()
    time = time_list[-1].split(' seconds')[0].split(' ')[-1]
"""
