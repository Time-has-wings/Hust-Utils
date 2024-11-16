from utils import loadConfig, logger, recordStore
from LoginSession import LoginSession
from Badminton import Badminton

if __name__ == "__main__":
    info = loadConfig()
    recordStore(info)
    session = LoginSession(userId=info["account"]["ID"], 
                           password=info["account"]["password"])
    badminton = Badminton(session=session, 
                          date=info["time"]["date"], 
                          start_time=info["time"]["start_time"], 
                          court=info["court"], 
                          partner=info["partner"])
    ecard = badminton.ecard()
    if ecard == False:
        logger.info("您的电子账户余额充足，即将进行场所锁定")
        result = badminton.run()
        logger.info(result)
    else:
        logger.info("您的电子账户余额不足，程序即将退出")
        exit(0)
