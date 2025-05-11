from datetime import datetime
import time
import os
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from slack_sdk.webhook import WebhookClient


SLACK_HOOK_LOCAL_CITY = os.environ.get('SLACK_HOOK_LOCAL_CITY')
webhook = WebhookClient(SLACK_HOOK_LOCAL_CITY)
BASE_URL = 'https://www.cityofspearfish.com'

DIR_DATA = Path('data')
DIR_PDFS = Path('pdfs')

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:134.0) Gecko/20100101 Firefox/134.0'

MONTH_YEAR_FORMATS = [
    "%B %Y",
    "%B%Y"
]


def check_for_new_reports():

    new_reports = []

    req = requests.get(
        f'{BASE_URL}/Archive.aspx?AMID=37',
        headers={
            'User-Agent': USER_AGENT
        }
    )

    req.raise_for_status()

    time.sleep(1)

    soup = BeautifulSoup(req.text, 'html.parser')
    table = soup.find('div', {'id': 'modulecontent'})

    for link in table.find_all('a'):
        if link.get('href') and '?ADID=' in link.get('href', '').upper():
            href = link.get('href')
            url = urljoin(BASE_URL, href)

            month_year = link.text.lower().split('permits')[-1].split('report')[-1].strip()

            month_year = month_year.lstrip('-').split('(')[0].strip()

            # fix month whose label is missing a year
            if 'ADID=1500' in href:
                month, year = '07', '2023'
            else:
                for my in MONTH_YEAR_FORMATS:
                    try:
                        parsed_date = datetime.strptime(month_year, my)
                    except ValueError:
                        continue
                month, year = str(parsed_date.month).zfill(2), parsed_date.year
            
            filepath = DIR_PDFS / f'{year}-{month}.pdf'

            if filepath.exists():
                continue

            # download the PDF
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                time.sleep(1)

                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content():
                        f.write(chunk)
                print(f'Downloaded {filepath}')

            month_str = datetime(int(year), int(month), 1).strftime('%B %Y')

            new_reports.append({
                'month': month,
                'year': year,
                'url': url,
                'month_str': month_str
            })

    if not new_reports:
        return []

    new_reports.sort(key=lambda x: (x['year'], x['month']))

    report_label = 'report' if len(new_reports) == 1 else 'reports'

    slack_str = f"*New City of Spearfish building permit {report_label} ({len(new_reports)})*"

    for report in new_reports:
        slack_str += f'\n- <{report.get("url")}|{report.get("month_str")}>'

    blk = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": slack_str
            }
        }
    ]

    response = webhook.send(
        text=f'New City of Spearfish building permit {report_label} ({len(new_reports)}: {" | ".join([x.get("url") for x in new_reports])}',
        blocks=blk
    )

    time.sleep(1)
    
    return new_reports


if __name__ == '__main__':
    check_for_new_reports()
