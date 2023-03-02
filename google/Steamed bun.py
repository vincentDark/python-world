import time
import random
import requests
import functions_framework
from datetime import datetime
from bs4 import BeautifulSoup
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}


def wp_post(article_info):
    # wordpress 網站登入資訊
    # 饅頭WP
    wp_id = "ad2022min"
    wp_pw = "uzNZ zgFk 0ycD XZ5t QxRO DNaI"
    wp_url = "https://nice77.shop/xmlrpc.php"
    # 送出WP  建立客戶端
    wp = Client(wp_url, wp_id, wp_pw)
    # 建立新文章
    post = WordPressPost()
    post.post_status = "publish"
    post.title = article_info['title']
    post.content = article_info['article']
    tag = article_info['tag']
    category = article_info['category']

    post.terms_names = {
        "post_tag": [tag],
        "category": [category]
    }
    # 發出去!
    wp.call(NewPost(post))
    return

# 即時新聞    一頁20篇
# channelId = 1
# cate_id = 0
# type_ = 'breaknews'

# 分類新聞    一頁6篇
# channelId = 2[兩岸][股市][產經][體育] 1013[旅遊]
# type_ = 'cate_latest_news'
# cate_id = 6640[兩岸] 6645[股市] 6644[產經] 7227[體育]  0[旅遊]


def getudn_news_id(inportid):
    # 取API列表幾頁  一頁6篇
    news_list = getudn_news_list(inportid)
    base_url = "https://udn.com"
    # 數量
    num = 0
    for news in news_list:
        num += 1
        print(f'ID{inportid}開始第{num}篇文章載入')
        news_url = base_url + news['titleLink']
        print(news_url)
        try:
            article_info = getudn_article_info(news_url)
            print(article_info['title'])
            print(article_info['category'])
            print(article_info['tag'])
            wp_post(article_info)
            print(f'新增ID{inportid}第{num}篇文章完成')
        except:
            print(f'新增ID{inportid}第{num}篇文章失敗')
            pass
        print('=' * 30)
        time.sleep(random.uniform(1, 2))
        # 更新10篇中斷
        if num >= 10:
            break

    return len(news_list)


def getudn_news_list(inportid):
    """爬取新聞列表"""
    # 取幾頁
    page_num = 3
    # 取API  轉json 格式處理
    base_url = "https://udn.com/api/more"

    news_list = []
    for page in range(page_num):
        # 即時新聞
        channelId = 2
        cate_id = inportid
        type_ = 'cate_latest_news'
        query = f"page={page+1}&channelId={channelId}&cate_id={cate_id}&type={type_}"
        news_list_url = base_url + '?' + query

        r = requests.get(news_list_url, headers=HEADERS)
        news_data = r.json()
        news_list.extend(news_data['lists'])
        time.sleep(random.uniform(1, 2))

    return news_list


def getudn_article_info(article_url):
    """爬取文章內文資訊"""

    r = requests.get(article_url, headers=HEADERS)
    if r.status_code != requests.codes.ok:
        print('網頁文章資訊載入失敗')
        return {}

    content = BeautifulSoup(r.text, "html.parser")
    article = content.find("section", class_="article-content__wrapper")
    # 標題
    article_title = article.select_one(".article-content__title").text
    # 分類跟TAG選項
    items = article.select(".breadcrumb-items")
    article_category = items[1].text
    article_tag = items[2].text
    # 文章圖片兩個區塊
    article_content1 = content.find("figure", class_="article-content__cover")
    article_content2 = article.select_one(
        ".article-content__editor").prettify()

    # 避免沒有圖片
    cont1 = ""
    if article_content1:
        cont1 = article_content1.prettify()

    article_content = cont1 + article_content2
    article_info = {
        'title': article_title,
        'category': article_category,
        'tag': article_tag,
        'article': article_content,
    }

    return article_info


if __name__ == "__main__":
    # # udn新聞
    tol_bilateral = getudn_news_id(6640)
    print(f"共抓到兩岸 {tol_bilateral} 篇新聞")
    tol_stock = getudn_news_id(6645)
    print(f"共抓到股票 {tol_stock} 篇新聞")
    tol_obstetrics = getudn_news_id(6644)
    print(f"共抓到產經 {tol_obstetrics} 篇新聞")
    tol_sport = getudn_news_id(7227)
    print(f"共抓到體育 {tol_sport} 篇新聞")
