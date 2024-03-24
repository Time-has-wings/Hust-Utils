from LoginSession import LoginSession

# TODO
class hardWorking:
    def __init__(self, session: LoginSession) -> None:
        self.session = session
        resp = self.session.get("http://hard-working.hust.edu.cn/wechat/menuPage.do").text
    def getCourseList(self):
        data = {
            "pageNum": 1,
            "pageSize": 100,
        }
        resp = self.session.post(
            "http://hard-working.hust.edu.cn/wechat/publicBenLabor/student/queryOptionalCourseList.do",
            data=data,
        )
        # save response json to file
        with open("src/courseList.json", "w", encoding="utf8") as f:
            f.write(resp.text)
        return resp.json()["returnData"]["list"]

    def getCourseDetail(self, course_name: str,course_list: list = None):
        for course in course_list:
            if course["KCMC"] == course_name:
                course_id = course["KCID"]
                break
        data = {
            "pageNum": 1,
            "pageSize": 100,
            "kcid": course_id,
        }
        resp = self.session.post(
            "http://hard-working.hust.edu.cn/wechat/publicBenLabor/student/queryOptionalCLRMList.do",
            data=data,
        )
        # save response json to file
        with open("src/courseDetail.json", "w", encoding="utf8") as f:
            f.write(resp.text)
        return resp.json()["returnData"]["list"]

    def preSelect(self, course_id: str):
        data = {
            "xmid": course_id,
        }
        resp = self.session.post(
            "http://hard-working.hust.edu.cn/wechat/publicBenLabor/student/queryClassRoomUnitTeas.do",
            data=data,
        )
        # save response json to file
        with open("src/preSelect.json", "w", encoding="utf8") as f:
            f.write(resp.text)
        return resp.json()

    def selectCourse(self, course_id: str, class_id: str):
        data = {
            "xmid": 4309,
            "zdjsJson": '[{"xldyid": 142, "zdjsgh": "2023310158"}]',
            "jsfzxs": 1,
        }
        resp = self.session.post(
            "http://hard-working.hust.edu.cn/wechat/publicBenLabor/student/stuCourseSelection.do",
            data=data,
        )
        # save response json to file
        with open("src/select.json", "w", encoding="utf8") as f:
            f.write(resp.text)
        return resp.json()
    def run(self):
        List = self.getCourseList()
        self.getCourseDetail("PLC与HMI的交互控制",List)
        # self.preSelect("4307")
        # self.selectCourse("4307", "142")