
# coding: utf-8

# In[62]:

import requests
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
         'Accept-Encoding':'gzip, deflate, sdch',
         'Accept-Language':'zh-CN,zh;q=0.8',
         'Cache-Control':'max-age=0',
         'Connection':'keep-alive',
         'Cookie':'lianjia_uuid=fc884263-f22e-4609-9b53-8e653501153d; gr_user_id=68b3c808-1784-4d16-b4c6-6e897fad4f54; _ga=GA1.3.323323106.1494403486; _smt_uid=591ab2e9.1dd1f26f; UM_distinctid=15c104ae0c426e-070e4c5dfc6566-151c7454-13c680-15c104ae0c546d; _jzqa=1.2036462135474262300.1494921962.1494921962.1494921962.1; _jzqc=1; _jzqy=1.1494921962.1494921962.1.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6%E7%BD%91.-; _jzqckmp=1; _jzqb=1.1.10.1494921962.1; _gid=GA1.2.2046946560.1494921963; select_city=310000; cityCode=sh; gr_session_id_970bc0baee7301fa=cf0bda30-58a4-4dac-aa1e-fddc61dffad4; __xsptplus696=696.2.1494921969.1494922486.28%231%7Cbaidu_zf%7Cppc%7C%25E5%259F%258E%25E5%258C%25BA%25E8%25AF%258D%7C%25E9%2597%25B5%25E8%25A1%258C%25e6%2588%25bf%25e7%25a7%259f%7C%25e6%2588%25bf%25e7%25a7%259f%23%23fZM1lv_mdtS1KMhPZxihjTWXBjA7Z2aW%23; _ga=GA1.2.323323106.1494403486; lianjia_ssid=3b15f89d-df19-42c8-ac4e-2817f3122b7a; ubt_load_interval_b=1494922486326; ubt_load_interval_c=1494922486326; ubta=2299869246.3521605972.1494403486199.1494922460484.1494922486367.32; ubtb=2299869246.3521605972.1494922486369.CFFD98629133EDAFC3332B66793DC946; ubtc=2299869246.3521605972.1494922486369.CFFD98629133EDAFC3332B66793DC946; ubtd=28',
         'Host':'sh.lianjia.com',
         'Upgrade-Insecure-Requests':'1',
         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2853.0 Safari/537.36'
        }
url='http://sh.lianjia.com/chengjiao/'
#定义page
page=('d')
tp=[]
hiInfo=[]
areaInfo=[]
#sizeInfo=[]
for i in range(1,101):
    i=str(i)
    urlnew=url+page+i
    #print(urlnew)
    res=requests.get(urlnew,headers=headers)
    soup=bs(res.text,'lxml')
    time.sleep(0.3)
    price=soup.select('li span.strong-num')
    xiaoqu=soup.select('li a.info-col.text.link-hover-green span.cj-text')
    area=soup.select('li span.row2-text a')
    size=soup.select('li a.info-col.text.link-hover-green')
    for iprice in price:
        totalprice=iprice.string
        tp.append(totalprice)
    for ixiaoqu in xiaoqu:
        hiInfo1=ixiaoqu.get_text()
        hiInfo.append(hiInfo1)
    for iarea in area:
        for wocao in iarea: #循环两次才能取到href里面的数据
            areaInfo.append(wocao)
    #for isize in size:
        #isize=isize.get_text().strip('\xa0\n\t\t\t\t\t\t\t\t\t\t')
        #print(isize)
        #sizeInfo.append(isize)
        #print(sizeInfo)
    areaInfo1=[]
    areaInfo2=[]
    num=int(len(areaInfo)/2)
    for i in range(1,num+1):
        jishu=areaInfo[2*i-2]
        areaInfo1.append(jishu)
        #print(areaInfo1)
    for i in range(1,num+1):
        oushu=areaInfo[2*i-1]
        areaInfo2.append(oushu)
        #print(areaInfo2)

house=pd.DataFrame({'totalprice':tp,'address':hiInfo,'big area':areaInfo1,'specific area':areaInfo2})
house.head() #查看house的列表

#houseinfo_split = pd.DataFrame((x.split('|') for x in house.hiInfo),index=house.index,columns=['xiaoqu']) #将小区的房产信息进行分裂
#houseinfo_split.head()

