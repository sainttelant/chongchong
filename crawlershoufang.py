
# coding: utf-8

# In[10]:

import requests
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

headers={'Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
url=input('请输入需要爬虫的５８地址:')

title1=[]
tedian1=[]
price1=[]
phone1=[]
columns=['标题','手机','价格','特点']
def crawlInfo():
    for page in range(0,7):
        urlpage= url+'pn'+str(page)
        re= requests.get(urlpage,headers=headers)
        soup=bs(re.text,'lxml')
        
        for b in soup.select('li h2.title a'):
            urlall=b['href']
            reall=requests.get(urlall)
            time.sleep(1)
            soupp=bs(reall.text,'lxml')
            for ph in soupp.select('p.phone-num'):
                phone1.append(ph.get_text())
              
            for title in soupp.select('div.house-title h1.c_333.f20'):
                title1.append(title.get_text())
            
            for pc in soupp.select('p.house-basic-item1 span.price'):
                price1.append(pc.get_text())
      
            
            for tedian in soupp.select('div.genaral-pic-desc p.pic-desc-word'):
                tedian1.append(tedian.get_text().strip())
    
    return phone1,title1,price1,tedian1


                
                

if __name__ == '__main__':

    phone1,title1,price1,tedian1=crawlInfo()
    table=pd.DataFrame({'标题':title1,'手机':phone1,'价格':price1,'特点':tedian1},columns=columns)
    table.to_csv('szershou.csv',index=False)

           


# In[ ]:



