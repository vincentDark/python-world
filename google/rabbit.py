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
    wp_pw = "m0H6 CVcJ 4GHN 557O 3OJ0 7rAt"
    wp_url = "https://nc66.net/xmlrpc.php"
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
    article = soup.find("div", class_="part_list_2")
    item_blocks = article("h3", limit=amount)

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
    article = content.find("div", itemprop="articleBody", class_="story")
    article_info = article.prettify()

    return article_info


def get_ettoday_news(category, amount):
    # 欲爬取網址 - ettoday
    url = 'https://www.ettoday.net/news/news-list'
    org_url = 'https://www.ettoday.net'
    # 要幾篇文章
    if category == 0:
        # 綜合
        url = url + '.htm'
    else:
        # 單獨分類  ||  今天日期
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
        try:
            article = get_ettoday_article(article_url['url'])
            article_info = {
                'title': article_url['title'],
                'category': article_url['category'],
                'tag': 'ettoday',
                'article': article,
            }
            wp_post(article_info)
            print(f'新增ID{category}第{num}篇文章完成')
        except:
            print(f'新增ID{category}第{num}篇文章失敗')
            pass

        print('=' * 30)
        time.sleep(random.uniform(1, 2))
        # 更新10篇中斷
        if num >= 10:
            break

    return num


category_name = {
    'sports': '體育'
}


def get_china_article_info(target_url):
    """爬取文章內文資訊"""

    r = requests.get(target_url, headers=HEADERS)
    if r.status_code != requests.codes.ok:
        print('網頁文章資訊載入失敗')
        return {}

    content = BeautifulSoup(r.text, "html.parser")
    # 內文
    article = content.find("article", class_="article-box")

    # 文章圖片兩個區塊
    article_content1 = article.find("div", class_="main-figure")
    article_content2 = article.select_one(".article-body").prettify()

    # 避免沒有圖片
    cont1 = ""
    if article_content1:
        cont1 = article_content1.prettify()

    article_content = cont1 + article_content2

    return article_content


def get_china_news(category):
    # 欲爬取網址 - ettoday
    url = 'https://www.chinatimes.com'
    query = f"/{category}/total?chdtv"
    target_url = url + query
    print(target_url)
    r = requests.get(target_url, headers=HEADERS)
    if r.status_code != requests.codes.ok:
        print('網頁文章資訊載入失敗')
        return {}
    soup = BeautifulSoup(r.text, features='html.parser')
    item_blocks = soup.find_all("div", class_="articlebox-compact")
    num = 0

    for item_block in item_blocks:
        num += 1
        item = item_block.find("h3")
        title = item.select_one("a").text
        link = url + item.select_one("a").get("href")
        print(f'中時新聞{category}開始第{num}篇文章載入')
        print(link)
        try:
            article = get_china_article_info(link)
            article_info = {
                'title': title,
                'category': category_name[category],
                'tag': category,
                'article': article,
            }
            wp_post(article_info)
            print(f'中時新聞{category}第{num}篇文章完成')
        except:
            print(f'中時新聞{category}第{num}篇文章失敗')
            pass
        print('=' * 30)
        time.sleep(random.uniform(1, 2))
        # 載入12篇就好
        if num >= 10:
            break
    return num


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
        channelId = 1013
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
    # # 中時新聞
    category = 'sports'
    pet_list = get_china_news(category)
    print(f"共抓到中時 {pet_list} 篇新聞")
    # # ettoday即時新聞  分類在最上面
    category = 5  # 分類  生活
    amount = 15  # 數量
    news_num = get_ettoday_news(category, amount)
    print(f"共抓到ettoday生活 {news_num} 篇新聞")
    category = 21  # 分類  健康
    amount = 15  # 數量
    news_num = get_ettoday_news(category, amount)
    print(f"共抓到ettoday健康 {news_num} 篇新聞")
    # # udn新聞
    temp = getudn_news_id(0)
    print(f"共抓到udn旅遊 {temp} 篇新聞")
