from __future__ import print_function
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import telebot
from telebot import types
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from flask import Flask, request

app = Flask(__name__)


gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)

bot_token = '921319853:AAGRhh_okupip4_qX2kC8zsu2PVfwN-VM9Y'
bot = telebot.TeleBot(token=bot_token, threaded=False)
bot.remove_webhook()
bot.set_webhook(url='https://dubproject.pythonanywhere.com/' + bot_token)

@app.route('/' + bot_token, methods=['GET'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200
    

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome!')
    

@bot.message_handler(content_types=['photo'])
def photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    if message.caption != None:
        file_name = message.caption + '.jpg'
    else:
        file_name = 'image.jpg'
    
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
        
    file5 = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": '14_5u6-mv3LywmR7VWNmz6dGZgNNojDut'}]})
    # Read file and set it as a content of this instance.
    file5.SetContentFile(file_name)
    file5.Upload() # Upload the file.
    os.remove(file_name)
    bot.reply_to(message, 'Photo Uploaded.')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
