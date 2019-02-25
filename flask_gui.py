from flask import Flask, render_template, request, redirect, Response
import sys
import json
import requests
import hashlib

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
            print(response1.text, 'odowid')
            global all_files
            all_files = json.loads(json.loads(response1.text))

            return render_template('views/gui.html', all_files=all_files, len=len(all_files))
        else:
            print(response)
            error = 'Not authenticated'
            return render_template('views/login.html', error=error)
        print('Login')
    return render_template('views/login.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        file = request.files['upload_button']
        data = file.read()
        print(dir(file))
        with open(file.filename, 'wb') as f:
            f.write(data)
        raw_args = ['upload', file.filename]

        main(oauth_json_string=oauth_json, raw_args=raw_args, email_list=[
            'sheet-disk@sheet-disk-230910.iam.gserviceaccount.com'
        ])
        json_str = None
        with open(file.filename+'.json', 'r') as f:
            json_str = f.read()

        data = {
            'auth_dict': auth_dict,
            'json_str': json_str
        }
        print(data)
        response = requests.post(url=BASE_URL+'/upload', data=data)

        messages = 'failed'
        print("status_code  ", response.status_code)
        print("json ", response.json())
        if response.status_code == 200:
            messages = 'Successful'
            print('Login')
            
        return render_template('views/gui.html', messages=messages)


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
    print('sognup')
    if request.method == 'POST':
        email = request.form['email']
        pass1 = request.form['pass']
        pass2 = request.form['pass1']
        json_data = request.files['creds']
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
    print('thwt')
