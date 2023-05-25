import logging
import os
import sys
from datetime import datetime

from mastodon import Mastodon, StreamListener
import unicodedata
import re
import json
import emoji

from sdk import *

m = Mastodon(
    api_base_url=os.getenv('MASTODON_API_BASE_URL'),
    access_token=os.getenv('MASTODON_ACCESS_TOKEN')
)

# m = Mastodon(
#     api_base_url=f'https://aus.social/',
#     access_token='UfLp7ucfmaisAiU9nK7nBj3G7wiTDaSgPE9f-G8NsDE'
# )

def contains_emoji(text):
    '''
    This function checks if a string text contains emoji element
    :param text: A string of row context of Toot
    :return: A boolean indicating if any emoji is found
    '''
    return any(is_emoji(c) for c in text)


def is_emoji(char):
    '''
    This function checks for if a character is emoji
    :param char: the target character
    :return: A boolean indicating if this character is emoji
    '''
    return unicodedata.category(char).startswith('So')


class Listener(StreamListener):
    def on_update(self, status):
        obj = json.dumps(status, indent=0, sort_keys=True, default=str, ensure_ascii=False, separators=(',', ':'))
        obj = obj.replace("\n", "")
        obj =  re.sub("<[^>]*>", '', obj)
        if contains_emoji(obj):
            try:
                data = json.loads(obj)
                info = dict()
                text = data['content']
                if contains_emoji(text):
                    info['id'] = data['id']
                    info['author'] = data['account']['id']
                    info['account'] = data['account']
                    info['text'] = text
                    info['created_at'] = data['created_at']
                    info['emoji'] = emoji.distinct_emoji_list(text)
                    # print(json.dumps(info, indent=4))
                    # file.write(json.dumps(info, indent=4) + '\n')
                    response, error = SDK.save_to_database(data=info, platform=MASTDON)
                    if error is not None:
                        logging.error(error)
                    else:
                        logging.info(str(response.text).strip())
            except:
                pass

while True:
    try:
        print("Start streaming")
        print(os.getenv('MASTODON_ACCESS_TOKEN'))
        print(os.getenv('MASTODON_API_BASE_URL'))
        m.stream_public(Listener())
    except Exception as e:
        logging.error(e)
        continue