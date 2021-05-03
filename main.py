import requests
import urllib.parse
from bs4 import BeautifulSoup as bs4
from time import sleep
import os

TOKEN = str() # bot token
chat_id = int() # your id

# 'business','development','engineering-architecture','design','marketing','writing-translation','support','training'
category_lst = [] # Put the fields that you want to search (you can place more than one field)
keywords = [] # your key words
category = '' if len(category_lst) == 0 else ','.join(category_lst)
search_url = "https://mostaql.com/projects?keyword={}&category="+category
send = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=markdown"

def get_text(text:str):
    return ''.join([t for t in text.strip('منذ') if not t.isnumeric()]).strip()

def get_numbers(text:str):
    return ''.join([num for num in text if num.isnumeric()])

def main():
    if os.path.lexists('./projects_id.txt'):
        pass
    else:
        with open('./projects_id.txt', mode='a+'): pass
    while True:
        for keyword in keywords:
            with open('projects_id.txt', 'r') as f:
                projects_id = f.read().split('\n')
            url = search_url.format(urllib.parse.quote(keyword))
            soup = bs4(requests.get(url).content, "lxml")
            projects = soup.find_all('tr', class_="project-row")
            for project in projects:
                title_and_url = project.find('span', class_="text-zeta12 text-meta")
                title = title_and_url.find('a').text.strip()
                project_url = title_and_url.find('a').get('href')
                project_id = project_url.replace('https://sa.mostaql.com/project/', '').split('-')[0]
                time_ago = project.find('li', class_="text-muted").text.strip()
                date = project.find('li', class_="text-muted").find('time').get('title')
                detalils = project.find('a', class_="details-url").text.strip()
                if get_text(time_ago) in ['دقيقة', 'دقيقتين', 'ساعات', 'دقائق', 'ساعتين', 'ساعتي'] and project_id not in projects_id:
                    text = f"[رابط العرض]({project_url})\nالعنوان: {title}\nالوصف: {detalils}\n\n التاريخ: {date}\n{time_ago}"
                    requests.post(send.format(TOKEN,chat_id,text))
                    with open('projects_id.txt', 'a') as f:
                        f.write('\n'+project_id)
        sleep(10*60)
if __name__ == "__main__":
    main()