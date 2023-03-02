import requests
import os
import openai

OPENAI_API_KEY = "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"
openai.api_key = os.getenv(OPENAI_API_KEY)
openai.Model.list()

# HEADERS = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
# }

# api = 'https://gpt-seo.qq588.cc/api/gpt-seo?prompt='


# # query = '用python创建一个array 里面的值共包含50个不重复心里学专有名词 值是要中文'
# # query = '用python创建一个array 里面的值共包含100个不重复MBA智库各大定律 理論 法則 理論 值是要中文  來源: wiki.mbalib.com'
# # query = '用python创建一个array 里面的值共包含100个不重复各大定律、理论、法则、理论 值是要中文  例如墨非定律、安慰劑效應、阿什法則'
# query = '推薦最好用5款的VPN給我  說明推薦原因 並分析他的優劣'
# # query = '我要做一個有關於360行業的心理學、行銷、經商方面應用的資訊網站 給我想出10個網站說明 有意義  讓人印象深刻 好記憶 '


# url = api + query
# r = requests.get(url, headers=HEADERS)
# data = r.json()

# print(data['text'])


