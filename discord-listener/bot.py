# bot.py
from dis import disco
import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
import dotenv

import requests

bot = discord.ext.commands.Bot(command_prefix = '');

load_dotenv()
TOKEN = os.environ["TOKEN"]
GROUPME_ENDPOINT = os.environ["GROUPME_ENDPOINT"]
BOT_CHANNEL = os.environ["BOT_CHANNEL"]
GROUPME_BOT_ID = os.environ["GROUPME_BOT_ID"]

@bot.event
async def on_ready():
    print('connected')

@bot.event 
async def on_message(message):
    await bot.process_commands(message)
    channel = message.channel.name

    if message.author.display_name == 'groupme-listener':
        return;

    if channel == BOT_CHANNEL:
        content = message.content
        author = message.author.display_name
        msg = f'{author}: {content}'
        data = '{ "bot_id":"' + GROUPME_BOT_ID + '", "text": "' + msg + '" }'
        print(f'message sent by {author}: {msg}')
        requests.post(url = GROUPME_ENDPOINT, data = data)

bot.run(TOKEN)