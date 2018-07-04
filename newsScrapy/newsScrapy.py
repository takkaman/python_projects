#-*- coding:UTF-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import time, random
import pandas as pd
import numpy as np
import requests
import traceback

url = "https://www.bloomberg.com/feeds/technology/sitemap_index.xml"
# url = "https://www.bloomberg.com/feeds/markets/sitemap_2018_6.xml"
# url = "https://www.bloomberg.com/news/articles/2018-06-24/china-s-central-bank-cuts-reserve-ratio-for-some-banks"

## randomly choose user agent
desktop_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

def random_headers():
    return {'User-Agent': random.choice(desktop_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

session = requests.session()
headers = random_headers()
page = session.get(url, headers=headers)
soup = BeautifulSoup(page.text, "html.parser")

# page = urllib.request.urlopen(url)
# soup = BeautifulSoup(page,"html.parser")

markets_news_dict = {}
fail = 0
prev_fail = False
i = 0
j = 0
monthly_urls = soup.findAll('loc')
for monthly_url in monthly_urls:
    print(monthly_url.text)
    j += 1
    if j <= 8: continue
    if 'sitemap_recent' in monthly_url.text or 'sitemap_news' in monthly_url.text or 'sitemap_video_recent' in monthly_url.text:
        # print("skip")
        continue
    # month_page = urllib.request.urlopen(monthly_url.text)
    session = requests.session()
    page = session.get(monthly_url.text, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")

    sub_urls = soup.findAll('loc')
    
    for sub_url in sub_urls:
        try:
            print(sub_url.text)
            session = requests.session()
            page = session.get(sub_url.text, headers=headers)
            soup = BeautifulSoup(page.text, "html.parser")
            # page = urllib.request.urlopen(sub_url.text)
            # soup = BeautifulSoup(page,"html.parser")
            content = []
            # titles = soup.findAll(attrs={"class":"lede-text-v2__hed"})
            title = soup.find(attrs={"class":"lede-text-v2__hed"})
            if title is None:
                print(sub_url.text+ " title returns none")
                title = soup.find(attrs={"class":"lede-text-only__hed"})
            print(title)
            # extract time

            page_time = soup.find(attrs={"class":"lede-text-v2__times"})
            if page_time is None:
                print(sub_url.text+ " page returns none")
                page_time = soup.find(attrs={"class":"lede-text-only__times"}) 
                page_time = page_time.find('time')['datetime']
            else:
                page_time = page_time.find('time')['datetime']
            print(page_time)
            # extract context
            topic = soup.find(attrs={"class": "eyebrow-v2"})
            if topic is None:
                topic = np.nan
            else:
                topic = topic.text.strip().replace('\n', '').replace('\r', '')

            body_div = soup.find(attrs={"class":"body-copy-v2"})
            if body_div is None:
                body_div = soup.find(attrs={"class":"body-copy"})
                
            p_list = body_div.findAll('p')
            context = ""
            for p in p_list:
                context += p.text.replace(u'’', u"'")
            # extract abstract
            abstract = [abs.text.replace(u'’', u"'") for abs in soup.findAll(attrs={"class":"abstract-v2__item-text"})]
            if len(abstract) == 0:
                abstract = [abs.text.replace(u'’', u"'") for abs in soup.findAll(attrs={"class":"abstract__item-text"})]
                if len(abstract) == 0:
                    abstract = "NA"
            content = [sub_url.text, page_time, topic, abstract, context]
            markets_news_dict[title.text] = content
            print(str(i)+" Done")
            fail = 0
            i += 1
            if i >= 10000: break
            time.sleep(random.random()*10)
        except:
            print(sub_url.text+" raised exception")
            traceback.print_exc()
            fail += 1
            print(str(fail)+ " failed")
            if fail > 50: break
            time.sleep(random.random()*10)
    if i >= 10000 or fail > 50: break

df = pd.DataFrame.from_dict(markets_news_dict, orient='index')
df.index.name = 'Title'
df.columns = ['url', 'time', 'topic', 'abstract', 'Context']
df.to_csv('news_technology.csv')
# df.to_csv('c:/workspace/learning/python_projects/newsScrapy/news_market.csv')