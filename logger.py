import logging

# ログファイル名
LOGFILE = "logfile.txt"

# logger設定
logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(LOGFILE)

# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
