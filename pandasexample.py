
# coding: utf-8

# In[1]:

import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import time
headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
         'Accept-Encoding':'gzip, deflate, sdch',
         'Accept-Language':'zh-CN,zh;q=0.8',
         'Cache-Control':'max-age=0',
         'Connection':'keep-alive',
         'Cookie':'A4gK_987c_saltkey=TK9kpEHb; A4gK_987c_lastvisit=1495504355; TYID=enANiFkjo/MYuyWsDW+SAg==; __jsluid=653824eccfee41295615cbbcae346fa9; A4gK_987c__public_advert_prefix_20_1=close; A4gK_987c_sendmail=1; A4gK_987c_lastact=1495508764%09ajax.php%09activity; Hm_lvt_556481319fcc744485a7d4122cb86ca7=1495507429,1495508236; Hm_lpvt_556481319fcc744485a7d4122cb86ca7=1495508236',
         'Host':'www.p2peye.com',
         'Referer':'http://bluewhale.cc/2017-05-05/use-python-and-tableau-to-capture-and-visualize-the-data.html',
         'Upgrade-Insecure-Requests':'1',
         'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2853.0 Safari/537.36'
         }
url='http://www.p2peye.com/shuju/ptsj/'
res=requests.get(url,headers=headers)
soup=bs(res.text,'lxml')
name=soup.select('tr.bd td.name')
volume=soup.select('tr.bd td.total')
rate=soup.select('tr.bd td.rate')
pnum=soup.select('tr.bd td.pnum')
cycle=soup.select('tr.bd td.cycle')
plnum=soup.select('tr.bd td.p1num')
fuload=soup.select('tr.bd td.fuload')
alltotal=soup.select('tr.bd td.alltotal')
capital=soup.select('tr.bd td.capital')
operation=soup.select('tr.bd td.operation')

mingzi=[]
chengjiaoe=[]
ll=[]
tzr=[]
jdzq=[]
jkr=[]
mbsd=[]
ljdkye=[]
jzjlr=[]
#生成当前时间
date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
#生成columns
columns=['日期','名称','成交额','利率','投资人','借贷周期','借款人','满标速度','累计贷款余额','净资金流入']
for iname in name:
    mingzi.append(iname.get_text().strip()) 
for ivolume in volume:
    for iivolume in ivolume:
        chengjiaoe.append(iivolume)
for irate in rate:
    for iirate in irate:
        ll.append(iirate)
for ipnum in pnum:
    tzr.append(ipnum.get_text().strip())
for icycle in cycle:
    jdzq.append(icycle.get_text().strip())
for iplnum in plnum:
    jkr.append(iplnum.get_text().strip())
for ifuload in fuload:
    mbsd.append(ifuload.get_text().strip())
for ialltotal in alltotal:
    ljdkye.append(ialltotal.get_text().strip())
for icapital in capital:
    jzjlr.append(icapital.get_text().strip())
#创建数据表
table=pd.DataFrame({'日期':date,'名称':mingzi,'成交额':chengjiaoe,'利率':ll,'投资人':tzr,'借贷周期':jdzq,'借款人':jkr,'满标速度':mbsd,'累计贷款余额':ljdkye,'净资金流入':jzjlr},columns=columns)
table.head()

table.to_csv('C:\\Users\\Administrator\\Desktop\\wdty'+date+'.csv',index=False)





# In[ ]:



