
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
#url='http://sh.58.com/qiuzu/'
title1=[]
name1=[]
nn=[]
phone1=[]
columns=['姓名','手机','标题']
def crawlInfo():
    for page in range(0,54):
        urlpage= url+'pn'+str(page)
        re= requests.get(urlpage,headers=headers)
        #print(re)
        soup=bs(re.text,'lxml')
        time.sleep(1)
        for b in soup.select('tr a.t'):
            urlall=b['href']
            reall=requests.get(urlall)
            time.sleep(1)
            soupp=bs(reall.text,'lxml')
            for ph in soupp.select('#t_phone'): 
                try:
                    a=int(ph.contents[0])
                    phone1.append(a)

                    for title in soupp.select('h1'):
                        title1.append(title.get_text().strip())
                    for name in soupp.select('.tx'):
                        name1.append(name.get_text().strip())
                except:
                    continue
    


    return name1[1::2],phone1,title1     #返回的类型是tuple的，注意,[1::2]:代表取偶数位，【：：２】：代表取奇数位
    
    
if __name__ == '__main__':

    xingming,shouji,biaoti=crawlInfo()
    table=pd.DataFrame({'姓名':xingming,'手机':shouji,'标题':biaoti},columns=columns)
    table.to_csv('szinfo.csv',index=False)

