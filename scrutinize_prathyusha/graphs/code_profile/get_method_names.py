import os
import subprocess
import re
import sys
import shutil


import StringIO
import pstats

#path = '/home/tcs/nova/nova'
path = '/opt/stack/new/nova/nova'
options = "^\+|^[^-]"
temp_log = '/tmp/temp_log'
main_path = os.getcwd()

def analyse_log(log_file, diff_data):
    #shutil.copy(log_file, temp_log)
    #lines = open(temp_log, 'r').readlines()
    #open(temp_log, 'w').writelines(lines[7:-1])
    #log = open(temp_log, 'r')
    matched_data = {}
    p = os.path.split(main_path)[0]+"/stats/req_1/servers-create#16:09:05.800477.prof"
    stream = StringIO.StringIO()
    stats = pstats.Stats(p)
    log = stats.stats.keys()
    for line in log:
        file_path = line[0]
        line_number = line[1]
        method_name = line[2]
        if file_path in diff_data.keys() :
            for method in diff_data[file_path]:
                if line_number in method.keys():
                    print file_path+"   "+method_name+"  at line number "+line_number
                    flag = False
                    if len(matched_data.keys()) > 0 and  file_path in matched_data.keys():
                        for temp_method in matched_data[file_path]:
                            print temp_method
                            if line_number in temp_method.keys():
                                flag = True
                    if not  flag:
                        if not file_path in matched_data.keys():
                            matched_data[file_path] = []
                        matched_data[file_path].append({line_number:method_name})
 
#    matched_data['/home/tcs/nova/nova/service.py']= [{'152':'__init__'}]
    matched_data['/opt/stack/new/nova/nova/service.py']= [{'152':'__init__'}]
    print matched_data
    return matched_data

def grep(data, pattern):
    new_data = []
    for line in data:
        if re.search(options, line):
            new_data.append(line)
    return new_data  


def main(path):
    diff_data = {}
    filename = ''
    os.chdir(path)
    cwd = os.getcwd()
    data = subprocess.check_output(['git','diff', '-U0']).splitlines()
    data = grep(data, options)
    for index in range(len(data)):

        if index == len(data)-2:
            break
        elif '+++' in data[index]:
           filename = cwd+data[index].split('+++ b')[1]
           print 
           print 'Filename: '+filename
           diff_data[filename] = []
        elif '@@' in data[index] and "def" in data[index] and re.search('^\+', data[index+1]):
           method_name = re.search('def.*\(',data[index]).group().split('def')[1].split('(')[0].strip()
           line_number  = re.search('\d+',data[index]).group()
           print 'Method name:',method_name
           print 'Line Number:',line_number
           file_data = {line_number:method_name};
           diff_data[filename].append(file_data)
           counter = 1
           print "newly Added Lines"
           while index+counter != len(data)-2:
               if re.search('^\+ ',data[index+counter]):
                   print data[index+counter]
               else:
                   break
               counter += 1
    
    return diff_data
def render_html(git_path, file_path, matched_data):
     os.chdir(git_path)
     cwd = os.getcwd()
     data = subprocess.check_output(['git','diff', '-U0']).splitlines()
     html_file = open(main_path+"/templates/"+file_path, 'w')
     html_file.writelines("""
        <html>
        <head>
            <!--  Stylesheets --!>
            <link rel="stylesheet" href="/static/css/bootstrap.min.css" />
            <link rel="stylesheet" href="/static/css/style1.css" />
            <style>
                .green{
                   color: green;
                }
                .red{
                   color: red;
                }
                code.prettyprint>div{
                    margin-left:20px;
                    margin-right:20px;
                    padding-left: 30px;
                    background-color: #F0F0D0;
                }
                code.prettyprint>div:first-child{
                    padding-top:20px;
                }
                code>div.default{
                    color: #101010;
                }
                code>div.red:hover{
                    border: 0.5px solid #C0C0C0;
                }
                code>div.green:hover{
                   border: 0.5px solid #C0C0C0;
                }
            </style>
            <!-- Scripts --!>
            <script src="/static/jquery.min.js"></script>
            <script src="/static/bootstrap.min.js"></script>
            <script>
                $(document).ready(function(){
                    $('div').tooltip();
                });
            </script>
        </head>
        <body>
            <ul class="nav nav-tabs custom-nav" role="tablist">
                <li class="custom-li"><a href="/test/">Profiling Report</a></li>
                <li class="active"><a href="./demo1.html">Code Coverage</a></li>
            </ul>
""")
     html_file.writelines("<code class='prettyprint'>")
     filename = ''
     for line in data:
         if '+++ b' in line:
             filename = cwd+line.split('+++ b')[1]
             html_file.writelines("<div class='default'>"+line+"</div>")
         elif '@@' in line and 'def' in line and filename in matched_data.keys():
            flag = False 
            for method in matched_data[filename]:
                 print method
                 if method.keys()[0] in line and method[method.keys()[0]] in line:
                     html_file.writelines("<div class='green' data-toggle='tooltip' data-placement='top' title='Functions that are invoked'>"+line+"</div>")
                     flag = True
            if not flag:
                html_file.writelines("<div class='red' data-toggle='tooltip' data-placement='top' title='Functions that are not invoked'>"+line+"</div>")
         elif '@@' in line and 'def' in line:
             html_file.writelines("<div class='red' data-toggle='tooltip' data-placement='top' title='Functions that are not invoked'>"+line+"</div>")
         else:
             html_file.writelines("<div class='default'>"+line+"</div>") 
     html_file.writelines('</code></body></html')
     html_file.close()
             
if __name__ == '__main__':
    if len(sys.argv)!=4:
        print """
Usage: python  get_names.py <path_to_root_git_repository> <log_file_to_analyze>
Both the arguments are mandatory
    """
    else:
        diff_data = main(sys.argv[1])
        diff_data["/opt/stack/python-glanceclient/glanceclient/openstack/common/apiclient/base.py"] = [{"205":"ManagerWithFind"}]
        print diff_data
        matched_data = analyse_log(sys.argv[2],diff_data)
        render_html(sys.argv[1], sys.argv[3], matched_data) 
