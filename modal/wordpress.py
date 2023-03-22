from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost


def wp_post(wp_info, article_info):
    wp_url = wp_info['wp_url']
    wp_id = wp_info['wp_id']
    wp_pw = wp_info['wp_pw']
    # 送出WP  建立客戶端
    wp = Client(wp_url, wp_id,wp_pw)
    #建立新文章
    post = WordPressPost()
    # post.post_status = "publish"
    post.post_status = "draft"
    post.title = article_info['title']
    post.content = article_info['article']
    tag = article_info['tag']
    category = article_info['category']
    
    post.terms_names = {
        "post_tag": tag,
        "category": [category]
    }
    wp.call(NewPost(post))
    return
