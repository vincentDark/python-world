# coding: utf-8
import base64
import json
import requests
from pprint import pprint


from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost

#網站登入資訊
id="feilyue"
password="IgO1 VDYi jEsn 13nh 265m knWI"

#網站網址，請把example.com替換成你的網址，並且先試著連上該網址，應該會出現「XML-RPC server accepts POST requests only.」才對。
url="https://3k6.net/xmlrpc.php"

#新文章要直接發布的話，就不用改，如果要變成草稿，就改成"draft"
which="publish"
#which="draft"

#建立客戶端
wp = Client(url, id,password)

#建立新文章
post = WordPressPost()
post.post_status = which
post.title = "新文章標題"
post.content = "新文章內容"
post.excerpt = "新文章內容摘要"
post.terms_names = {
    "post_tag": ['Python'],
    "category": ['Python']
}
#如果這一篇是過去的文章，可以透過這個方式指定該文章發表的日期。
#post.date=datetime.strptime("2018/1/01 10:05:10","%Y/%m/%d %H:%M:%S")
#發出去!
wp.call(NewPost(post))
