import os
import subprocess
import re
import sys
import shutil

options = "^\+|^[^-]"
temp_log = '/tmp/temp_log'

def count_spaces(data):
    counter = 0
    for index in range(len(data)):
        if data[index]==' ':
            counter+=1
        else:
            break
    return counter
def method_number(filename, line_number):
    with open(filename, 'r') as temp_file:
        data = temp_file.readlines()
    counter = 1
    line_number = int(line_number[1:])
    print line_number
    while(line_number-counter>=0):
        if 'def ' in data[line_number-counter]:
            print data[line_number-counter]
            print line_number-counter
            return line_number - counter
        counter += 1

def add_coverage(diff_data):
    for filename in diff_data.keys():
        #import_flag = True
        if len(diff_data[filename])==0:
            continue
        with open(filename, 'r') as temp_file:
            data = temp_file.readlines()
        data[0] = "from profilehooks import coverage\n"+data[0]
        for line_number in diff_data[filename]:
            method_line_number = method_number(filename, line_number)
            #import_statement = ''
            #if import_flag:
            #    import_statement = " "*count_spaces(data[method_line_number])+"from profilehooks import coverage\n"
            #    import_flag = False
                #data[method_line_number] = " "*count_spaces(data[method_line_number])+"@coverage\n"+data[method_line_number]
            data[method_line_number] = " "*count_spaces(data[method_line_number])+"@coverage\n"+data[method_line_number]
        with open(filename, 'w') as output_file:
            output_file.writelines(data)
        
def remove_coverage(git_path):
    diff_data = generate_diff(git_path)
    for filename in diff_data.keys():
        if len(diff_data[filename])==0:
            continue
        else:
            with open(filename, 'r') as temp_file:
                 data = temp_file.readlines()
            for index in range(len(data)):
                if '@coverage' in data[index] or 'from profilehooks import coverage' in data[index]:
                    data[index] = ''

        with open(filename, 'w') as output_file:
            output_file.writelines(data)        


def analyse_log(log_file_dir, diff_data, matched_data):
    for file in os.listdir(log_file_dir):
        data = open(log_file_dir+'/'+file, 'r').readlines()
        for index in range(len(data)):
            if 'Filename' in data[index]:
                filename = data[index].split(':')[1].replace('\n','',1)
                matched_data[filename] = matched_data[filename] if filename in matched_data.keys() else []
            elif 'Methodname' in data[index]:
                methodname = data[index].split(':')[1].replace('\n','')
            elif '+++++++' in data[index]:
                counter = 0
                temp_list = []
                while index+counter != len(data):
                    if re.search('^\+\+\+\+\+\+\+',data[index+counter]):
                        temp_string = data[index+counter].replace('+++++++','',1)
                        temp_list.append(temp_string.replace('\n',''))
                    counter += 1
                matched_data[filename].append({methodname:temp_list})
                break   

    return matched_data

def grep(data, pattern):
    new_data = []
    for line in data:
        if re.search(options, line):
            new_data.append(line)
    return new_data  


def generate_diff(path):
    diff_data = {}
    filename = ''
    os.chdir(path)
    cwd = os.getcwd()
    data = subprocess.check_output(['git','diff', '-U0']).splitlines()
    data = grep(data, options)
    for index in range(len(data)):

        if index == len(data)-1:
            break
        elif '+++' in data[index]:
           filename = cwd+data[index].split('+++ b')[1]
           if not '.py' in filename:
               continue
           diff_data[filename] = []
        elif '@@' in data[index] and ('def' in data[index] or 'class' in data[index]):
            if 'class' in data[index]:
                method_name = re.search('class.*\(',data[index]).group().split('class')[1].split('(')[0].strip()
            else:
                method_name = re.search('def.*\(',data[index]).group().split('def')[1].split('(')[0].strip()
            line_number  = re.search('\+\d+',data[index]).group()
            flag = False
            counter = 1
            while index+counter <= len(data)-1:  
                if re.search('^\+ ',data[index+counter]) and not '@coverage' in data[index+counter]:
                   flag = True
                elif '@@' in data[index+counter] or re.search('^diff', data[index+counter]):
                    break
                counter += 1

            if flag:
                diff_data[filename].append(line_number)

    
    return diff_data
def render_html(git_path, file_path, matched_data):
     os.chdir(git_path)
     cwd = os.getcwd()
     data = subprocess.check_output(['git','diff', '-U0']).splitlines()
     html_file = open(file_path, 'w')
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
                .orange{
                    color: orange;
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
		code>div.orange:hover{
                   border: 0.5px solid #C0C0C0;
                }
            </style>
            <!-- Scripts --!>
            <script src="/static/js/jquery.min.js"></script>
            <script src="/static/js/bootstrap.min.js"></script>
            <script>
                $(document).ready(function(){
                    $('div').tooltip();
                });
            </script>
        </head>
        <body>
            <ul class="nav nav-tabs custom-nav" role="tablist">
                <li class="custom-li"><a href="scrutinize">Profiling Report</a></li>
                <li class="active"><a href="code_coverage">Code Coverage</a></li>
		<li><a href="rally">Rally Graph</a></li>
            </ul>
""")
     html_file.writelines("<code class='prettyprint'>")
     filename = ''
     flag_method = False
     for line in data: 
        if '+++ b' in line:
            filename = cwd+line.split('+++ b')[1]
            html_file.writelines("<div class='default'>"+line+"</div>")
            #print filename
        elif '@@' in line and ('def' in line or 'class' in line):
            if 'def' in line:
                method_name = re.search('def.*\(',line).group().split('def')[1].split('(')[0].strip()
            else:
                method_name = re.search('class.*\(',line).group().split('class')[1].split('(')[0].strip()
            flag_method = True
            html_file.writelines("<div class='default'>"+line+"</div>")
            #print method_name
        elif '@@' in line and not 'def' in line:
             flag_method = False
             html_file.writelines("<div class='default'>"+line+"</div>")
        elif re.search('^\+', line) and not re.search('^\+\+\+ b',line):
            temp_line = line.replace('+','',1)
            if flag_method and filename in matched_data.keys() and len(matched_data[filename])>0:
                for method_dict in matched_data[filename]:
                    key = method_dict.keys()[0]
                    if method_name == key and temp_line in method_dict[key]:
                        html_file.writelines("<div class='green'>"+line+"</div>")
                    elif method_name == key and not temp_line in method_dict[key]:
                        html_file.writelines("<div class='red'>"+line+"</div>")
                    #else:
                    #    html_file.writelines("<div class='orange'>"+line+"</div>")
            else:
                html_file.writelines("<div class='orange'>"+line+"</div>")
        else:
            html_file.writelines("<div class='default'>"+line+"</div>")
          





if __name__ == '__main__':
    if len(sys.argv)<3:
        print """
Usage: python  code_coverage.py <path_to_root_git_repository> <log_file_to_analyze>
Both the arguments are mandatory
    """


    else:
        diff_data = generate_diff(sys.argv[1])
        print diff_data
        matched_data = {}
        add_coverage(diff_data)
        matched_data = analyse_log(sys.argv[2],diff_data, matched_data)
        print matched_data
        render_html(sys.argv[1], sys.argv[3], matched_data) 
        remove_coverage(sys.argv[1])
