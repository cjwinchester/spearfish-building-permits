from datetime import datetime
import time
import os

import requests
from bs4 import BeautifulSoup


def download_building_reports():
    filepaths = []
    base_url = 'https://www.cityofspearfish.com'
    url = f'{base_url}/Archive.aspx?AMID=37'

    req = requests.get(url)
    req.raise_for_status()

    soup = BeautifulSoup(req.text, 'html.parser')

    table = soup.find('div', {'id': 'modulecontent'})

    links = table.find_all('a')

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
                parsed_date = datetime.strptime(month_year,
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

            filepaths.append(filepath)

            time.sleep(1)
    return filepaths


if __name__ == '__main__':
    download_building_reports()
