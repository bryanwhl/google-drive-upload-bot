from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import telebot
from telebot import types
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from flask import Flask, request
import os
import datetime

app = Flask(__name__)

creds_txt_file = '' #Insert your mycreds.txt file directory into the string

def Authenticate():
    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile(creds_txt_file) #Insert your mycreds.txt file directory into the string

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
    gauth.SaveCredentialsFile(creds_txt_file)

    drive = GoogleDrive(gauth)
    return drive

Authenticate()

bot_token = '' #Insert your bot token into the string
bot = telebot.TeleBot(token=bot_token, threaded = False)
bot.remove_webhook()
bot.set_webhook(url='' + bot_token) #Insert your webhook url into the link

get_request_link = '' #Insert a new URL for your routine get request into the string

@app.route('/' + bot_token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


def generated_id(folder_name):
    drive = authenticate()
    top_level_folder = drive.CreateFile({'title': folder_name, 'mimeType' : 'application/vnd.google-apps.folder'})
    top_level_folder.Upload()
    parent_id = top_level_folder['id']
    return parent_id


@app.route('/' + get_request_link, methods=['GET'])
def refreshStuff():
    dateToday = datetime.datetime.now()+datetime.timedelta(hours=8)
    folder_name = str(dateToday.date())

    new_file_id = generated_id(folder_name)
    f= open("file_id.txt","w+")
    f.write(new_file_id)
    f.close()
    return "Code Done", 200


@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        Authenticate()
    except Exception as e:
        bot.reply_to(message, str(e))


@bot.message_handler(content_types=['photo'])
def photo(message):
    bot.reply_to(message, 'Processing Image...')
    drive = Authenticate()
    try:
        
        #Download the photo sent into the server
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        
        #Variable file_name is name of the photo which is set as the caption of the telegram message of the photo sent. 
        #If no caption is given, the default name given is image.jpg
        if message.caption != None:
            file_name = message.caption + '.jpg'
        else:
            file_name = 'image.jpg'

        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        #Upload the image onto a particular image folder with the folder's ID stored in a txt file called file_id.txt
        f= open("file_id.txt","r")
        file_id = f.read()
        file5 = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": file_id}]})
        file5.SetContentFile(file_name)
        file5.Upload() # Upload the file.
        os.remove(file_name)
        bot.reply_to(message, 'Photo Uploaded.')
    except Exception as e:
        #Tell the user that there's an error
        bot.reply_to(message, str(e))
