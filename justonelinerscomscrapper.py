# utility thing, saving it here because, you know, reasons (might and might not work, and im not sure if this is even legal :skull:)

import requests, re, random, bs4

session = requests.session()
session.headers = {
    'sec-ch-ua': '"Chromium";v="112", "Not_A Brand";v="24", "Opera";v="98"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Python script please do not do the target ads please"',
    'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 OPR/98.0.0.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'Referer': 'https://yandex.ru/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'x-forwarded-proto': 'https',
    'x-https': 'on'
}

cool_things = []

for page_num in range(1, 27 + 1):
    search_page_url = "https://www.just-one-liners.com/category/classifieds/" + str(f"page/{page_num}/" if page_num > 1 else "")

    search_page_content = session.get(search_page_url).content

    soup = bs4.BeautifulSoup(search_page_content, features = "lxml")

    titles = soup.find_all("h2", "title")

    for title in titles:
        cool_things.append(title.a.string)

import os

with open("cool_things.py", "wb") as out:
    out.write("ads = [".encode())
    for cool in cool_things:
        #SICK #CODING
        #I #JUST #DONT #KNOW
        if not cool:
            continue
        coolish = cool.replace('\u00a0', " ").replace("\"", "\\\"")
        out.write(f"\n\t\"{coolish}\",".encode())
    out.seek(-1, os.SEEK_END)
    out.truncate()
    out.write("\n]".encode())