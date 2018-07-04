# -*- coding:UTF-8 -*-




import urllib.request
from bs4 import BeautifulSoup
import time, random
import pandas as pd
import requests
import traceback
from random import choice
import numpy as np

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
    return {'User-Agent': choice(desktop_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

## url of a topic
url = "https://www.bloomberg.com/feeds/markets/sitemap_index.xml"

## parse the url
session = requests.session()
headers = random_headers()
# headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
page = session.get(url, headers=headers)
soup_full = BeautifulSoup(page.text, "html.parser")

## url of every month
j = 0
## inspect wrong parse
failed_sign = 0

monthly_urls = soup_full.findAll('loc')
for monthly_url in monthly_urls:
    if failed_sign == 1:
        break
    news_dict = {}
    crawled = 0
    total_num = 0
    failed = 0
    ceil = 200
    print("monthly url: " + monthly_url.text)
    j += 1
    if j <= 4: continue
    if 'sitemap_recent' in monthly_url.text or 'sitemap_news' in monthly_url.text or 'sitemap_video_recent' in monthly_url.text:
        # print("skip")
        continue

    session1 = requests.session()
    page1 = session1.get(monthly_url.text, headers=headers)
    soup = BeautifulSoup(page1.text, "html.parser")

    sub_urls = soup.findAll('loc')
    print("sub urls: ")
    print(sub_urls)
    name = monthly_url.text.split('/')[5].split('.')[0]
    name = "news_technology_" + name

    ## total news in this month
    total = 0
    for sub_url in sub_urls:
        total += 1

    print("---------------------------------------------")
    print("monthly url: " + monthly_url.text)
    print("csv name: " + name)
    print("there are " + str(total) + " news of this month")
    print("---------------------------------------------")

    ## from this news, start crawl
    index = 0
    for sub_url in sub_urls:
        total_num += 1

        if total_num > index:

            try:
                print("sub url: " + sub_url.text)
                session = requests.session()
                page = session.get(sub_url.text, headers=headers)
                soup = BeautifulSoup(page.text, "html.parser")

                content = []

                ## Title
                title = soup.find(attrs={"class": "lede-text-v2__hed"})
                if title is None:
                    title = soup.find(attrs={"class": "lede-text-only__hed"})
                    if title is None:
                        title = np.nan
                    else:
                        title = title.text.encode("utf-8").strip().replace('\n', '').replace('\r', '')

                else:
                    title = title.text.strip()
                print("title: " + title)

                ## topic
                topic = soup.find(attrs={"class": "eyebrow-v2"})
                if topic is None:
                    topic = np.nan
                else:
                    topic = topic.text.strip().replace('\n', '').replace('\r', '')

                ## public time
                page_time = soup.find(attrs={"class": "lede-text-v2__times"})
                if page_time is None:
                    page_time = soup.find(attrs={"class": "lede-text-only__times"})
                    if page_time is None:
                        page_time = np.nan
                    else:
                        page_time = page_time.find(attrs={'itemprop': "datePublished"}).text
                else:
                    page_time = page_time.find(attrs={'itemprop': "datePublished"}).text
                page_time = page_time.strip().replace('\n', '').replace('\r', '').split('}')[1].strip()
                print("Public Date: " + page_time)

                ## abstract
                abstract = [abs.text.replace(u'’', u"'") for abs in
                            soup.findAll(attrs={"class": "abstract-v2__item-text"})]
                if len(abstract) == 0:
                    abstract = [abs.text.replace(u'’', u"'") for abs in
                                soup.findAll(attrs={"class": "abstract__item-text"})]
                    if len(abstract) == 0:
                        abstract = np.nan
                for i in range (0, len(abstract)):
                    abstract[i] = abstract[i].strip().replace('\n', '').replace('\r', '')
                    print("Abstract: " + abstract[i])

                ## extract context
                body_div = soup.find(attrs={"class": "body-copy-v2"})
                if body_div is None:
                    body_div = soup.find(attrs={"class": "body-copy"})
                p_list = body_div.findAll('p')
                context = ""
                for p in p_list:
                    context += p.text.replace(u'’', u"'")
                context = context.strip().replace('\n', '').replace('\r', '')
                print("Context: " + context)

                content = [sub_url.text, page_time, topic, abstract, context]
                news_dict[title] = content
                crawled += 1
                print("Crawled " + str(crawled))
                print("Falied: " + str(failed))
                print("Total: " + str(total_num))
                # time.sleep(random.random()*3)
                time.sleep(10)
            except:
                print(sub_url.text + " raised exception")
                traceback.print_exc()
                failed += 1
                print("Crawled " + str(crawled))
                print("Falied: " + str(failed))
                print("Total: " + str(total_num))
                # time.sleep(random.random()*3)
                time.sleep(10)

            if crawled == ceil or crawled == total:
                df = pd.DataFrame.from_dict(news_dict, orient='index')
                df.index.name = 'Title'
                df.columns = ['web_url', 'published_date', 'topic', 'abstract', 'context']
                output_name = name + "_" + str(crawled) + '.csv'
                df.to_csv(output_name)
                print("---------------------------------------------")
                print(output_name + ' is done')
                print("---------------------------------------------")
                ceil = ceil + 200
                news_dict = {}

            if failed == 10:
                df = pd.DataFrame.from_dict(news_dict, orient='index')
                df.index.name = 'Title'
                df.columns = ['web_url', 'published_date', 'topic', 'abstract', 'context']
                output_name = name + "_" + str(crawled) + '.csv'
                df.to_csv(output_name)
                print("---------------------------------------------")
                print(output_name + ' is done')
                print("---------------------------------------------")
                failed_sign = 1
                break

    if failed_sign == 1:
        break

    # df = pd.DataFrame.from_dict(news_dict, orient='index')
    # df.index.name = 'Title'
    # df.columns = ['url', 'time', 'topic', 'abstract', 'Context']
    # df.to_csv(name)
    # print("---------------------------------------------")
    # print(name + ' is done')
    # print("---------------------------------------------")