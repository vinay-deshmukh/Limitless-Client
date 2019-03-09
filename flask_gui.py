from flask import Flask, render_template, request, redirect, Response, jsonify
import time
import os
import sys
import json
import requests
import hashlib
import threading
from sheet_disk.limitless import get_status, init_progress

'''
sheet-disk@sheet-disk-230910.iam.gserviceaccount.com
'''

sys.path.insert(0, "/home/rishabh/Downloads/Sheet-Disk-master")
sheet_disk_path = '../sheet_disk/cli.py'
app = Flask(__name__)

ROOT = '127.0.0.2'
PORT = 5000
BASE_URL = 'http://127.0.0.1:' + str(PORT)

from sheet_disk.sheet_disk import main

oauth_json = None
auth_dict = None
all_files = None

progress_bool = False


@app.route('/', methods=['POST', 'GET'])
def index():
    print('index')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        body = {
            'user': email,
            'pwd': hash_data(password)
        }
        response = requests.post(BASE_URL + '/login', json=body)
        if response.status_code == 200:
            global oauth_json
            global auth_dict
            auth_dict = response.json()
            oauth_json = json.loads(response.json())['oauth_json_string']
            print('Type: ', type(oauth_json))
            response1 = requests.post(BASE_URL + '/get_files', data={'auth_dict': auth_dict})
            global all_files
            all_files = json.loads(json.loads(response1.text))

            return render_template('views/progress_bar.html', all_files=all_files, len=len(all_files))
        else:
            print(response)
            error = 'Not authenticated'
            return render_template('views/login.html', error=error)
        print('Login')
    return render_template('views/login.html')

'''
@app.route('/upload/progress', methods=['GET'])
def progress():
	return jsonify(progress=request.args.get('prog'))


def start_upload(oauth_json, raw_args, receivers, data):
    main(oauth_json_string=oauth_json, raw_args=raw_args, email_list=receivers)

    response = requests.post(url=BASE_URL+'/upload', data=data)

    messages = 'failed'
    print("status_code  ", response.status_code)
    print("json ", response.json())
    if response.status_code == 200:
        messages = 'Successful'
        print('Login')
'''



def get_progress():
	prog = 0
	while True:
		prog = int(get_status().percent())
		#print(prog)
		if prog == 100:
			break
		#requests.get(url=BASE_URL+'/upload' + '?prog=' + str(int(prog)))

@app.route('/real_progress', methods=['POST'])
def real_progress():
    print('=' * 50)
    a = int(get_status().percent())
    print('Progress:', a)
    print('=' * 50)
    return str(a)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        #global progress_bool
        #if not progress_bool:
        file = request.files['file_upload']
        receivers = request.form['receivers']
        data = file.read()
        print(dir(file))
        with open(file.filename, 'wb') as f:
            f.write(data)
        receivers = receivers.split(';')
        progress_bool = True
        #file_path = os.path.abspath(file)
        raw_args = ['upload', file.filename]

        main(oauth_json_string=oauth_json, raw_args=raw_args, email_list=receivers)

        json_str = None
        with open(file.filename +'.json', 'r') as f:
            json_str = f.read()

        data = {
            'auth_dict': auth_dict,
            'json_str': json_str
        }

        messages = 'failed'
        response = requests.post(url=BASE_URL+'/upload', data=data)
        if response.status_code == 200:
        	messages = 'Successful'
        init_progress()
        #print(get_status().percent())
        return render_template('views/progress_bar.html', messages=messages)
        #else:
            #prog = Progress().percent()
            #return jsonify(progress=prog)

    if request.method == 'GET':
    	return jsonify(progress=request.args.get('prog'))
            


def hash_data(d):
	hash = hashlib.sha3_512(('bmrv' + d).encode('utf-8')).hexdigest()
	return hash


@app.route('/download', methods=['POST', 'GET'])
def download():
    if request.method == 'GET':
        id = int(request.args.get('id'))
        downloading_file = json.dumps(all_files[id])
        with open('crypt.json', 'w') as f:
            f.write(downloading_file)
        raw_args = ['download', all_files[id]['name'], 'crypt.json']
        main(oauth_json_string=oauth_json, raw_args=raw_args)
        messages = "successful"
        return render_template('views/gui.html', messages=messages, all_files=all_files, len=len(all_files))


@app.route('/register', methods=['POST', 'GET'])
def signup():
    print('signup')
    if request.method == 'POST':
        email = request.form['email']
        pass1 = request.form['pass']
        pass2 = request.form['pass1']
        json_data = request.files['credentials']
        print('Hello')
        if pass1 == pass2:
            try:
                creds = json_data.read().decode('utf-8')
                url = BASE_URL + '/register'
                body = {
                    'user': email,
                    'pwd': hash_data(pass1),
                    'json_oauth': creds
                }
                response = requests.post(url, json=body)
                if response.status_code == 200:
                    return redirect("/")
                else:
                    error = 'something went wrong'
                    return render_template('views/signup.html', error=error)
            except Exception as e:
                print(e)
                error = 'Not a json'
                return render_template('views/signup.html', error=error)
        print('Login')
    return render_template('views/signup.html')


if __name__ == '__main__':
    app.run(host=ROOT, port=PORT, debug=True)
