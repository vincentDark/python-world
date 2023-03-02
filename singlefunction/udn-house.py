import time
import random
import requests
from bs4 import BeautifulSoup

# 抓內文有問題
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}

def get_news_list():
    """爬取新聞列表"""
    # und-house不吃頁數
    base_url = "https://house.udn.com/rank/ajax_newest/1009/"

    r = requests.get(base_url, headers=HEADERS)
    news_data = r.json()
    time.sleep(random.uniform(1, 2))
    return news_data['articles']


def get_article_info(article_url):
    """爬取文章內文資訊"""
    
    r = requests.get(article_url, headers=HEADERS)
    if r.status_code != requests.codes.ok:
        print('網頁文章資訊載入失敗')
        return {}

    content = BeautifulSoup(r.text, "html.parser")
    # 內文
    article = content.find("div" ,id = "story_body_content").prettify()
    
    # 分類跟TAG選項
    nav = content.find("div" ,id = "nav")
    article_tag = nav.select_one("b").text

    
    article_info = {
            'tag': article_tag,
            'article': article,
    }

    return article_info


if __name__ == "__main__":
    # 取json頁面
    news_list = get_news_list()
    
    for news in news_list:
        article_org = news_list[news]
        art_title = article_org['art_title']
        link = article_org['link']
        
        article_info = get_article_info(link)
        
        # 原有連結資訊
        print(art_title)
        print(link)
        print(article_org['cate_name'])
        # infotag
        print(article_info['tag'])
        # print(article_info['article'])
        print('=' * 30)

        time.sleep(random.uniform(1, 2))
        if int(news) >= 3:
            break
        
    
    print(f"共抓到 {len(news_list)} 篇新聞")
