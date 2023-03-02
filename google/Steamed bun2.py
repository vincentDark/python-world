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
    wp_pw = "Y4Vm FWYh 9XKX Qmpi 5vws nrop"
    wp_url = "https://nbnb77.net/xmlrpc.php"
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
    page_num = 2
    # 取API  轉json 格式處理
    base_url = "https://udn.com/api/more"

    news_list = []
    for page in range(page_num):
        # 旅遊
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


def get_stars_article_info(target_url):
    """爬取文章內文資訊"""

    r = requests.get(target_url, headers=HEADERS)
    if r.status_code != requests.codes.ok:
        print('網頁文章資訊載入失敗')
        return {}

    content = BeautifulSoup(r.text, "html.parser")
    # 內文
    article_content1 = content.find("div", class_="article-content__focus")
    article_content2 = content.find(
        "section", class_="article-content__editor").prettify()
    # 避免沒有圖片
    cont1 = ""
    if article_content1:
        cont1 = article_content1.prettify()

    article_content = cont1 + article_content2
    return article_content


def get_udn_stars(start_info):
    # 取json頁面
    """爬取stars即時新聞列表"""
    page_num = 2
    api_url = "https://stars.udn.com/api/more"
    start_list = []

    for page in range(page_num):
        # 最新文章
        channel_id = start_info['channel_id']
        cate_id = start_info['cate_id']
        type_ = start_info['type_']
        cate_id = start_info['cate_id']
        last_page = start_info['last_page']

        query = f"page={page+1}&cate_id={cate_id}&channel_id={channel_id}&type={type_}&last_page={last_page}"
        start_list_url = api_url + '?' + query
        category = '國際娛樂'
        if cate_id == '10090':
            category = '電影'

        print(f'開始{category}第{page_num}頁文章列表')
        print(start_list_url)
        r = requests.get(start_list_url, headers=HEADERS)
        news_data = r.json()
        start_list = news_data['lists']
        time.sleep(random.uniform(1, 2))

        num = 0
        base_url = "https://stars.udn.com"

        for item in start_list:
            num += 1
            print(f'開始第{num}篇文章載入')
            target_url = base_url + item['url']
            print(target_url)
            print(item['title'])
            try:
                article = get_stars_article_info(target_url)
                article_info = {
                    'title': item['title'],
                    'category': category,
                    'tag': '娛樂',
                    'article': article,
                }
                wp_post(article_info)
                print(f'需新聞{category}第{num}篇文章完成')
                print("*" * 30)
            except:
                print(f'需新聞{category}第{num}篇文章失敗')
                pass
            # 更新10篇中斷
            if num >= 10:
                break

    return num

# 最新文章
# channel_id = 1022
# cate_id = 0
# type_ = 'category'
# cate_id= '10087'


def get_pets_article_info(target_url):
    """爬取文章內文資訊"""
    r = requests.get(target_url, headers=HEADERS)
    if r.status_code != requests.codes.ok:
        print('網頁文章資訊載入失敗')
        return {}

    content = BeautifulSoup(r.text, "html.parser")
    # 內文
    article_content = content.find("div", itemprop="articleBody", class_="story")
    # 尋找所有iframe  如果iframe內容是ettoday 就刪除
    for s in article_content.select('iframe'):
        if "ettoday" in s.get("src"):
            s.extract()
    article = article_content.prettify()
    time.sleep(random.uniform(1, 2))

    return article


def get_udn_pets(page_num):
    # 取json頁面
    """爬取pets即時新聞列表"""
    api_url = "https://pets.ettoday.net/more/focus/index.phtml?tag=新聞總覽&xhr=true"

    for page in range(page_num):

        query = f"&page={page+1}"
        pet_list_url = api_url + '?' + query
        print(f'開始寵物第{page_num}頁文章列表')
        print(pet_list_url)
        r = requests.get(pet_list_url, headers=HEADERS)
        if r.status_code != requests.codes.ok:
            print('網頁文章資訊載入失敗')
            return {}

        content = BeautifulSoup(r.text, "html.parser")
        pet_list = content.find_all('h3')
        time.sleep(random.uniform(1, 2))

        num = 0

        for item in pet_list:
            num += 1
            print(f'開始寵物第{num}篇文章載入')
            target_url = 'https:' + item.select_one("a").get("href")
            target_title = item.select_one("a").get("title")
            print(target_url)
            # 取內文
            try:
                article = get_pets_article_info(target_url)
                article_info = {
                    'title': target_title,
                    'category': '寵物',
                    'tag': '萌寵',
                    'article': article,
                }
                wp_post(article_info)
                print(f'寵物第{num}篇文章完成')
                print("*" * 30)
            except:
                print(f'新增寵物第{num}篇文章失敗')
                pass
            # 12篇
            if num >= 10:
                break

    return num


if __name__ == "__main__":
    # # # udn新聞  旅遊
    # tol_bilateral = getudn_news_id(0)
    # print(f"共抓到旅遊 {tol_bilateral} 篇新聞")

    # # # stars即時新聞
    # start_info = {
    #     'channel_id': '1022',
    #     'cate_id': '0',
    #     'type_': 'category',1
    #     'cate_id': '10087',
    #     'last_page': '1813',
    # }
    # start_list = get_udn_stars(start_info)
    # print(f"共抓到即時 {start_list} 篇新聞")

    # # # stars電影新聞
    # start_info = {
    #     'channel_id': '1022',
    #     'cate_id': '0',
    #     'type_': 'category',
    #     'cate_id': '10090',
    #     'last_page': '254',
    # }
    # start_list = get_udn_stars(start_info)
    # print(f"共抓到電影 {start_list} 篇新聞")

    # # pets即時新聞
    pet_list = get_udn_pets(page_num=1)
    print(f"共抓到寵物 {pet_list} 篇新聞")
