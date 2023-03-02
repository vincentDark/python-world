import time
import random
import requests
from bs4 import BeautifulSoup


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
}

# udn 聯合新聞網，不同網頁版型範例
# https://udn.com/news/story/6809/4690414
# https://udn.com/news/story/6904/4698001   # https://udn.com/umedia/story/12762/4697096
# https://udn.com/news/story/6809/4699983   # https://global.udn.com/global_vision/story/8663/4698371
# https://udn.com/news/story/6809/4699958   # https://opinion.udn.com/opinion/story/120611/4698526
# https://udn.com/news/story/6812/4700330   # 跳轉"會員專屬內容"

# 即時新聞   
# channelId = 1
# cate_id = 0
# type_ = 'breaknews'

# 分類新聞
# channelId = 2
# type_ = 'cate_latest_news'
# cate_id = 6640[兩岸] 6645[股市] 6644[產經] 

def get_news_list(page_num=1):
    """爬取新聞列表"""
    # 取API  轉json 格式處理
    base_url = "https://udn.com/api/more"

    news_list = []
    for page in range(page_num):
        # 即時新聞
        channelId = 2
        cate_id = 6640
        type_ = 'cate_latest_news'
        query = f"page={page+1}&channelId={channelId}&cate_id={cate_id}&type={type_}"
        news_list_url = base_url + '?' + query
        
        r = requests.get(news_list_url, headers=HEADERS)
        news_data = r.json()
        news_list.extend(news_data['lists'])
        time.sleep(random.uniform(1, 2))

    return news_list

def get_article_info(article_url):
    """爬取文章內文資訊"""
    
    r = requests.get(article_url, headers=HEADERS)
    if r.status_code != requests.codes.ok:
        print('網頁文章資訊載入失敗')
        return {}

    content = BeautifulSoup(r.text, "html.parser")
    article = content.find("section" ,class_ = "article-content__wrapper")
    # 標題
    article_title = article.select_one(".article-content__title").text
    # 分類跟TAG選項
    items = article.select(".breadcrumb-items")
    article_category = items[1].text
    article_tag = items[2].text
    # 文章圖片兩個區塊
    article_content1 = content.find("figure" ,class_ = "article-content__cover").prettify()
    article_content2 = article.select_one(".article-content__editor").prettify()
    article_content = article_content1 + article_content2
    
    article_info = {
            'title': article_title,
            'category': article_category,
            'tag': article_tag,
            'article': article_content,
    }

    return article_info


if __name__ == "__main__":
    # 取API列表幾頁  一頁20篇
    news_list = get_news_list(page_num=1)
    base_url = "https://udn.com"
    for news in news_list:
        news_url = base_url + news['titleLink']
        article_info = get_article_info(news_url)
        print(article_info['title'])
        print(news_url)
        print(article_info['category'])
        print(article_info['tag'])
        print('=' * 30)

        time.sleep(random.uniform(1, 2))
        # break
        
    
    print(f"共抓到 {len(news_list)} 篇新聞")
