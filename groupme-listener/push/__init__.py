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
    attachments = req_body.get('attachments')
    attachmentUrl = ''
    if attachments:
        attachmentUrl = str(attachments[0].get('url'))
    if attachmentUrl == 'None':
        attachmentUrl = ''

    if name == 'discord-pusher':
        return func.HttpResponse('was a bot message')

    data = { "content": f'{msg} {attachmentUrl}' }
    # data = { "content": msg, "embed": { "image": { "url": attachmentUrl } } }

    response = requests.post(WEBHOOK, json = data)
