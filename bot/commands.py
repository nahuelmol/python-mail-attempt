from telegram import Update
from telegram.ext import CallbackContext

from .quickstart import *

def sendmessage(update=Update,context=CallbackContext):

    mylist = []
    mylist = context.args
    mystring = ""
    destino = ""

    for i in mylist:
        if '@' in i:
            destino = i
            continue
        mystring = mystring + " "+ i

    if destino:

        service = get_service()
        user_id = 'me'
        sender = 'molinahuel44@gmail.com'
        to = destino  
        subject = 'THIS IS FROM BOT'
        body = mystring
        file = 'bot/sample.txt'
    
        msg = create_message_with_attachment(sender,to,subject,body,file)
        send_message(service,user_id,msg)
    
        update.message.reply_text(f'Message Sent')	
