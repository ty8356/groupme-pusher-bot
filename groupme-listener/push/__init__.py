import logging
import webbrowser
import azure.functions as func
import os
from dotenv import load_dotenv
import dotenv
import requests

load_dotenv()

WEBHOOK = str(os.environ["CUSTOMCONNSTR_WEBHOOK"])

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    name = req_body.get('name')
    message = req_body.get('text')
    msg = f'{name}: {message}'

    if name == 'discord-pusher':
        return func.HttpResponse('was a bot message')

    data = { "content": msg }

    response = requests.post(WEBHOOK, json = data)
