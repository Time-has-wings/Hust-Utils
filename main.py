from utils import loadConfig, logger
from LoginSession import LoginSession
from Badminton import Badminton

if __name__ == "__main__":
    info = loadConfig()
    session = LoginSession(userId=info["account"]["ID"], 
                           password=info["account"]["password"])
    badminton = Badminton(session=session, 
                          date=info["time"]["date"], 
                          start_time=info["time"]["start_time"], 
                          court=info["court"], 
                          partner=info["partner"])
    logger.info("badminton created, will run to book the court")
    result = badminton.run()
    logger.info(result)
