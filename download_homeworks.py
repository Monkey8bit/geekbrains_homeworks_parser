# coding=utf-8

import requests
import json
from bs4 import BeautifulSoup
import os


COOKIE = json.load(open("cookies.json", "r", encoding="cp1252"))
HOMEWORK_ITEM = "user-solution-item"
ITEM_ARCHIVE = "user-solution-item__archive"
NO_COMMENT = "[нет комментария]".encode("cp1251")
COMMENT_AREA = "user-solution-item__user-comment"
homeworks = json.load(open("homeworks.json", "r"))

headers = {
    "cookie": os.environ.get("gb_parser_cookie")
}

r = requests.Session()
r.headers.update(headers)
i = 1

for homework in homeworks:
    print(f"Homework {i} of {len(homeworks)}")
    homework_page = r.get(homework["link"])
    homework_soup = BeautifulSoup(homework_page.text, "lxml")
    homework_item = homework_soup.find("div", {"class": HOMEWORK_ITEM})
    comment = homework_item.find("div", {"class": COMMENT_AREA})
    github_or_comment = comment.text if comment.text != NO_COMMENT else None
    path_to_file = f"./{homework['course']}/{homework['name']}/"

    if not os.path.exists(path_to_file):
        os.makedirs(path_to_file)

    try:
        file_link = homework_item.find("div", {"class": ITEM_ARCHIVE}).find("a").get("href")
        file_name = homework_item.find("div", {"class": ITEM_ARCHIVE}).find("a").text
        file = r.get(file_link, allow_redirects=True).content
        path_to_file = f"./{homework['course']}/{homework['name']}/"

        open(f"{path_to_file}{file_name}", "wb").write(file)

    except AttributeError:
        print(f"{homework['name']} github - {github_or_comment}")
        open(f"{path_to_file}github_or_comment.txt", "w").write(github_or_comment)

    i += 1
