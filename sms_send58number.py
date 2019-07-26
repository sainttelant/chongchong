# 这个代码非常完整，涉及到爬虫，涉及到page翻页，能够爬虫整站做参考。

import pandas
import requests
from bs4 import BeautifulSoup as bs
import http.client
import urllib
import time
#User_Agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'userid360_xml=9135B1C8241FB4B859E5243A85370EF3; time_create=1505619023762; f=n; f=n; bj58_id58s="Kzk9U0FKakRvdE9ZMjk0OQ=="; id58=c5/ns1jl2Tu5S1qUCQzVAg==; als=0; bdshare_firstime=1491457971664; cookieuid=68a067cc-700c-40e2-94c6-859e4c079f2f; UM_distinctid=15b45baa6e9389-06de7736c3252a-151c7454-13c680-15b45baa6ea2c7; mcity=zz; mcityName=%E9%83%91%E5%B7%9E; nearCity=%5B%7B%22city%22%3A%22zz%22%2C%22cityName%22%3A%22%E9%83%91%E5%B7%9E%22%7D%5D; cookieuid1=c5/n61jm2kGr0l6IBpeUAg==; gr_user_id=2738daaf-d663-4728-bf14-1472c87e735d; Hm_lvt_4d4cdf6bc3c5cb0d6306c928369fe42f=1494920368; Hm_lvt_d32bebe8de17afd6738ef3ad3ffa4be3=1494920369; wmda_uuid=372113da0af6efc1f10c3fbdc9c4ed87; wmda_new_uuid=1; wmda_visited_projects=%3B1409632296065; commontopbar_myfeet_tooltip=end; xxzl_smartid=60cf97a5dddfa22d046b9fbb096fae9a; Hm_lvt_e2d6b2d0ec536275bb1e37b421085803=1501725770; bj58_new_uv=33; Hm_lvt_3bb04d7a4ca3846dcc66a99c3e861511=1501718794; Hm_lvt_e15962162366a86a6229038443847be7=1501718794; GA_GTID=0d303986-0000-5dd6-039d-702107207da5; _ga=GA1.2.404146765.1494920434; myfeet_tooltip=end; city=zz; 58home=zz; firstLogin=true; ipcity=su%7C%u82CF%u5DDE%7C0; __utmt_pageTracker=1; f=n; final_history=31096116318262%2C31098565612619%2C30830485225673%2C30940903161146; ppStore_fingerprint=730535E77CA51CB34611BE7F59D6B0481042DABA0FE3233B%EF%BC%BF1503027060028; __utma=253535702.404146765.1494920434.1501725812.1503027046.5; __utmb=253535702.4.9.1503027060076; __utmc=253535702; __utmz=253535702.1503027046.5.5.utmcsr=zz.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/zhengdongxinqu/xiezl/pve_1092_1/; 58tj_uuid=25a6d68d-d2b3-4ea7-9b2c-fdf692fd9831; new_session=0; new_uv=36; utm_source=; spm=; init_refer=https%253A%252F%252Fwww.baidu.com%252Flink%253Furl%253D6bIIU5JO60VBbJ8SHyQFYG6W5CGc9-punDEmgau8j_7%2526wd%253D%2526eqid%253De7c22e3f000050270000000559965f7d; commontopbar_city=342%7C%u90D1%u5DDE%7Czz; xxzl_deviceid=YZ6jdupfk50SD6SRdP4Pz5xGdgbZ%2BgcllhlbsxlohwFNiUYjmJVXIRvoXWvzGgjK',
'Host':'zz.58.com',
'Referer':'http://zz.58.com/zhengdongxqzb/xiezl/pve_1092_1/?PGTID=0d305766-02c6-1b01-abcc-575e14795621&ClickID=1',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2853.0 Safari/537.36'
}
url='http://zz.58.com/xiezl/pn1/pve_1092_1/?PGTID=0d305766-0015-6469-fc33-e8bd9120640f&ClickID=1'
title1=[]
size1=[]
ph1=[]

host  = "106.ihuyi.com"
sms_send_uri = "/webservice/sms.php?method=Submit"

#用户名是登录用户中心->验证码短信->产品总览->APIID
account  = "C43895399" 
#密码 查看密码请登录用户中心->验证码短信->产品总览->APIKEY
password = "deb80105a52434df75ba8fc7c3fd0686"

def send_sms(text, mobile):
    params = urllib.parse.urlencode({'account': account, 'password' : password, 'content': text, 'mobile':mobile,'format':'json' })
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = http.client.HTTPConnection(host, port=80, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str

def aquire_phone():
    for page in range(1,8):
        page_url='http://zz.58.com/xiezl/pn'+str(page)+'/pve_1092_1/?PGTID=0d305766-0015-6469-fc33-e8bd9120640f&ClickID=1' #循环page页面
        print(page_url)
        time.sleep(2)
        res=requests.get(page_url,headers=headers)
        #print(res)
        soup=bs(res.text,'lxml')
        #print(soup)
        for b in soup.select('div.list-info h2.title a'):
            url_all=b['href']
            html=requests.get(url_all,headers=headers)
            html_soup=bs(html.text,'lxml')
            for title in html_soup.select('div.w.headline h1'):
            
                title1.append(title.get_text().strip()) #可以直接append，不需要定义某某等于某某append
            for size in html_soup.select('ul.info li'):
        
                size1.append(size.get_text().strip())
            for phone in html_soup.select('li.call_2 #t_phone'):
                ph=phone.get_text().strip()
                ph1.append(ph)
    print(len(ph1))
    return ph1 #返回大循环的phone  号码，这样可以获取1到7页的所有号码

if __name__ == '__main__':
    aquire_phone() 
    for mobile1 in ph1:
        print(mobile1)
        #text = "您的验证码是：1289。请不要把验证码泄露给其他人。"
        #print(send_sms(text, mobile1))
