from flask import Flask,jsonify
from flask import render_template
app = Flask(__name__)

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
import os
import sys
original_path = os.path.split(os.getcwd())[0]
sys.path.append(original_path)

import scrutinize_analyzer as s_app
import code_profile.get_method_names as cd_coverage
import code_profile.rally_data as rd
import json

config = ''
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route("/", methods=['POST','GET'])
@crossdomain(origin='*')
def hello():
    #s_app.main(config)
    result =  s_app.get_folder(config)
    print type(result)
    print result
    
    file  = open(os.getcwd()+'/static/root.json', 'w')
    json.dump(result, file)
    file.close()
    return jsonify(dict(result))

@app.route("/req/<id>", methods=['GET'])
@crossdomain(origin='*')
def hello_req(id):
    result =  s_app.get_request_data(id)
    print result
    file  = open(os.getcwd()+'/static/'+id+'.json', 'w')
    json.dump(result, file)
    return jsonify(dict(result))

@app.route("/test/")
def t():
    return render_template('scrutinize.html')

@app.route("/test/code_coverage")
def code_coverage():
    return render_template('index.html')

@app.route("/rally",methods=['POST','GET'])
@crossdomain(origin='*')
def rally_data():
    data_list = rd.get_data()
    print "rally_data"
    print data_list
    file  = open(os.getcwd()+'/static/rally.json', 'w')
    json.dump(data_list, file)
    return jsonify(data_list)

@app.route("/test/rally.html")
def rally_render_graph():
    return render_template('rally.html')



if __name__ == '__main__':
    if len(sys.argv)<3:
       print "usage: python test.py [port] [json file path for command]"
       sys.exit()
    print len(sys.argv)
    port = sys.argv[1] if len(sys.argv)>=2 else 8989
    print sys.argv[2]
    with open(sys.argv[2]) as f: 
        config = json.load(f)
    print config
    s_app.main(config)
    app.run(port=int(port))
