#!/usr/bin/env python
import requests
import logging
import log
import time

USER_BEARER_TOKEN = 'OTYxZWNmMmMtMDZjNy00OWRiLTgwMzQtMWUwOGMzY2Y2MzQyNzAxOWJlYzUtYmY1'
LOGGER = log.setup_logging(logging.getLogger(__name__))


# Posts a message on Spark.
def spark_message_post(msg, room_id, url='https://webexapis.com/v1/messages',
                       file_path=None, file_name=None, file_type=None,
                       bearer_token=USER_BEARER_TOKEN, max_retries=3):
    headers = {
        'Authorization': 'Bearer {}'.format(bearer_token),
        'Content-Type': 'application/json'
    }
    data = {
        'roomId': room_id,
        'text': msg
    }
    if file_path and file_name and file_type:
        file_data = {'files': (file_name, open(file_path, 'rb'), file_type)}
        data.update(file_data)
    retry_list = [409, 500, 503]
    attempt = 0
    while attempt < max_retries:
        try:
            if attempt > 0:
                LOGGER.debug('Retrying post request')
            LOGGER.debug('Posting data: {0} on url: {1}, attempt: {2}'.format(data, url, attempt+1))
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                return True
            elif response.status_code in retry_list:
                LOGGER.error('Failed to post a message to spark room, received \n'
                             'Response code: {0} Response: {1}'.
                             format(response.status_code, response.text))
                attempt += 1
                time.sleep(5)
            else:
                LOGGER.error('Failed to post a message to spark room, received a non 200 '
                             'response code.\n Response code: {0} Response: {1}'.
                             format(response.status_code, response.text))
                return False
        except Exception:
            LOGGER.exception('Could not post message to Spark Room.')
            attempt += 1
            time.sleep(5)
    return False
