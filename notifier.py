import requests
from config import SLACK_URL

def send_slack(message):
    payload = {'text': message}
    requests.post(SLACK_URL, json=payload)