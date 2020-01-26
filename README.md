# Google Drive Telegram Bot

## Description
This project is a telegram bot hosted on the website https://pythonanywhere.com . It connects with your google drive using
Google Authentication which you can set up at https://developers.google.com .

## Usage
This telegram bot is created for a specific work procedure. Everyday, a few photos must be taken by a particular person
and stored in folders separated by days for future references. The telegram bot serves as an interface for the user to upload 
images to their google drive folders of the current day without having to navigate Google Drive, create new folders manually
and name the folders or pictures.

## Functionality
Everyday at 0000hrs, the script generate_new_file_id.py is scheduled to run automatically on pythonanywhere that creates a new folder on your Google Drive that is named by date (e.g. the folder will be named '200220' for 20th February 2020). Every photo that you send to the telegram bot will be uploaded to the folder dated the day at which you uploaded the photo on (which coincides with the latest folder created by this scheduled task). The image caption that you send to telegram with the image will be the name of the picture created in .jpg format (e.g. automated.jpg if your image caption is 'automated'). If no caption is given, the image name will be image.jpg by default. Having multiple images of the same name is perfectly fine in Google Drive.

## Libraries Used
This project is created using the following libraries:

- PyDrive
https://pythonhosted.org/PyDrive/

- PyTelegramBotAPI
https://github.com/eternnoir/pyTelegramBotAPI

- Flask for webhooks and URL for GET request
