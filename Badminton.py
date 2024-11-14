import datetime
import json
import re
import time
from bs4 import BeautifulSoup
from LoginSession import LoginSession
from utils import logger

class Badminton:
    def __init__(self, session:LoginSession, date:str, start_time:str, court:dict, partner:dict):
        self.session = session
        self.date = date
        self.start_time = datetime.datetime.strptime(start_time, "%H").strftime("%H:%M:%S")
        self.end_time = (datetime.datetime.strptime(self.start_time, "%H:%M:%S") + datetime.timedelta(hours=2)).strftime("%H:%M:%S")
        self.partner = partner
        self.cg_csrf_token = None
        with open("court.json") as f:
            info = json.load(f)
            self.court_cdbh = info[court["name"]]["cdbh"]
            self.court_number = info[court["name"]]["number"][court["number"]]

    def ecard(self):
        url = "http://ecard.m.hust.edu.cn/wechat-web/service/new_profile.html"
        res = self.session.get(url)
        soup = BeautifulSoup(res.text, features="html.parser")
        bills = float(soup.section.find_all("dl")[9].dd.div.span.string.strip("元"))
        return bills < 40 if self.start_time >= "18:00:00" else bills < 20
    
    def run(self) -> str:
        # 检查电子账户余额
        if self.ecard():
            return "电子账户余额不足"
        
        # 配置Referer && 获取csrf_token(看不懂的东西)
        self.session.headers["Referer"] = str(self.session.get("http://pecg.hust.edu.cn/cggl/index1").url)
        text = self.session.get("http://pecg.hust.edu.cn/cggl/index1").text
        self.cg_csrf_token = re.search('name="cg_csrf_token" value="(.*)" />', text).group(1)

        # 填写预约信息
        params = [
            ("starttime", self.start_time),  # 开始时间
            ("endtime", self.end_time),  # 结束时间
            ("partnerCardType", self.partner['card_type']),  # 第一个类型:学生
            ("partnerName", self.partner["name"]),  # 同伴姓名
            ("partnerSchoolNo", self.partner["ID"]),  # 同伴学号
            ("partnerPwd", self.partner["password"]),  # 同伴密码
            ("choosetime", self.court_number),  # 此处设置场地号
            ("changdibh", self.court_cdbh),  # 此处设置场地 光谷体育馆,西边体育馆,游泳馆
            ("date", self.date),  # 预约日期
            ("cg_csrf_token", self.cg_csrf_token),
        ]

        # 等待预约时间为前两天的8点
        wait = str(datetime.datetime.strptime(self.date + " 08", "%Y-%m-%d %H") - datetime.timedelta(days=2))
        wait = time.mktime(time.strptime(wait, "%Y-%m-%d %H:%M:%S"))
        previous_minutes_left = None
        while time.time() - wait < 0:
            current_time = time.time()
            time_left = wait - current_time
            minutes_left = int(time_left // 60)
            
            if minutes_left != previous_minutes_left:
                hours_left = int(time_left // 3600)
                minutes_left = int((time_left % 3600) // 60)
                seconds_left = int(time_left % 60)
                
                if time_left > 5 * 60:
                    if previous_minutes_left is None or previous_minutes_left - minutes_left >= 10:
                        logger.info(f"还需等待: {hours_left}h {minutes_left}min {seconds_left}s")
                        previous_minutes_left = minutes_left
                else:
                    logger.info(f"还需等待: {hours_left}h {minutes_left}min {seconds_left}s")
                    previous_minutes_left = minutes_left
            
            time.sleep(1)

        # 预约
        logger.info("开始预约")
        text = self.session.post("http://pecg.hust.edu.cn/cggl/front/step2", params=params).text
        try:
            data = re.search('name="data" value="(.*)" type', text).group(1)
            Id = re.search('name="id" value="(.*)" type', text).group(1)
            params = [
                ("data", data),
                ("id", Id),
                ("cg_csrf_token", self.cg_csrf_token),
                ("select_pay_type", -1),
            ]
            text = self.session.post("http://pecg.hust.edu.cn/cggl/front/step3", params=params).text
        except AttributeError:
            return re.search(r"alert\(HTMLDecode\('(.*)'\), '提示信息'\);", text).group(1)
        return re.search(r"alert\(HTMLDecode\('(.*)'\), '提示信息'\);", text).group(1)