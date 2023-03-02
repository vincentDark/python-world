import requests
from time import time, sleep
from threading import Thread, Lock
from random import randint, sample
from modal.ai_list import *
from modal.wordpress import wp_post

class OpenAI(object):

    def __init__(self):
        self._article = {}
        self._lock = Lock()

    def AIarticle(self, text):
        # 先获取锁才能执行后续的代码
        self._lock.acquire()
        try:
            print('-'*30)
            self._article.update(text)
        finally:
            # 在finally中执行释放锁的操作保证正常异常锁都能释放
            self._lock.release()

    @property
    def article(self):
        return self._article


class AddQueryThread(Thread):

    def __init__(self, openAI, query, type):
        super().__init__()
        self._openAI = openAI
        self._query = query
        self._type = type

    def run(self):
        print(f'query: {self._query}')
        if self._type == 'url':
            url = api_img + self._query
        else:
            url = api + self._query
            
        r = requests.get(url, headers=HEADERS)
        data = r.json()
        if self._type == 'url':
            text = data['img']
        else:
            text = data['text']
        self._openAI.AIarticle({self._type:text})

def main():
    # keyword陣列
    select_list = [can_up,how_do_good,sell,can_up+how_do_good+sell+Psychology, feeling+mba]
    category = ['個人學習提升','企業品牌','企業行銷','實際應用','心理學','心理學']
    category_img = ['Personal Learning Improvement','Corporate Brand','Corporate Marketing','Practical Application','spiritual mind','mind control']
    # 亂數 選擇哪一個分類  3為單純企業實際應用  4為心理學  5為心理學談論
    number = randint(0, 4)
    if number > 3:
        # 心理學
        industry = sample(Psychology, 1)[0]
    else:
        # 行業
        industry = sample(industry_list, 1)[0]
    # 關鍵詞
    keyword = sample(select_list[number], 1)[0]

    # 哪一個WP
    wp_info = {
        'wp_id':  "ad2022min",
        'wp_pw':  "2pVi 6S7x YkME fQBG z7p6 AUoU",
        'wp_url': "https://happycity.info/xmlrpc.php",
    }
    # 開啟多線程
    openAI = OpenAI()
    threads = []
    # 圖片
    query = f'There are pictures about the {category_img[number]}, science fiction style, and the background should be in the style of science and technology'
    t = AddQueryThread(openAI, query, 'url')
    threads.append(t)
    t.start()
    
    # 文章1
    if number > 3:
        if randint(0, 1) == 0:
            query = f'給我 {industry} 詳細應用與如何有效學習提升'
        else:
            query = f'詳細分析{mba}概論 與{mba}的實際應用並舉例'
    else:
        if randint(0, 1) == 0:
            query = f'給我 {keyword} 詳細應用與如何有效學習提升'
        else:
            query = f'詳細分析 {industry} 如何發展與優劣。 分析他如何跨業發展  實現協同效應'
    t = AddQueryThread(openAI, query, 'text1')
    threads.append(t)
    t.start()

    
    match number:
        case 0:
            if randint(0, 3):
                title = f'{industry}者如何有效學習{keyword}能力' 
            else:
                title = f'如何有效提升自我{keyword}能力' 

        case 1:
            if randint(0, 3):
                title = f'{industry}如何做好企業的{keyword}'
            else:
                title = f'企業如何做好{keyword}'

        case 2:
            if randint(0, 3):
                title = f'{industry}如何有效提升{keyword}'
            else:
                title = f'如何有效提升{keyword}'
        
        case 3:
            title = f'{industry}關於{keyword}的實際應用'
        
        case 4 | 5:
            if randint(0, 3):
                title = f'從{industry}談論{keyword}'
            else:
                title = f'關於{keyword}的剖析與概論'
        
        case _:
            if randint(0, 3):
                title = f'從{industry}談論{keyword}'
            else:
                title = f'關於{keyword}的剖析與概論'

    if number >= 3:
        query = f'給我一篇非常詳細的 {title}文章 並列出相關具體應用舉例'
    else:
        query = f'給我 {title} 非常詳細的教程步驟 與每個步驟具體如何操作'
        
    # 文章2
    t = AddQueryThread(openAI, query, 'text2')
    threads.append(t)
    t.start()
    for t in threads:
        t.join()

    print(f'行業:{industry} / 亂數:{number} / 關鍵詞:{keyword}')
    print(f'標題:{title} / 分類:{category[number]} / 關鍵詞:[{keyword}][{industry}]')
    print(openAI.article)

    content_url = openAI.article.get("url", "更多資訊等待您的探索")
    content_text1 = openAI.article.get("text1", "更多資訊等待您的探索")
    content_text2 = openAI.article.get("text2", "更多資訊等待您的探索")
    img = f'<img src="{content_url}" alt="{title}">'
    print('img')
    print(img)
    print('--'*30)
    print('content_text1')
    print(content_text1)
    print('--'*30)
    print('content_text2')
    print(content_text2)
    article_content = img + '\n\n' + content_text1 + '\n\n' + content_text2
    # article_content =  '\n\n' + content_text1 + '\n\n' + content_text2
    article_info = {
        'title': title,
        'category': category[number],
        'tag': [industry , keyword],
        # 'tag': keyword,
        'article': article_content,
    }
    wp_post(wp_info, article_info)

if __name__ == '__main__':
    main()

