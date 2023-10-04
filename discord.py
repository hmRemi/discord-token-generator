import random
import string
import requests
import time
from mailbox import Mailbox
import asyncio
import secrets
from console import *

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class DiscordGenerator:
    def __init__(self, mailbox: Mailbox, captcha_key: str):
        self.proxies = []
        self.mailbox: Mailbox = mailbox

        self.cap_monster_key = captcha_key

        self.fingerprint = None

        self.load_proxies('proxies.txt')

    def fetch_fingerprint(self, proxy):
        if not self.fingerprint:
            console.pending('Obtaining fingerprint')
            self.fingerprint = requests.get('https://discord.com/api/v9/experiments', proxies=proxy).json()[
                'fingerprint']

    def headers(self):
        return {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'en-GB',
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/channels/@me',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'cookie': '__dcfduid=23a63d20476c11ec9811c1e6024b99d9; __sdcfduid=23a63d21476c11ec9811c1e6024b99d9e7175a1ac31a8c5e4152455c5056eff033528243e185c5a85202515edb6d57b0; locale=en-GB',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.1.9 Chrome/83.0.4103.122 Electron/9.4.4 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-context-properties': 'eyJsb2NhdGlvbiI6IlVzZXIgUHJvZmlsZSJ9',
            'x-fingerprint': self.fingerprint,
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjAuMS45Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTc3NjMiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6OTM1NTQsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
            'te': 'trailers',
        }

    def create_account(self) -> str:
        proxy = self.random_proxy()

        self.fetch_fingerprint(proxy)

        # mail_account = self.mailbox.buy_email('HOTMAIL')
        # email = mail_account['Email']

        password = self.generate_password()
        email = self.generate_email()

        r = requests.post('https://discord.com/api/v9/auth/register', json={
            'fingerprint': self.fingerprint,
            'email': email,
            'username': "urdesires",
            'password': password,
            'invite': None,
            'consent': True,
            'date_of_birth': '2001-06-27',
            'gift_code_sku_id': None,
            'promotional_email_opt_in': False
        }, proxies=proxy, headers=self.headers())

        json = r.json()
        # Check if captcha is required
        if "captcha_sitekey" in r.text:
            # CREATE CAPTCHA TASK
            console.error('Captcha has been detected')
            createTask = requests.post("https://api.capmonster.cloud/createTask", json={
                "clientKey": self.cap_monster_key,
                "task": {
                    "type": "HCaptchaTask",
                    "websiteURL": "https://discord.com/channels/@me",
                    "websiteKey": r.json()['captcha_sitekey'],
                    "proxyType": "http",
                    "proxy_address": proxy['http'].split(':')[1],
                    "proxy_port": proxy['http'].split(':')[2],
                    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
                }
            }).json()["taskId"]

            getResults = {}
            getResults["status"] = "processing"

            console.pending(f'Attempting to solve captcha | {getResults["status"]} | {createTask}')

            while getResults["status"] == "processing":
                console.pending(f'Processing captcha | {getResults["status"]} | {createTask}')

                getResults = requests.post("https://api.capmonster.cloud/getTaskResult", json={
                    "clientKey": self.cap_monster_key,
                    "taskId": createTask
                }).json()

            solution = getResults["solution"]["gRecaptchaResponse"]
            console.solved(f'Successfully got solution | {getResults["status"]} | {createTask}')

            r = requests.post('https://discord.com/api/v9/auth/register', json={
                'fingerprint': self.fingerprint,
                'email': email,
                'username': "urdesires",
                'password': "UrDesires1234",
                'invite': "snipes",
                'consent': True,
                'date_of_birth': '2001-06-27',
                "captcha_key": solution,
                'gift_code_sku_id': None,
                'promotional_email_opt_in': False
            }, proxies=proxy, headers=self.headers())

            json = r.json()
            if 'token' in json:
                token = json['token']
                console.solved(f'Created token: {token}')

                with open("tokens.txt", 'a') as file:
                    file.write(f"{token}\n")
            else:
                if 'captcha_key' in json:
                    return console.error(f'Failed to create token: Invalid Captcha Response')
                if 'message' in json:
                    error = json['message']
                    error2 = json['retry_after']
                    return console.error(f'Failed to create token: {error} {error2}')
                else:
                    return console.error('Failed to create token.')
        else:
            if 'token' in json:
                token = json['token']
                console.solved(f'Created token: {token}')
            else:
                error = json['message']
                error2 = json['retry_after']
                return console.error(f'Failed to create token: {error} {error2}')

    def must_verify(self, token: str):
        # Check if the account needs to be verified
        r = requests.get('https://discord.com/api/v9/users/@me', headers={
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'en-GB',
            'content-type': 'application/json',
            'Authorization': token,
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/channels/@me',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'cookie': '__dcfduid=23a63d20476c11ec9811c1e6024b99d9; __sdcfduid=23a63d21476c11ec9811c1e6024b99d9e7175a1ac31a8c5e4152455c5056eff033528243e185c5a85202515edb6d57b0; locale=en-GB',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.1.9 Chrome/83.0.4103.122 Electron/9.4.4 Safari/537.36',
            'x-debug-options': 'bugReporterEnabled',
            'x-context-properties': 'eyJsb2NhdGlvbiI6IlVzZXIgUHJvZmlsZSJ9',
            'x-fingerprint': self.fingerprint,
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjAuMS45Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTc3NjMiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6OTM1NTQsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
            'te': 'trailers',
        }, proxies={
            'http': self.random_proxy(),
            'https': self.random_proxy()
        })

        return r.status_code == 403

    def generate_password(self):
        # Generate a Secure Password
        # https://stackoverflow.com/a/23728630
        chars = string.ascii_letters + string.digits + '!@#$%^&*()'
        size = random.randint(8, 16)

        return ''.join(random.choice(chars) for _ in range(size))

    def generate_email(self):
        return f"{secrets.token_hex(8)}@gmail.com"

    def random_proxy(self):
        # Return a random proxy
        proxy = random.choice(self.proxies).strip()
        return {'http': 'http://' + proxy, 'https': 'https://' + proxy}

    def load_proxies(self, filename: str):
        # Load proxies from a file
        with open(filename, 'r') as f:
            self.proxies = f.readlines()
