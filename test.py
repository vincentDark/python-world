import time
import random
import requests
from bs4 import BeautifulSoup
from modal.wordpress import wp_post

# yahoo新聞
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}


def get_health_article_info(target_url):
    """爬取文章內文資訊"""
    url = f'https://www.top1health.com{target_url}'
    r = requests.get(url, headers=HEADERS)
    print(url)
    if r.status_code != requests.codes.ok:
        print('網頁文章資訊載入失敗')
        return {}
    content = BeautifulSoup(r.text, "html.parser")
    # 內文
    section_block = content.find("section", class_="block-wrapper").find("div", class_="single-post")
    tag_list = section_block.find("div", class_="post-tags").find_all("a")
    tags = []
    for tag in tag_list:
        tags.append(tag.text)
    article = section_block.find("div", class_="post-content-area").prettify()
    article_info = {
        'tag': tags,
        'article': article,
    }
    time.sleep(random.uniform(1, 2))

    return article_info


def get_health(category='養生保健', wp_info=0):
    # 欲爬取網址 - ettoday
    target_url = f'https://www.top1health.com/Category/{category}'
    print(target_url)
    r = requests.get(target_url, headers=HEADERS)
    if r.status_code != requests.codes.ok:
        print('網頁文章資訊載入失敗')
        return {}
    soup = BeautifulSoup(r.text, features='html.parser')
    article = soup.find("section", class_="block-wrapper").find("div", class_="post-list")
    item_blocks = article.find_all("div", class_="row")
    print('=' * 30)
    num = 0
    for item_block in item_blocks:
        num += 1
        item = item_block.find("h2")
        title = item.select_one("a").text
        link = item.select_one("a").get("href")
        print(f'華人健康開始第{num}篇文章載入')
        article_info = get_health_article_info(link)
        article_info['tag'].append(category)
        article_info.update({'title': title,'category': '保健資訊分享',})
        print(title)
        try:
            wp_post(wp_info,article_info)
            print(f'華人健康{category}第{num}篇文章完成')
        except:
            print(f'華人健康{category}第{num}篇文章失敗')
            pass
        print("*" * 30)
    return num


if __name__ == "__main__":
    wp_info = {
        'wp_id':  "ad2022min",
        'wp_pw':  "Y4Vm FWYh 9XKX Qmpi 5vws nrop",
        'wp_url': "https://nbnb77.net/xmlrpc.php",
    }
    category = ['養生保健','癌症百科','美麗新知','兩性議題','育嬰親子','減重塑身','吃出健康','癌症百科']
    for i in category:
        temp = get_health(i,wp_info)
        print(f"共抓到健康{i}第 {temp} 篇新聞")
