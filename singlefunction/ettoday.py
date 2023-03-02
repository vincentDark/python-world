import time
import random
import requests
from datetime import datetime
from bs4 import BeautifulSoup


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}
# https://www.ettoday.net/news/news-list-2023-02-5-5.htm
# 1 政治 
# 17 財經
# 2 國際
# 6 社會
# 9 影劇
# 10 體育
# 20 3c
# 21 健康
# 30 時尚 
# 24 遊戲
# 5 生活
# https://www.ettoday.net/news/news-list.htm  總覽

def get_ettoday_url_list(forum_url, org_url, amount):
    """爬取文章列表"""
    
    response = requests.get(forum_url, headers=HEADERS)
    if response.status_code != requests.codes.ok:
        print('網頁文章列表載入失敗')
        print('---------------------')
        return []
    
    # 爬取每一篇文章網址
    article_info_list = []
    soup = BeautifulSoup(response.text, features='html.parser')
    article = soup.find("div", class_ = "part_list_2")
    item_blocks = article("h3",limit=amount)
    
    for item_block in item_blocks:
        article_url = org_url + item_block.select_one("a").get("href")
        article_category = item_block.select_one("em").text
        article_title = item_block.select_one("a").text
        article_info = {
            'title': article_title,
            'category': article_category,
            'url': article_url,
        }
        article_info_list.append(article_info)
    return article_info_list


def get_ettoday_article(article_url):
    """爬取文章內文資訊"""
    
    r = requests.get(article_url, headers=HEADERS)
    if r.status_code != requests.codes.ok:
        print('網頁文章資訊載入失敗')
        return {}

    content = BeautifulSoup(r.text, "html.parser")
    article = content.find("div" ,itemprop="articleBody",class_ = "story")
    article_info = article.prettify()

    return article_info

def get_ettoday_news(category,amount):
    # 欲爬取網址 - ettoday
    url = 'https://www.ettoday.net/news/news-list'
    org_url = 'https://www.ettoday.net'
    # 要幾篇文章
    if category == 0:
        # 綜合
        url = url + '.htm'
    else:
        #單獨分類  ||  今天日期
        currentDateAndTime = datetime.now()
        year = currentDateAndTime.year
        month = currentDateAndTime.month
        day = currentDateAndTime.day
        query = f"-{year}-{month}-{day}-{category}.htm"
        url = url + query
    
    print(url)
    article_url_list = get_ettoday_url_list(url, org_url, amount)
    print(f"共爬取 {len(article_url_list)} 篇文章")
    print('=' * 30)
    num = 0
    for article_url in article_url_list:
        num += 1
        print(f'ID{category}開始第{num}篇文章載入')
        print(article_url)
        
        article_info = get_ettoday_article(article_url['url'])
        time.sleep(random.uniform(1, 2))


    # # 測試第一篇
    article_info = get_ettoday_article(article_url_list[0]['url'])
    print(article_url_list[0]['title'])
    print(article_url_list[0]['category'])
    print(article_url_list[0]['url'])
    print(article_info)
    return num


if __name__ == "__main__":
    # # ettoday即時新聞  分類在最上面  0抓全部
    category = 5  #分類  
    amount = 15  #數量
    news_num = get_ettoday_news(category,amount)
    print(f"共抓到ettoday {news_num} 篇新聞")