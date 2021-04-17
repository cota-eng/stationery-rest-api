import environ
env = environ.Env()
env.read_env('.env')
import threading
import requests
import json

class WebhookThread(threading.Thread):

    def __init__(self, data):
        self.data = data
        threading.Thread.__init__(self)

    def run(self):
        WEB_HOOK_URL = env.get_value("SLACK_WEBHOOK_CREATE_USER")
        print("-"*10)
        print(self.data)
        webhook_post = requests.post(WEB_HOOK_URL,data=self.data)


class Util:
    @staticmethod
    def send_webhook(data):
        WebhookThread(data).start()