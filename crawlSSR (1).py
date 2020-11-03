#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from lxml import etree
from io import BytesIO
import re
from bs4 import BeautifulSoup as soup
import pandas as pd
from pandas.core.frame import DataFrame
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

try:
    import cookielib
except:
    import http.cookiejar as cookielib



class SSR:
    def __init__(self, username, password, country,address,port,pword,security,protobuf,mixed):
        self.username = username
        self.password = password
        self.country = country
        self.address = address
        self.port = port
        self.pword = pword
        self.security = security
        self.protobuf = protobuf
        self.mixed = mixed
        self.headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Host': 'github.com',
                    'Origin': 'https://github.com',
                    'Referer': 'https://github.com/login',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'  
                  } 
        self.profileUrl = 'https://github.com/settings/profile'
        self.loginUrl = 'https://github.com/session'
         # 设置session
        self.session = requests.session()
        # 生成github_cookie文件
        self.session.cookies = cookielib.LWPCookieJar(filename='github_cookie')
    
    def load_cookie(self):
        try:
            self.session.cookies.load(ignore_discard=True)
        except:
            print('cookie aquire not success!!')
            
    def isLogin(self):
        self.load_cookie()
        response = self.session.get(self.profileUrl, headers=self.headers)
        selector = etree.HTML(response.text)
        flag = selector.xpath('//div[@class="column two-thirds"]/dl/dt/label/text()')
        info = selector.xpath('//div[@class="column two-thirds"]/dl/dd/input/@value')
        textarea = selector.xpath('//div[@class="column two-thirds"]/dl/dd/textarea/text()')
        # 登陆成功返回来的个人设置信息
        print(u'个人设置Profile标题: %s'%flag)
        print(u'个人设置Profile内容: %s'%info)
        print(u'个人设置Profile内容: %s'%textarea)
        
    def _token(self):

        response = self.session.get(self.loginUrl, headers=self.headers)

        selector = etree.HTML(response.text)

        token = selector.xpath('//div//input[2]/@value')[0]

        return token
            
    def formLoginData(self):
        r = self.session.get(self.loginUrl, headers = self.headers)
        sp = soup(r.content, "lxml")
        hidden = sp.find_all("input", {'type':'hidden'}) 
        hiddenEx = sp.find_all("input",{'hidden':"hidden"})
        field = str(hiddenEx)
        fieldtext=re.findall('<input class="form-control" hidden="hidden" name="(.+?)" type="text"/>',field)
        #[<input class="form-control" hidden="hidden" name="required_field_1f79" type="text"/>]
        #authenticity_token = re.findall('<input type="hidden" name="authenticity_token" value="(.+?)" />', r.text)
        
        zuhe =[]
        for x in hidden:
            try:
                zuhe.append(eval(str(x).split(" value=")[1].split("/>")[0]))
            except:
                continue
        #print(zuhe[0],zuhe[3],zuhe[4])
        LoginData ={
            'commit': 'Sign in',
            'authenticity_token':zuhe[0], 
            'ga_id': '2031671460.1569298998',
            'login': self.username,
            'password': self.password, 
            'webauthn-support': 'supported',
            'webauthn-iuvpaa-support':' unsupported',
            'return_to':'', 
            'allow_signup':'', 
            'client_id':'', 
            'integration':'', 
             fieldtext[0]:'', 
            'timestamp':zuhe[3],
            'timestamp_secret': zuhe[4]
        }
        ret = self.session.post(self.loginUrl, data=LoginData, headers=self.headers)
        print(ret)
        title = re.findall('<title>(.+?)</title>',ret.text)
        self.session.cookies.save()
        if "GitHub" == title[0]:
            return True
        else:
            return False 
        
    def Switch2Alvin999(self):
        count = 0
        urlalvin ="https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
        headers = {
            'Host': 'github.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
        }
        ret = self.session.get(urlalvin, headers= headers)
        sp =soup(ret.content,"lxml")
        for info in sp.select("td"):
            print(info.get_text())
            count+=1
            if count%7 == 1:
                self.country.append(info.get_text())
            if count%7 ==2:
                self.address.append(info.get_text())
            if count%7 ==3:
                self.port.append(info.get_text())
            if count%7 == 4:
                self.pword.append(info.get_text())
            if count%7 ==5:
                self.security.append(info.get_text())
            if count%7 ==6:
                self.protobuf.append(info.get_text())
            if count%7 ==0:
                self.mixed.append(info.get_text())
        gj = {"国家":self.country}
        dz = {"地址":self.address}
        dk = {"端口":self.port}
        mm = {"密码":self.pword}
        jm ={"加密":self.security}
        xy ={"协议":self.protobuf}
        hh ={"混合":self.mixed}
        return gj,dz,dk,mm,jm,xy,hh
    
def transfer2frame(a,b,c,d,e,f,g):
    fra=DataFrame(a)
    frb=DataFrame(b)
    frc=DataFrame(c)
    frd=DataFrame(d)
    fre =DataFrame(e)
    frf = DataFrame(f)
    frg =DataFrame(g)
    return fra,frb,frc,frd,fre,frf,frg

def send2email():
    sender = '525324158@qq.com'
    receiver1 ='525324158@qq.com'
    psw = 'zfullrbuddrmbhjh'
    content = 'this is a email sended via python'
    msg = MIMEText(content,'html','utf-8')
    msg['From'] = 'who knows'
    msg['To'] = receiver1
    msg['Subject'] = 'whatever'



    #发送word附件
    word = MIMEApplication(open('SSR.csv','rb').read())
    word.add_header('Content-Disposition', 'attachment', filename='SSR.csv')


    multipart = MIMEMultipart()
    multipart.attach(word)

    s = smtplib.SMTP_SSL('smtp.qq.com',465)
    s.login(sender,psw)
    s.sendmail(sender,receiver1,multipart.as_bytes())
    print('succeed')
    

if __name__ =="__main__":
    
    print("it is time to be free now")
    username = 'sainttelant@163.com'
    password = 'Xue198607wei'
    country=[]
    address=[]
    port=[]
    pword=[]
    security=[]
    protobuf=[]
    mixed=[]
    ssrCount = SSR(username, password,country,address,port,pword,security,protobuf,mixed)
    if ssrCount.formLoginData()== True:
        print("Login successfully, begin to switch ssrwebsite!")
        a,b,c,d,e,f,g=ssrCount.Switch2Alvin999()
        aa,bb,cc,dd,ee,ff,gg = transfer2frame(a,b,c,d,e,f,g)
        df=pd.concat([aa,bb,cc,dd,ee,ff,gg],axis=1)
        df.to_csv('SSR.csv',index=0)
        send2email()
    else:
        print("Login Failed！！！")
        
    


# In[ ]:




