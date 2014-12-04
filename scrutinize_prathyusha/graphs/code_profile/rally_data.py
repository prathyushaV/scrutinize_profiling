#! /usr/bin/python
import mysql_interface
import json
def get_data():
#    msi = mysql_interface.MySQLInterface("localhost","rally","root", "openstack")
    msi = mysql_interface.MySQLInterface("127.0.0.1","rally","root", "secretmysql")
    task_data_list = []
    task_data = msi.get_rows("task_results")
    print task_data
    if task_data:
        for i in range(0,len(task_data)):
           task_data_list.append(eval(task_data[i][0])['raw'])
        task_json = {'body' : task_data_list}
        print "rally is executed" 
    else:
        print "rally not executed"
        task_json = {}
    return task_json

get_data()
