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

def get_stars_article_info(target_url):
    """爬取文章內文資訊"""
    
    r = requests.get(target_url, headers=HEADERS)
    if r.status_code != requests.codes.ok:
        print('網頁文章資訊載入失敗')
        return {}

    content = BeautifulSoup(r.text, "html.parser")
    # 內文
    article_content1 = content.find("div" ,class_ = "article-content__focus")
    article_content2 = content.find("section" ,class_ = "article-content__editor").prettify()
    # 避免沒有圖片
    cont1 = ""
    if article_content1 :
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
        cate_id= start_info['cate_id']
        last_page= start_info['last_page']
        
        query = f"page={page+1}&cate_id={cate_id}&channel_id={channel_id}&type={type_}&last_page={last_page}"
        start_list_url = api_url + '?' + query
        print(f'開始第{page_num}頁文章列表')
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
            article = get_stars_article_info(target_url)
            print(item['title'])
            # print(article)
            print(f'需新聞第{num}篇文章完成')
            print("*" * 30)

            
    return num

if __name__ == "__main__":
    # # stars即時新聞
    start_info = {
        'channel_id' : '1022',
        'cate_id' : '0',
        'type_' : 'category',
        'cate_id' : '10087',
        'last_page' : '1813',
    }
    start_list = get_udn_stars(start_info)
    print(f"共抓到即時 {start_list} 篇新聞")
    
    # # stars電影新聞
    start_info = {
        'channel_id' : '1022',
        'cate_id' : '0',
        'type_' : 'category',
        'cate_id' : '10090',
        'last_page' : '254',
    }
    start_list = get_udn_stars(start_info)
    print(f"共抓到電影 {start_list} 篇新聞")

    