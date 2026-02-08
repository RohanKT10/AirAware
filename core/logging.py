from loguru import logger
import sys

#For console logging
logger.remove()
logger.add(sys.stdout,format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",level="INFO")