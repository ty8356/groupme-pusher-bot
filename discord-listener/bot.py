# bot.py
from dis import disco
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import dotenv
from PIL import Image
import requests
from io import BytesIO
import shutil
import urllib.request
import json

bot = discord.ext.commands.Bot(command_prefix = '');

load_dotenv()
TOKEN = os.environ["TOKEN"]
GROUPME_ENDPOINT = os.environ["GROUPME_ENDPOINT"]
BOT_CHANNEL = os.environ["BOT_CHANNEL"]
GROUPME_BOT_ID = os.environ["GROUPME_BOT_ID"]
GROUPME_ACCESS_TOKEN = os.environ["GROUPME_ACCESS_TOKEN"]
GROUPME_IMAGE_URL = os.environ["GROUPME_IMAGE_URL"]
GROUPME_LISTENER_NAME = os.environ["GROUPME_LISTENER_NAME"]

@bot.event
async def on_ready():
    print('connected')

@bot.event 
async def on_message(message):
    await bot.process_commands(message)
    channel = message.channel.name

    if message.author.display_name == GROUPME_LISTENER_NAME:
        return;

    if message.attachments:
        print(f'there are attachments: {message.attachments[0].url}, {message.attachments[0].filename}, {message.attachments[0].content_type}')

    if channel == BOT_CHANNEL:
        pictureUrl = ''
        if (message.attachments):
            attachmenturl = str(message.attachments[0].url)
            contentType = str(message.attachments[0].content_type)
            fileName = str(message.attachments[0].filename)
            outputDir = f'./attachments/{fileName}'

            img_data = requests.get(attachmenturl).content
            with open(outputDir, 'wb') as handler:
                handler.write(img_data)

            img = open(outputDir, 'rb').read()
            gmImageRes = requests.post(url = GROUPME_IMAGE_URL, data = img, headers = { "X-Access-Token": GROUPME_ACCESS_TOKEN, "Content-Type": contentType })
            jsonResponse = gmImageRes.json()
            pictureUrl = jsonResponse["payload"]["picture_url"];

        content = message.content
        author = message.author.display_name
        msg = f'{author}: {content}'
        data = str('{ "bot_id": "' + GROUPME_BOT_ID + '", "text": "' + msg + '", "picture_url": "' + pictureUrl + '" }').encode('utf-8')
        headers = { "Content-Type": "text/plain; charset=utf-8" }
        print(f'message sent by {author}: {msg}')
        requests.post(url = GROUPME_ENDPOINT, data = data, headers = headers)

bot.run(TOKEN)