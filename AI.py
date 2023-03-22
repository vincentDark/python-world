import requests
from time import time, sleep
from threading import Thread, Lock
from random import randint, sample
from modal.ai_list_beef import *
from modal.wordpress import wp_post
import openai

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
        openai.api_key = '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'
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=self._query,
            max_tokens=4000,
            temperature=0.5,
        )
        data = response["choices"][0]
        print(f'query: {self._query}')
        if self._type == 'url':
            text = data['img']
        else:
            text = data['text']
        self._openAI.AIarticle({self._type:text})

def main():
    # keyword陣列
    category = '牛肉介紹'
    number = randint(0, 2)
    industry = sample(industry_list, 1)[0]

    # 哪一個WP
    wp_info = {
        'wp_id':  "snack666",
        'wp_pw':  "cAaA a6SE Uwlq Cio7 uTJh TCle",
        'wp_url': "https://wudiniu.net/xmlrpc.php",
    }
    # 開啟多線程
    openAI = OpenAI()
    threads = []
    # 圖片
    # query = f'There are pictures about the {category_img[number]}, science fiction style, and the background should be in the style of science and technology'
    # query = industry

    # t = AddQueryThread(openAI, query, 'url')
    # threads.append(t)
    # t.start()
    
    # 文章1
    query = f'詳細介紹 {industry}'
    t = AddQueryThread(openAI, query, 'text1')
    threads.append(t)
    t.start()

    
    title = f'關於我們的 {industry}' 

    
    if randint(0, 2):
        query = f'寫一篇讚美我們的{industry}產品的文章  內容要有提到我們是有質量保證'
    else:
        query = f'如何吃 {industry} 比較好'
        
    # 文章2
    t = AddQueryThread(openAI, query, 'text2')
    threads.append(t)
    t.start()
    for t in threads:
        t.join()

    print(f'肉:{industry}')
    print(f'標題:{title} / 分類:{category} / 關鍵詞:[{category}][{industry}]')
    print(openAI.article)

    content_text1 = openAI.article.get("text1", "更多資訊等待您的探索")
    content_text2 = openAI.article.get("text2", "更多資訊等待您的探索")

    print('--'*30)
    print('content_text1')
    print(content_text1)
    print('--'*30)
    print('content_text2')
    print(content_text2)
    article_content =  content_text1 + '\n\n' + content_text2
    article_content =  '\n\n' + content_text1 + '\n\n' + content_text2
    article_info = {
        'title': title,
        'category': category,
        'tag': [industry , category],
        'article': article_content,
    }
    wp_post(wp_info, article_info)

if __name__ == '__main__':
    main()

