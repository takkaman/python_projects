# -*- coding: utf-8 -*-




import urllib.request
from bs4 import BeautifulSoup
import time, random
import pandas as pd
import requests
import traceback
from random import choice
import numpy as np
import re
from xml.sax.saxutils import quoteattr

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

def save_csv(news_dict, name, total_num):
    df = pd.DataFrame.from_dict(news_dict, orient='index')
    df.index.name = 'Title'
    df.columns = ['web_url', 'published_date', 'topic', 'abstract', 'context']
    output_name = name + "_" + str(total_num) + '.csv'
    df.to_csv(output_name)
    print("---------------------------------------------")
    print(output_name + ' is done')
    print("---------------------------------------------")

## url of a topic
url = "https://www.bloomberg.com/feeds/technology/sitemap_index.xml"

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
    
    news_dict = {}
    crawled = 0
    total_num = 0
    failed = 0
    total_failed = 0
    print("monthly url: " + monthly_url.text)

    j += 1
    if j <= 7:
        continue
    if 'sitemap_recent' in monthly_url.text or 'sitemap_news' in monthly_url.text or 'sitemap_video_recent' in monthly_url.text:
        # print("skip")
        continue

    session1 = requests.session()
    page1 = session1.get(monthly_url.text, headers=headers)
    soup = BeautifulSoup(page1.text, "html.parser")

    sub_urls = soup.findAll('loc')

    name = monthly_url.text.split('/')[5].split('.')[0]
    name = "news_tech_" + name

    ## total news in this month
    total = 0
    for sub_url in sub_urls:
        total += 1

    print("---------------------------------------------")
    print("monthly url: " + monthly_url.text)
    print("csv name: " + name)
    print("there are " + str(total) + " news of this month")
    print("---------------------------------------------")

    for sub_url in sub_urls:
        total_num += 1

        try:
            print("sub url: " + sub_url.text)
            session = requests.session()
            page = session.get(sub_url.text, headers=headers)
            soup = BeautifulSoup(page.text, "html.parser")

            content = []

            ## decompose
            for div in soup.find_all('div', attrs={'class': 'disclaimer'}):
                div.decompose()

            for p in soup.find_all('p', attrs={'class': 'news-rsf-contact-author'}):
                p.decompose()

            for p in soup.find_all('p', attrs={'class': 'news-rsf-contact-editor'}):
                p.decompose()

            ## Title
            title = soup.find(attrs={"class": "lede-text-v2__hed"})
            if title is None:
                title = soup.find(attrs={"class": "lede-text-only__hed"})
            if title is None:
                title = soup.find('h1', attrs={"class": re.compile(r'hed')})
            if title is None:
                title = np.nan
                print("title is None")
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
            page_time = soup.find('time', attrs={'itemprop': "datePublished"})
            if page_time is None:
                page_time = np.nan
                print("Published date is None")
            else:
                page_time = page_time.text
                page_time = page_time.strip().replace('\n', '').replace('\r', '').split('}')[1].strip()
                print("Public Date: " + page_time)

            ## abstract
            abs = ""
            abstract = [abs.text.replace(u'’', u"'") for abs in
                        soup.findAll(attrs={"class": "abstract-v2__item-text"})]
            if len(abstract) == 0:
                abstract = [abs.text.replace(u'’', u"'") for abs in
                            soup.findAll(attrs={"class": "abstract__item-text"})]
                if len(abstract) == 0:
                    abstract = soup.find('div', attrs={"class": "lede-text-only__dek"})
                    if abstract is None:
                        abs = np.nan
                        print("Abstract is None")
                    else:
                        abstract = abstract.find('span', attrs={"class": "lede-text-only__highlight"})
                        abs = quoteattr(abstract.text.strip().replace('\n', '').replace('\r', '')).replace('&amp;', '').replace('apos;', "'").replace(u'\xa0', ' ').replace("\'", "'")[1:-2]
                        print("Abstract: " + abs)
                else:
                    for i in range(0, len(abstract)):
                        abstract[i] = quoteattr(abstract[i].text.strip().replace('\n', '').replace('\r', '')).replace('&amp;', '').replace('apos;', "'").replace(u'\xa0', ' ').replace("\'", "'")[1:-2]
                        abs = abs + str(abstract[i])
                        abs = abs + ', '
                    abs = abs[:-2]
                    print("Abstract: " + abs)

            ## extract context
            body_div = soup.find(attrs={"class": "body-copy-v2"})
            if body_div is None:
                body_div = soup.find(attrs={"class": "body-copy"})
            p_list = body_div.findAll('p')
            context = ""
            for p in p_list:
                context += p.text.replace(u'’', u"'")
            context = quoteattr(context.strip().replace('\n', '').replace('\r', '')).replace('&amp;', '').replace(
                'apos;', "'").replace(u'\xa0', ' ').replace("\'", "'")[1:-2]
            context = re.sub(' +', ' ', context)
            print("Context: " + context)

            content = [sub_url.text, page_time, topic, abs, context]
            news_dict[title] = content
            crawled += 1
            failed = 0
            print("Crawled " + str(crawled))
            print("Falied: " + str(failed))
            print("Total failed: " + str(total_failed))
            print("Total: " + str(total_num))
            # time.sleep(random.random()*3)
            time.sleep(15)
        except:
            print(sub_url.text + " raised exception")
            traceback.print_exc()
            failed += 1
            total_failed += 1
            print("Crawled " + str(crawled))
            print("Falied: " + str(failed))
            print("Total failed: " + str(total_failed))
            print("Total: " + str(total_num))
            # time.sleep(random.random()*3)
            time.sleep(15)

        if failed == 10:
            save_csv(news_dict, name, total_num)
            failed_sign = 1
            break

    if failed_sign == 1:
        break

    save_csv(news_dict, name, total_num)
    # df = pd.DataFrame.from_dict(news_dict, orient='index')
    # df.index.name = 'Title'
    # df.columns = ['url', 'time', 'topic', 'abstract', 'Context']
    # df.to_csv(name)
    # print("---------------------------------------------")
    # print(name + ' is done')
    # print("---------------------------------------------")