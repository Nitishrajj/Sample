import requests
import logging
import log
from bs4 import BeautifulSoup


cc_reports_host = 'cc-reports.cisco.com'
recent_crashes = '/acr/signatures/recent'

LOGGER = log.setup_logging(logging.getLogger(__name__))


def get_todays_crashes():
    res = []
    url = 'https://' + cc_reports_host + recent_crashes
    response = requests.get(url)
    if response.status_code == 200:
        page_data = BeautifulSoup(response.content, "html.parser")

        for node in page_data.findAll('tr'):
            ab = node.findAll('a', text=True)
            try:
                if "Today" in str(ab[0]) and "build" in str(ab[3]):
                    res.append(ab[0].get('href'))
            except:
                pass
    else:
        LOGGER.error('could not get data from recent crashes page' + url)

    return res
