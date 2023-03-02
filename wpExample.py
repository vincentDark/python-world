import functions_framework
from modal.udn import getudn_news_id
from modal.yahooFootball import get_yahoo_football


# 哪一個WP
wp_info = {
    'wp_id':  "kirin",
    'wp_pw':  "d6uz MelW MHa0 p0L4 EkFq wQ2n",
    'wp_url': "https://xn--koy30b585a.net/xmlrpc.php",
}

# udn-sub 籃球
amount = 1  # 數量

# # udn新聞
bilateral = getudn_news_id(6640, amount, wp_info)
print(f"共抓到兩岸 {bilateral} 篇新聞")
stock = getudn_news_id(6645, amount, wp_info)
print(f"共抓到股票 {stock} 篇新聞")
temp = getudn_news_id(6641, amount, wp_info)
print(f"共抓到地方 {temp} 篇新聞")
temp = getudn_news_id(6639, amount, wp_info)
print(f"共抓到社會 {temp} 篇新聞")
temp = getudn_news_id(6649, amount, wp_info)
print(f"共抓到生活 {temp} 篇新聞")
temp = getudn_news_id(7225, amount, wp_info)
print(f"共抓到國際 {temp} 篇新聞")
sport = getudn_news_id(7227, amount, wp_info)
print(f"共抓到體育 {sport} 篇新聞")
obstetrics = getudn_news_id(6644, amount, wp_info)
print(f"共抓到產經 {obstetrics} 篇新聞")

# # yahoo足球
temp = get_yahoo_football(amount, wp_info)
print(f"共抓到yahoo足球第 {temp} 篇新聞")
