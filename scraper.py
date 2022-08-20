import pandas as pd
from bs4 import BeautifulSoup
import requests

base_url = 'https://www.mavcsoport.hu'
pagination = ''
jobs = []

pages_url = f'{base_url}/mav-csoport/allasajanlataink'
pages_response = requests.get(pages_url)
pages_doc = BeautifulSoup(pages_response.text, 'html.parser')
last_page = pages_doc.find(class_='pager-last').a['href'].split('page=')[1]
number_of_pages = int(last_page) + 1

for page in range(0, number_of_pages):
    if page != 0:
        pagination = f'?page={page}'
    url = f'{base_url}/mav-csoport/allasajanlataink{pagination}'
    print(f'Requesting url: {url}')
    response = requests.get(url)
    doc = BeautifulSoup(response.text, 'html.parser')
    parents = doc.find_all(class_='views-row')
    print(f'Number of jobs: {len(parents)}')
    for parent in parents:
        company = parent.find(class_='field-job-company').string.strip()
        expiration_date = parent.find(class_='field-job-expiration-date').string.strip()
        title = parent.h3.string
        link = base_url + parent.h3.a['href']
        speciality = parent.find(class_='field-job-specialty').string.strip()
        schedule = parent.find(class_='field-job-schedule').string.strip()
        job = {'title': title, 'link': link, 'company': company, 'expiration-date': expiration_date,
               'specialty': speciality, 'schedule': schedule}
        jobs.append(job)

df = pd.json_normalize(jobs)

df.to_csv('results.csv')
