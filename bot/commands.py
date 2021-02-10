from telegram import Update
from telegram.ext import CallbackContext
import quickstart

def sendmessage(update=Update,context=CallbackContext):

	service = quickstart.get_service()
    user_id = 'me'
    sender = 'molinahuel44@gmail.com'
    to = 'kindermolina98@gmail.com'
    subject = 'IMPORTANT do not delete'
    body = 'sasageyo'
    file = 'sample.txt'

    msg = quickstart.create_message_with_attachment(sender,to,subject,body,file)
    quickstart.send_message(service,user_id,msg)

	update.message.reply_text(f'Message Sent')	
