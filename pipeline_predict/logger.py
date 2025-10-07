import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class Logs:
    def __init__(self, name="pipeline", emoji=""):
        self.logger = logging.getLogger(name)
        self.emoji = emoji

    def info(self, msg):
        self.logger.info(f"{self.emoji} {msg}")

    def error(self, msg):
        self.logger.error(f"{self.emoji} {msg}")
        raise Exception(msg)
