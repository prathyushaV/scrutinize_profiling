import StringIO
import collections
import os
import shutil
import pstats
import json

original_path = os.path.split(os.getcwd())[0]
path = os.path.split(os.getcwd())[0]+'/stats-dump'  
file_data = {}
file_names = []
file_dict = {}
file_dict1 = {}
    
config = ""
sc_count = 0

def sort_files(filenames):
    file_list = []
    new_file_list = []
    file_dict = {}
    for filename in filenames:
        timestamp = filename.split("#")[1]
        file_dict[timestamp] = filename
        file_list.append(file_dict)
    keys_list = sorted(file_dict)
    for key in keys_list:
        new_file_list.append(file_dict[key])
    return new_file_list


def main(config):
    sc_count = 0
    config = config
    scenario = config["scenario"]
    entry_points = eval(scenario[sc_count]["entry_points"])
    for dir_entry in os.listdir(path):
        file_names.append(dir_entry)
    print file_names

    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    #file_dict1 = list(sorted(os.listdir(path), key=mtime))
    file_dict1 = sort_files(file_names)
    print file_dict1
    i = 0
    count = 0
    if os.path.isdir(original_path+'/stats/'):
        shutil.rmtree(original_path+'/stats/')
    if not os.path.isdir(original_path+'/stats/'):
        os.makedirs(original_path+'/stats/')
    
    for fname in file_dict1:
        if "os-" in fname or 'show' in fname or 'index' in fname:
            continue
        if "create" in fname:
            if scenario[sc_count]["count"] > 0:
                scenario[sc_count]["count"] = scenario[sc_count]["count"] - 1
            else:
                break
            if sc_count < len(scenario)-1:
                if scenario[sc_count]["count"] == 0:
                    sc_count = sc_count+1
                    entry_points = eval(scenario[sc_count]["entry_points"] )
            count = count+1
            i = 0
        if count==0:
            continue

        if fname.split("#")[0]:# in entry_points:
            print fname
            if not os.path.exists(original_path+'/stats/%s_%s'%(scenario[sc_count]["name"],str(count))):
                os.makedirs(original_path+'/stats/%s_%s'%(scenario[sc_count]["name"],str(count)))
            shutil.copy(original_path+'/stats-dump/'+fname, \
                       original_path+'/stats/%s_%s/%s'%(scenario[sc_count]["name"],str(count),fname))
        #    i = i+1
        #else:
        #    i == len(entry_points)
        i=i+1
        #if i == len(entry_points):
        #    if scenario[sc_count]["count"] > 0:
        #        scenario[sc_count]["count"] = scenario[sc_count]["count"] - 1
        #   else:
        #        break
        #    if sc_count < len(scenario)-1:
        #        if scenario[sc_count]["count"] == 0:
        #            sc_count = sc_count+1
        #            entry_points = eval(scenario[sc_count]["entry_points"] )
        #    count = count+1
        #    i = 0

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
      based[subd] = sort_files(filenames)
  return alld['']
#Methiod to divide scenarios and calculate time
def get_folder(config):
    result_lst = list()
    path1 = original_path+'/stats'
    dir_list = explore(path1)
    for key in dir_list.keys():
        total_time = 0
        request_list = dict() 
        for fname in dir_list[key]:
            p = original_path+'/stats/%s/%s'%(key,fname)
            stream = StringIO.StringIO()
            stats = pstats.Stats(p)
            stats.sort_stats('cum')
            time = stats.stats[stats.fcn_list[0]][3]
            total_time = total_time+float(time)
        request_list["request_id"] = key
        request_list["time"] = total_time
        request_list["req_no"] = key.split("_")[-1]
        result_lst.append(request_list)
    print "result_lst"
    print result_lst
    return {config["scenario"][0]["name"] : result_lst }

#get_folder(config)
#Method to get functions that are executed
def get_request_data(req_id):
    path1 = original_path+'/stats'
    dir_list = explore(path1)
    service_list = list()
    for key in dir_list.keys():
        total_time = 0
        if key == req_id:
            for fname in dir_list[key]:
                service_names = dict()
                p = original_path+'/stats/%s/%s'%(key,fname)
                stream = StringIO.StringIO()
                stats = pstats.Stats(p)
                stats.sort_stats('cum')
                time = stats.stats[stats.fcn_list[0]][3]
                if time >= 0.1:
                    service_names["fname"] = fname 
                    service_names["time"] = float(time)
                    service_list.append(service_names) 
    print "service_list"
    print service_list
    return {'body' : service_list }

