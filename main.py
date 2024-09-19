import configparser
import pytesseract

from LoginSession import LoginSession
from operate import Operator

config = configparser.ConfigParser()
config.read("account.ini")
userId = config["account"]["userId"]
password = config["account"]["password"]
if __name__ == "__main__":
    try:
        pytesseract.get_tesseract_version()
        session = LoginSession(userId=userId, password=password)
        operation = Operator(session, userId)
        print(operation.professional_credit().course_details())
    except pytesseract.TesseractNotFoundError:
        print("your device haven't installed tesseract yet")
