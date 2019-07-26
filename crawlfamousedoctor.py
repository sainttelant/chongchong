
# coding: utf-8

# In[3]:

import requests
from bs4 import BeautifulSoup as bs
import time
import json
import random
import pandas as pd
headers={

'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'accept-encoding':'gzip, deflate, br',
'accept-language':'zh-CN,zh;q=0.8',
'cache-control':'max-age=0',
'upgrade-insecure-requests':'1',
'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

url='https://www.guahao.com/hospital/dde98fc9-4183-48ee-8c84-453058fa7fe3000'
name=[]
title=[]
feature=[]
appointment=[]
score=[]
columns=['姓名','擅长','预约量']
def crawldoc():
    re=requests.get(url,headers=headers)
    soup=bs(re.text,'lxml')
    for clinic in soup.select('p span a.ishao'):
        urlall=clinic['href']
        shuzi=urlall.split('department/')[1].split('?')[0] #把中间href的数字解析出来
        urlall='https://www.guahao.com/department/shiftcase/'+shuzi
        #print(urlall)
        req=requests.get(urlall)
        soup1=bs(req.text,'lxml')
        for nm in soup1.select('dl dt a.name.js-doc em'):
            name.append(nm.get_text())
        for feat in soup1.select('div.g-doctor-item2.g-clear.to-margin div.skill.g-left'):
            feature.append(feat.get_text().replace("\r\n","").replace("\n","").strip())
        #for sc in soup1.select('div.g-doctor-item2.g-clear.to-margin div.num-info.g-left div.stars em'):
            #score.append(sc.get_text())
        for ap in soup1.select('div.num-info.g-left div.count span'):
            appointment.append(ap.get_text())
        urlall1=urlall+'?pageNo=2'
        time.sleep(1)
        req1=requests.get(urlall1)
        soup2=bs(req1.text,'lxml')
        for nm1 in soup2.select('dl dt a.name.js-doc em'):
            name.append(nm.get_text())
        for feat1 in soup2.select('div.g-doctor-item2.g-clear.to-margin div.skill.g-left'):
            feature.append(feat.get_text().replace("\r\n","").replace("\n","").strip())
        #for sc1 in soup2.select('div.g-doctor-item2.g-clear.to-margin div.num-info.g-left div.stars em'):
            #score.append(sc.get_text())
        for ap1 in soup2.select('div.num-info.g-left div.count span'):
            appointment.append(ap.get_text())
    
    return name,feature,appointment[1::2]

if __name__ == '__main__':

    daming,tedian,yuyue=crawldoc()
    table=pd.DataFrame({'姓名':daming,'擅长':tedian,'预约量':yuyue},columns=columns)
    table
    table.to_csv('shuijindoctorinfo.csv',index=False)
    

    
    
    
    

      
       

    
   

   
   
  
 
        
  
       


        
   
       

        
        
        
        
        
            
    
    
    
    
    




# In[4]:

table.head()


# In[5]:

table


# In[ ]:



