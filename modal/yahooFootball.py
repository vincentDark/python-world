import time
import random
import requests
from bs4 import BeautifulSoup
from .wordpress import wp_post

# yahoo新聞
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}


def get_yahoofoodball_article_info(target_url):
    """爬取文章內文資訊"""

    r = requests.get(target_url, headers=HEADERS)
    if r.status_code != requests.codes.ok:
        print('網頁文章資訊載入失敗')
        return {}

    content = BeautifulSoup(r.text, "html.parser")
    # 內文
    article = content.find("div", class_="caas-content-wrapper").prettify()
    time.sleep(random.uniform(1, 2))

    return article


def get_yahoo_football(amount, wp_info):
    # 欲爬取網址 - ettoday
    target_url = 'https://tw.sports.yahoo.com/soccer/?guccounter=1'
    # query = f"/{category}/total?chdtv"
    # target_url = url + query
    print(target_url)
    r = requests.get(target_url, headers=HEADERS)
    if r.status_code != requests.codes.ok:
        print('網頁文章資訊載入失敗')
        return {}
    soup = BeautifulSoup(r.text, features='html.parser')
    article = soup.find("div", id="Col1-1-SportsStream").find("ul")
    item_blocks = article.find_all("li")
    num = 0
    # print(item_blocks)
    for item_block in item_blocks:
        num += 1
        item = item_block.find("h3")
        title = item.select_one("a").text
        link = item.select_one("a").get("href")
        print(f'yahoo足球開始第{num}篇文章載入')
        # print(item_block)
        print(title)
        print(link)
        try:
            article = get_yahoofoodball_article_info(link)
            article_info = {
                'title': title,
                'category': '足球',
                'tag': '足球專欄',
                'article': article,
            }
            wp_post(wp_info, article_info)
            print(f'yahoo足球第{num}篇文章完成')
            print("*" * 30)
        except:
            print(f'yahoo足球第{num}篇文章失敗')
            pass
        # 第幾篇中斷
        if num >= amount:
            break
    return num


if __name__ == "__main__":
    # # yahoo足球
    temp = get_yahoo_football()
    print(f"共抓到yahoo足球第 {temp} 篇新聞")
