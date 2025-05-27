import requests
from config import SLACK_URL

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1376383588550967336/uNQXW_Mq38OA8xcq8Xz1zcpIuQ0Vpi5N2zFAsRsIJ4rHFLXrFtm60l-tg6iQ9iy2o5U3"

def send_discord_message(message):
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code != 204:
        print(f"메시지 전송 실패: {response.status_code}, {response.text}")