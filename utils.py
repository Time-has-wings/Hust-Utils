import io
from PIL import Image, ImageSequence
from pytesseract import image_to_string

import base64
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.PublicKey import RSA

import toml
import logging
import csv
import datetime
import json
import os

def launchLogging():
    logger = logging.getLogger("All for Badminton!")
    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')    
    console.setFormatter(formatter)
    logger.addHandler(console)
    return logger

logger = launchLogging()

def loadConfig():
    info = toml.load(open('info.toml', 'r', encoding='utf-8'))
    logger.info("配置文件加载成功")
    logger.info(f"""\n
                时间: {info['time']['date']} {info['time']['start_time']}点\n
                地点: {info['court']['name']} {info['court']['number']}号场地\n
                人员: {info['account']['name']} {info['partner']['name']}""")
    return info

def recordStore(info):
    account = {
        info['account']['name']: {
            "ID": info['account']["ID"],
            "password": info['account']['password']
        }
    }

    partner = {
        info['partner']['name']: {
            "ID": info['partner']['ID'],
            "password": info['partner']['password']
        }
    }

    if os.path.exists('record.json'):
        with open('record.json', 'r', encoding='utf-8') as jsonfile:
            existing_data = json.load(jsonfile)
    else:
        existing_data = {'account': {}, 'partner': {}}

    existing_data['account'].update(account)
    existing_data['partner'].update(partner)
    with open('record.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(existing_data, jsonfile, ensure_ascii=False, indent=4)  

    with open('record.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['execution_time', 'date', 'start_time', 'court_name', 'court_number', 'account_ID', 'account_name', 'partner_ID', 'partner_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow({
            'execution_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'date': info['time']['date'],
            'start_time': info['time']['start_time'],
            'court_name': info['court']['name'],
            'court_number': info['court']['number'],
            'account_ID': info['account']['ID'],
            'account_name': info['account']['name'],
            'partner_ID': info['partner']['ID'],
            'partner_name': info['partner']['name'],
        })
    
    logger.info("信息存储成功")

def deCaptcha(imageContent: bytes):
    # 打开图像文件
    img = Image.open(io.BytesIO(imageContent))

    # 检查图像是否是动态GIF
    if img.format == 'GIF':
        img_list = [frame.copy().convert('L') for frame in ImageSequence.Iterator(img)]
    else:
        img_list = [img.copy().convert('L')]
    width, height = img_list[0].size
    img_merge = Image.new(mode='L', size=(width + 20, height + 20), color=255)
    for pos in [(x, y) for x in range(width) for y in range(height)]:
        if sum([img.getpixel(pos) < 254 for img in img_list]) >= 3:
            img_merge.putpixel((pos[0] + 15, pos[1] + 10), 0)
    return image_to_string(img_merge, config='-c tessedit_char_whitelist=0123456789 --psm 11').strip()


class RsaEncoder:
    def __init__(self, user_id, password, public_key):
        self.public_key = RSA.importKey(f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----")
        self.password = password
        self.user_id = user_id

    def encode(self):
        cipher = PKCS1_cipher.new(self.public_key)
        encoded_user_id = base64.b64encode(cipher.encrypt(self.user_id.encode())).decode()
        encoded_password = base64.b64encode(cipher.encrypt(self.password.encode())).decode()
        return encoded_user_id, encoded_password
