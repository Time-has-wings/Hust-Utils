import io
from PIL import Image, ImageSequence
from pytesseract import image_to_string

import base64
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.PublicKey import RSA

import toml
import logging

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
    logger.info(f"""\n
                时间: {info['time']['date']} {info['time']['start_time']}点\n
                地点: {info['court']['name']} {info['court']['number']}号场地\n
                人员: {info['account']['ID']} {info['partner']['ID']}""")
    return info

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
