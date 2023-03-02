import time
import random
import requests
from bs4 import BeautifulSoup
#噓新聞
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}

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
    article = content.find("article" ,class_ = "article-box")
    
    # 文章圖片兩個區塊
    article_content1 = article.find("div" ,class_ = "main-figure")
    article_content2 = article.select_one(".article-body").prettify()
    
    # 避免沒有圖片
    cont1 = ""
    if article_content1 :
        cont1 = article_content1.prettify()

    article_content = cont1 + article_content2
    time.sleep(random.uniform(1, 2))

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
    item_blocks = soup.find_all("div", class_ = "articlebox-compact")
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
            print(f'中時新聞{category}第{num}篇文章完成')
            print("*" * 30)
        except:
            print(f'中時新聞{category}第{num}篇文章失敗')
            pass
        # 載入12篇就好
        if num >= 12:
            break
    return num

if __name__ == "__main__":
    # # 中時新聞
    category = 'sports'
    pet_list = get_china_news(category)
    print(f"共抓到中時 {pet_list} 篇新聞")
    


    