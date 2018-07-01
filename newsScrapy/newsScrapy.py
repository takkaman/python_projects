import urllib.request
from bs4 import BeautifulSoup
import time

url = "https://www.bloomberg.com/feeds/markets/sitemap_2018_6.xml"
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page,"html.parser")

sub_urls = soup.findAll('loc')
markets_news_dict = {}

for sub_url in sub_urls:
    print(sub_url.text)
    page = urllib.request.urlopen(sub_url.text)
    soup = BeautifulSoup(page,"html.parser")

    # titles = soup.findAll(attrs={"class":"lede-text-v2__hed"})
    title = soup.find(attrs={"class":"lede-text-v2__hed"})
    body_div = soup.find(attrs={"class":"body-copy-v2"})
    p_list = body_div.findAll('p')

    context = ""
    for p in p_list:
        context += p.text

    markets_news_dict[title.text] = context
    time.sleep(2)

df = pd.DataFrame.from_dict(markets_news_dict, orient='index')
df.index.name = 'Title'
df.columns = ['Context']
df.to_csv('news_market.csv')