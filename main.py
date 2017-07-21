#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pdfkit
import requests
from bs4 import BeautifulSoup

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>
"""

def parse_url_to_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find_all(class_="x-wiki-content")[0]

    # 加入标题，居中显示
    title = soup.find('h4').get_text()
    center_tag = soup.new_tag("center")
    title_tag = soup.new_tag('h1')
    title_tag.string = title
    center_tag.insert(0, title_tag)
    body.insert(0, center_tag)

    html = str(body)
    html = html_template.format(content=html)
    html = html.encode("utf-8")
    return html

def get_url_list():
    response = requests.get("https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000")
    soup = BeautifulSoup(response.content, "html.parser")
    menu_tag = soup.find_all(class_="uk-nav uk-nav-side")[1]
    # urls = []
    for li in menu_tag.find_all("li"):
        url = "https://www.liaoxuefeng.com" + li.a.get("href")
        # urls.append(url)
    # return urls
        yield url

def save_pdf(htmls):
    options = {
        'page-size': 'A5',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': 'UTF-8',
        'custom-header':[
            ('Accept-Encoding', 'gzip')
        ],
        'outline-depth': 10
    }
    pdfkit.from_file(htmls, "Python_Tutorial.pdf", options=options)

htmls = []

# Tips: 需要使用enumerate标注每个url对应的index，同时用join命名文件名，存为一个新的文件
for index, url in enumerate(get_url_list()):
    html = parse_url_to_html(url)
    f_name = ".".join([str(index), "html"])
    with open(f_name, 'wb') as f:
        f.write(html)
    htmls.append(f_name)

save_pdf(htmls)
