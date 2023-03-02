import time
import random
import requests
from bs4 import BeautifulSoup
#噓新聞
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}


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
    article_content = content.find("div" ,itemprop="articleBody",class_ = "story")
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
            article = get_pets_article_info(target_url)
            print(target_title)
            # print(article)
            print(f'寵物第{num}篇文章完成')
            print("*" * 30)
            
    return num

if __name__ == "__main__":
    # # pets即時新聞
    pet_list = get_udn_pets(page_num=1)
    print(f"共抓到寵物 {pet_list} 篇新聞")
    


    