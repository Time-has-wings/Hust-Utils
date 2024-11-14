import re
import time
from random import random

import fake_useragent
import httpx

from utils import deCaptcha, RsaEncoder, logger

user_agent = fake_useragent.UserAgent().chrome

class LoginSession(httpx.Client):
    def __init__(self, userId, password):
        super().__init__()
        self.url = "https://one.hust.edu.cn/dcp/"
        self.password = password
        self.userId = userId
        self.headers.update({"User-Agent": user_agent})
        self.follow_redirects = True
        self.login()

    def get_code(self):
        url = "https://pass.hust.edu.cn/cas/code?" + str(random())
        captchaContent = self.get(url)
        return deCaptcha(captchaContent.content)

    def get_rsa(self):
        rsa = self.post("https://pass.hust.edu.cn/cas/rsa").json()
        return RsaEncoder(self.userId, self.password, rsa["publicKey"]).encode()

    def get_lt(self):
        res = self.get(self.url)
        return re.search('<input type="hidden" id="lt" name="lt" value="(.*)" />', res.text).group(1)

    def login(self):
        cnt = 0
        try:
            lt = self.get_lt()
            code = self.get_code()
            rsa_userId, rsa_password = self.get_rsa()
            post_params = {
                "code": code,
                "rsa": "",
                "ul": rsa_userId,
                "pl": rsa_password,
                "lt": lt,
                "execution": "e1s1",
                "_eventId": "submit",
            }
            self.post(
                "https://pass.hust.edu.cn/cas/login?service=http://one.hust.edu.cn/dcp/index.jsp",
                data=post_params,
            )
            logger.info("Login Success!")
        except Exception as e:
            print(e)
            time.sleep(5)
            cnt += 1
            print("Login failed, retrying...", cnt)
            self.login()
