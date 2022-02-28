import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import os


COOKIE = json.load(open("cookies.json", "r", encoding="cp1252"))
ROOT = "https://gb.ru"
URL = "https://gb.ru/study_groups/34518"
NAME_CLASS = "homework-preview-item__user-name"
COURSE_CLASS = "homework-preview-item__task-number"

headers = {
    "cookie": os.environ.get("gb_parser_cookie")
}

r = requests.get(URL, headers=headers)
soup = BeautifulSoup(r.text, "lxml")
homeworks_block = soup.find("div", {"id": "mentor-unverified-homeworks"})
homeworks = homeworks_block.find_all("a", {"class": "homework-preview-item"})

homeworks_data = []

for item in homeworks:
    homework = {}
    name = item.find("div", {"class": NAME_CLASS}).text
    course = item.find("div", {"class": COURSE_CLASS}).text
    link = urljoin(ROOT, item.get("href"))
    homework["name"] = name
    homework["course"] = course
    homework["link"] = link
    homeworks_data.append(homework)
    print(homework)

with open("homeworks.json", "w") as f:
    json.dump(homeworks_data, f)

