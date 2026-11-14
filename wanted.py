
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import csv


p = sync_playwright().start()
browser = p.chromium.launch(headless=False)

page = browser.new_page()
keyword = "flutter"

page.goto(f"https://www.wanted.co.kr/search?query={keyword}&search_method=direct&tab=position")

for x in range(4):
    page.keyboard.down("End")
    time.sleep(5)

all_jobs = []

content = page.content()
soup = BeautifulSoup(content, "html.parser")
jobs = soup.find_all("div", class_="JobCard_container__zQcZs")
for job in jobs:
    try:
        title = job.find("strong", class_="JobCard_title___kfvj").text
    except AttributeError:
        title = ""
    try:
        company_name = job.find("span", class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__location__4_w0l").text
    except AttributeError:
        company_name = ""
    try:
        reword = job.find("span", class_="JobCard_reward__oCSIQ").text
    except AttributeError:
        reword = ""
    job_data = {
        "title" : title,
        "company_name" : company_name,
        "reword" : reword
    }
    all_jobs.append(job_data)

with open("data.csv", "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["title", "company_name", "reward"]) 

    for job in all_jobs:
        writer.writerow(job.values())

p.stop()