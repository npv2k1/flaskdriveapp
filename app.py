from flask import Flask, request, render_template

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
app = Flask(__name__)
import time
@app.route('/')
def my_form():
    return render_template('f1.html')

# @app.route('/', methods=['POST'])
# def my_form_post():
#     text = request.form['email']
#     processed_text = text.upper()
#     return processed_text

# @app.route('/')
# def hello_world():
#     return 'Hello Worxld!'
@app.route('/', methods=['POST'])
def mains():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API

    data={
        "role":'organizer',
        "type": "user",
        "emailAddress": request.form['email']
    }
    datacreate={
        'name':request.form['pass']
    }
    try:
        drive = service.drives().create(body=datacreate,requestId=request.form['email'],fields='id').execute()
        #request_id = str('68489849')
        #ex: '0AChZcuKJ1pHhUk9PVA'
        drive1 = service.permissions().create(body=data,fileId=drive['id'],supportsAllDrives=True,supportsTeamDrives=True).execute()
        #ex
        drive2 = service.permissions().delete(fileId=drive['id'],permissionId='15469801397911266740', supportsAllDrives=True,supportsTeamDrives=True).execute()
    except :
        return "<script>alert('Không thành công. Địa chỉ email này đã tạo hoặc quá tải vui lòng thử lại sau it phút')</script>"
    return f"Thành công! drive của bạn <a>https://drive.google.com/drive/u/0/{drive['id']}</a>"

if __name__ == '__main__':
    app.run(debug=True)

