from datetime import datetime
import time
import os

import requests
from bs4 import BeautifulSoup
from slack_sdk.webhook import WebhookClient


SLACK_HOOK_LOCAL_CITY = os.environ.get('SLACK_HOOK_LOCAL_CITY')
BASE_URL = 'https://www.cityofspearfish.com'

req = requests.get(
    f'{BASE_URL}/Archive.aspx?AMID=37',
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:134.0) Gecko/20100101 Firefox/134.0'
    }
)

req.raise_for_status()

time.sleep(1)

soup = BeautifulSoup(req.text, 'html.parser')
table = soup.find('div', {'id': 'modulecontent'})
links = table.find_all('a')


def check_for_new_reports():
    for link in links:
        if link.get('href') and '?ADID=' in link.get('href', '').upper():
            href = link.get('href')
            url = f'{BASE_URL}/{href}'

            month_year = link.text.lower().split('permits')[-1].split('report')[-1].strip()
            month_year = month_year.lstrip('-').split('(')[0].strip()

            # fix month whose label is missing a year
            if 'ADID=1500' in href:
                month, year = '07', '2023'
            else:
                parsed_date = datetime.strptime(
                    month_year,
                    '%B %Y'
                )
                month, year = str(parsed_date.month).zfill(2), parsed_date.year
            
            filepath = f'pdfs/{year}-{month}.pdf'

            if os.path.exists(filepath):
                continue

            blk = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*<{url}|New City of Spearfish building permits report for {month} {year}>*"
                    }
                }
            ]

            response = webhook.send(
                text=f'New City of Spearfish building permits report for {month} {year}: {url}',
                blocks=blk
            )

            time.sleep(1)
    return


def download_building_reports():
    new_reports = []

    for link in links:
        if link.get('href') and '?ADID=' in link.get('href', '').upper():
            href = link.get('href')
            url = f'{base_url}/{href}'

            month_year = link.text.lower().split('permits')[-1].split('report')[-1].strip()
            month_year = month_year.lstrip('-').split('(')[0].strip()

            # fix month whose label is missing a year
            if 'ADID=1500' in href:
                month, year = '07', '2023'
            else:
                parsed_date = datetime.strptime(
                    month_year,
                    '%B %Y'
                )
                month, year = str(parsed_date.month).zfill(2), parsed_date.year
            
            filepath = f'pdfs/{year}-{month}.pdf'

            if os.path.exists(filepath):
                continue

            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content():
                        f.write(chunk)
                print(f'Downloaded {filepath}')

            new_reports.append({
                'month': month,
                'year': year,
                'url': url
            })

            time.sleep(1)
    return filepaths


if __name__ == '__main__':
    check_for_new_reports()
