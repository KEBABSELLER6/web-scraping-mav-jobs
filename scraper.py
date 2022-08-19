from bs4 import BeautifulSoup
import requests
import json

base_url = 'https://www.mavcsoport.hu'
pagination = ''
jobs = []

for page in range(0, 49):
    if page != 0:
        pagination = f"?page={page}"
    url = f"{base_url}/mav-csoport/allasajanlataink{pagination}"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, 'html.parser')
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

with open("results.json", "w") as outfile:
    outfile.write(json_object)
