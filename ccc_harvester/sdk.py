import json
import decimal
import logging
import os
import sys
from datetime import datetime

import requests

# PLATFORMS
TWITTER = 'twitter'
MASTDON = 'mastodon'
# CONNECTION URL
BACKEND_URL = 'http://172.26.135.47:5566'
# BACKEND_URL = 'http://server.muqoe.xyz:5566'
# BACKEND_URL = 'http://localhost:5000'

# Create Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# check if "/logs" exist
if not os.path.exists('logs/'):
    os.makedirs('logs/')

# check if "/logs/logs.log" exist
if os.path.exists('logs/logs.log'):
    # change the name of the "/logs/logs.log" log file to "logs-{time}.log"
    time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.rename('logs/logs.log', f'logs/logs-{time}.log')

# Set File Handler
file_handler = logging.FileHandler('logs/logs.log')
file_handler.setLevel(logging.INFO)

# Set Stream Handler
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)

# Set Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add Handlers to Logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.info('Harvester Started')



class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


class SDK:

    def __init__(self):
        pass

    @staticmethod
    def save_to_database(data=None, platform=None):
        buffer = {}
        if data is None:
            data = {}
        data_str = ""
        if type(data) is str:
            data_str = data
        else:
            try:
                data_str = json.dumps(data, ensure_ascii=False, cls=DecimalEncoder)
            except Exception as e:
                return None, "data is not json serializable"
        if platform is None:
            platform = TWITTER

        data_str = data_str.encode('utf-16', 'surrogatepass').decode('utf-16')

        url = BACKEND_URL + '/save_data'
        buffer["platform"] = platform
        buffer["data"] = data_str
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        try:
            response = requests.post(url, data=buffer, headers=headers)
            return response, None
        except requests.exceptions.RequestException as e:
            return None, str(e)
