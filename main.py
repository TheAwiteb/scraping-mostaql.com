import requests
import urllib.parse
from bs4 import BeautifulSoup as bs4
from time import sleep
import os

TOKEN = str() # bot token
chat_id = int() # your id

search_url = "https://mostaql.com/projects?keyword={}"
keywords = list() # your key words
send = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=markdown"

def get_text(text:str):
    return ''.join([t for t in text.strip('منذ') if not t.isnumeric()]).strip()

def main():
    if os.path.lexists('./urls.txt'):
        pass
    else:
        with open('./urls.txt', mode='w'): pass
    while True:
        for keyword in keywords:
            with open('urls.txt', 'r') as f:
                urls = f.read().split('\n')
            url = search_url.format(urllib.parse.quote(keyword))
            soup = bs4(requests.get(url).content, "lxml")
            projects = soup.find_all('tr', class_="project-row")
            for project in projects:
                title_and_url = project.find('span', class_="text-zeta12 text-meta")
                title = title_and_url.find('a').text.strip()
                project_url = title_and_url.find('a').get('href')
                time_ago = project.find('li', class_="text-muted").text.strip()
                date = project.find('li', class_="text-muted").find('time').get('title')
                detalils = project.find('a', class_="details-url").text.strip()
                if get_text(time_ago) in ['دقيقة', 'دقيقتين', 'ساعات', 'دقائق', 'ساعتين'] and project_url not in urls:
                    text = f"[رابط العرض]({project_url})\nالعنوان: {title}\nالوصف: {detalils}\n\n التاريخ: {date}\n{time_ago}"
                    requests.post(send.format(TOKEN,chat_id,text))
                    with open('urls.txt', 'a') as f:
                        f.write(project_url+'\n')
        sleep(10*60)
if __name__ == "__main__":
    main()