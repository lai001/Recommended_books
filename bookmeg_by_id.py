import json
import pymysql
import requests
import time

id=4864832
# while id <= 6021450:
# print(id)
#添加headers模拟浏览器
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept - Encoding': 'gzip, deflate, sdch, br',
           'Accept-Language': 'zh-CN,zh;q=0.8',
           'Connection': 'keep-alive',
           'Cookie' : 'bid=N65S4H9y1fI; gr_user_id=40d72ed7-b765-4bfe-80b6-d960e2824f22; viewed="1148282"; as="https://book.douban.com/subject/1148282/"; ps=y; _vwo_uuid_v2=D6C1B0AE0687712718D995662659565A8|2d42a6ecef3e2cbb60baa7ec57104c33; __utmt=1; __utma=30149280.103340410.1527078864.1527078864.1527125172.2; __utmb=30149280.1.10.1527125172; __utmc=30149280; __utmz=30149280.1527125172.2.2.utmcsr=developers.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/wiki/',
           'Host': 'api.douban.com',
           'Upgrade-Insecure-Requests' : '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

url = "https://api.douban.com/v2/book/{ID}"#  网址
url=url.format(ID=id)
# print(url)
msg = requests.get(url,headers=headers,timeout=30)             #请求访问网址
if msg.ok:
    text = json.loads(msg.text)         #得到网址的内容
    # print("评价人数:",text['rating']['numRaters'])
    # print("评分:",text['rating']['average'])
    # print("作者:",text['author'][0])
    # print("书的名字",text['title'])
    length=len(text['tags'])#拥有的标签数，从下标0开始
    tag=''
    for i in text['tags']:
        tag+=i['name']+"\\t"
    # print('书籍标签',tag)
    # print("书的简介:",text['summary'])
    # print("书籍ISBN:",text['isbn13'])

# 连接数据库
connect=pymysql.connect(host="localhost",port=3306,user="root",passwd="",db="py_book",charset="utf8")
# 获取游标
cursor = connect.cursor()
sql="INSERT INTO Book (isbn, book_name, author, average, tags, summary, evaluation_number) VALUES ( '{ISBN}','{book_name}', '{author}', '{average}', '{tags}', '{summary}', '{evaluation_number}' )"
try:
    SQL=sql.format(ISBN=text['isbn13'],book_name=text['title'],author=text['author'][0],average=text['rating']['average'],tags=tag,summary=text['summary'],evaluation_number=text['rating']['numRaters'])
    print(SQL)
    cursor.execute(SQL)
    connect.commit()
except:
    # 如果发生错误则回滚
    connect.rollback()
if cursor:
    cursor.close()
if connect:
    connect.close()
# id+=1
# time.sleep(40)

