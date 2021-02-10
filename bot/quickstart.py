from __future__ import print_function

import pickle
import os.path
import mimetypes
import base64

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.text import MIMEText


SCOPES = ['https://mail.google.com/']

def get_service():
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    return service

def send_message(service,user_id,message):
    try:
        message = service.users().messages().send(userId=user_id,body=message).execute()
        print('Message id')
        return message
    except Exception as e:
        print('an error occured:{}',e)
        return None

def create_message_with_attachment(sender,to,subject,body,file):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(body)
    message.attach(msg)

    (content_type, encoding) = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'

    (main_type, sub_type)=content_type.split('/',1)

    if main_type == 'text':
        with open(file,'rb') as f:
            msg = MIMEText(f.read().decode('utf-8'),_subtype=sub_type)

        
    elif main_type == 'image':
        with open(file,'rb') as f:
            msg = MIMEImage(f.read(),_subtype=sub_type)

    elif main_type == 'audio':
        with open(file,'rb') as f:
            msg = MIMEAudio(f.read(),_subtype=sub_type)  

    else:
        with open(file,'rb') as f:
            msg = MIMEBase(maintype,sub_type)
            msg.set_payload(f.read())

    filename = os.path.basename(file)
    msg.add_header('Content-Disposition','attachment',filename=filename)
    message.attach(msg)

    raw_msg = base64.urlsafe_b64encode(message.as_string().encode('utf-8'))

    return {'raw':raw_msg.decode('utf-8')}

    