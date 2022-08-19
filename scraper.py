from bs4 import BeautifulSoup
import requests
import json

base_url = 'https://www.mavcsoport.hu'
pagination = ''
jobs = []

pages_url = f'{base_url}/mav-csoport/allasajanlataink'
pages_response = requests.get(pages_url)
doc = BeautifulSoup(pages_response.text, 'html.parser')
number_of_pages = doc.find(class_='pager-last').a['href'].split('page=')

for page in range(0, number_of_pages[1] + 1):
    if page != 0:
        pagination = f'?page={page}'
    url = f'{base_url}/mav-csoport/allasajanlataink{pagination}'
    response = requests.get(url)
    doc = BeautifulSoup(response.text, 'html.parser')
    parents = doc.find_all(class_='views-row')
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

print(len(jobs))

json_object = json.dumps(jobs, indent=4)

with open('results.json', 'w') as outfile:
    outfile.write(json_object)
