#-*- coding:UTF-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import time
import pandas as pd

url = "https://www.bloomberg.com/feeds/markets/sitemap_index.xml"
# url = "https://www.bloomberg.com/feeds/markets/sitemap_2018_6.xml"
# url = "https://www.bloomberg.com/news/articles/2018-06-24/china-s-central-bank-cuts-reserve-ratio-for-some-banks"
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page,"html.parser")

markets_news_dict = {}
i = 0
monthly_urls = soup.findAll('loc')
for monthly_url in monthly_urls:
    # print(monthly_url.text)
    if 'recent' in monthly_url.text or 'news' in monthly_url.text or 'video' in monthly_url.text:
        # print("skip")
        continue
    month_page = urllib.request.urlopen(monthly_url.text)
    soup = BeautifulSoup(month_page,"html.parser")
    sub_urls = soup.findAll('loc')
    
    for sub_url in sub_urls:
        print(sub_url.text)
        page = urllib.request.urlopen(sub_url.text)
        soup = BeautifulSoup(page,"html.parser")
        content = []
        # titles = soup.findAll(attrs={"class":"lede-text-v2__hed"})
        title = soup.find(attrs={"class":"lede-text-v2__hed"})
        # extract time
        page_time = soup.find(attrs={"class":"lede-text-v2__times"}).find('time')['datetime']
        # extract context
        body_div = soup.find(attrs={"class":"body-copy-v2"})
        p_list = body_div.findAll('p')
        context = ""
        for p in p_list:
            context += p.text.replace(u'’', u"'")
        # extract abstract
        abstract = [abs.text.replace(u'’', u"'") for abs in soup.findAll(attrs={"class":"abstract-v2__item-text"})]

        content = [sub_url.text, page_time, abstract, context]
        markets_news_dict[title.text] = content
        i += 1
        # if i >= 5: break
        time.sleep(.5)
    # if i >= 5: break

df = pd.DataFrame.from_dict(markets_news_dict, orient='index')
df.index.name = 'Title'
df.columns = ['url', 'time', 'abstract', 'Context']
df.to_csv('news_market.csv')
# df.to_csv('c:/workspace/learning/python_projects/newsScrapy/news_market.csv')