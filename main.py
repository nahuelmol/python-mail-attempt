from dotenv import load_dotenv
from pathlib import Path
from telegram.ext import Updater, CommandHandler
import bot.commands

load_dotenv(verbose=True)
env_path = Path('.env')
load_dotenv(dotenv_path=env_path)

token = os.getenv('TOKEN_BOT_TEL')

updater = Updater(token)
dispatcher = updater.dispatcher

send_mail = CommandHandler('sendmail',commands.sendmessage, pass_args=True,pass_chat_data=True)

dispatcher.add_handler(send_mail)

updater.start_polling()
updater.idle()