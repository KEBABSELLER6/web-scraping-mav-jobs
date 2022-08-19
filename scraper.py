from bs4 import BeautifulSoup
import requests

url = 'https://www.mavcsoport.hu/mav-csoport/allasajanlataink'

result = requests.get(url)
doc = BeautifulSoup(result.text, 'html.parser')

parents = doc.find_all(class_='views-row')
jobs = []
for parent in parents:
    company = parent.find(class_='field-job-company').string.strip()
    expiration_date = parent.find(class_='field-job-expiration-date').string.strip()
    title = parent.h3.string
    link = parent.h3.a['href']
    speciality = parent.find(class_='field-job-specialty').string.strip()
    schedule = parent.find(class_='field-job-schedule').string.strip()
    job = {'title': title, 'link': link, 'company': company, 'expiration-date': expiration_date,
           'specialty': speciality, 'schedule': schedule}
    jobs.append(job)

for j in jobs:
    print(j)
