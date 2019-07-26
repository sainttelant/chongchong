

import json
import requests
from bs4 import BeautifulSoup as bs
import datetime
import time

s=requests.Session()
s.keep_alive = False
headers={'Host':'www.bjguahao.gov.cn',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

kk=[]
def loginbj():
    url='http://www.bjguahao.gov.cn/quicklogin.htm'
    data={'mobileNo':'13915729766',
            'password':'xue11wei',
            'yzm':'',
            'isAjax':'true'}
    res=s.post(url,headers=headers,data=data)
    resp=res.text     #这个返回赋值的是ｓｔｒ格式，然后下面语句就是转化成ｊｓｏｎ，字典格式
    jresp=json.loads(resp)
    if jresp['msg']=='OK':
  
        return True
    else:
        return False

def recheck():
    if loginbj()==True:
        url='http://www.bjguahao.gov.cn/islogin.htm'
        data={'isAjax':'true'}
        res=s.post(url,data=data)
        jresp=json.loads(res.text)
        print('{},您登录成功了'.format(jresp['username']))
        return True
    else:
        print('显然没登录成功，再试试')
        return False
    
def guahao():
    if recheck()==True:
        sortdata()
       
        
        
def sendorder(): #发送手机接收码
    url='http://www.bjguahao.gov.cn/v/sendorder.htm'
    res=s.post(url).text
    jres=json.loads(res)

    if jres['msg']=='OK.':
        print('稍等片刻，等着输入手机接收到的验证码')
    else:
        print('验证码没有成功发送哎,'+jres['msg'])

def shuruma():
    code=input('请输入手机接收到的码：')
    return code

def book():
    hospitalId=input("请输入你想挂号的医院ID，3位码：")
    departmentId=input("请输入想挂的科室ID，9位编码")
    url='http://www.bjguahao.gov.cn/dpt/appoint/'+hospitalId+'-'+departmentId+'.htm'
    res=s.get(url)
    res.encoding='gzip'
    soup=bs(res.text,'html.parser')
    for sy in soup.select('td.ksorder_kyy input'):
        k=sy['value']
        kk.append(k)
    return kk,hospitalId,departmentId

def sortdata():
    validtime,hospitalId,departmentId=book()
    for i in range(0,len(validtime)):
        dutyCode=validtime[i].split('_')[1].split('_')[0]  #上午还是下午
        dutyDate=validtime[i].split('_')[2]
        url='http://www.bjguahao.gov.cn/dpt/partduty.htm'
        data1={'hospitalId':hospitalId,
            'departmentId':departmentId,
            'dutyCode':dutyCode,
            'dutyDate':dutyDate,
            'isAjax':'true'}
        res=s.post(url,data=data1).text
        res=json.loads(res)   #把返回的变成ｊｓｏｎ格式
        data=res['data']
        docname=data[0]['doctorName']
        dutySourceId=data[0]['dutySourceId']
        hospitalId=data[0]['hospitalId']
        departmentId=data[0]['departmentId']
        doctorId=data[0]['doctorId']
        url1='http://www.bjguahao.gov.cn/order/confirm/'+str(hospitalId)+'-'+str(departmentId)+'-'+str(doctorId)+'-'+str(dutySourceId)+'.htm'
        res=s.get(url1,headers=headers)
        res.encoding='gzip'
        soup=bs(res.text,'html.parser')
        for id in soup.select('div.Rese_db dl.Rese_db_dl dd p input'):
            patientid=id['value']
        print('{},是你的就诊医生'.format(docname))
        print('你的就诊日期是{}'.format(dutyDate)+'上午为1，下午为2--{}--'.format(dutyCode))
        sendorder()
        smsverifycode=shuruma()
      
        querystring={
                    'dutySourceId':dutySourceId,
                    'hospitalId':hospitalId,
                    'departmentId':departmentId,
                    'doctorId':doctorId,
                    'patientId':patientid,  #这个要用ｂｅａｕｔｉｆｕｌｓｏｕｐ解析处理
                    'hospitalCardId':'',
                    'medicareCardId':'',
                    'reimbursementType':'5',
                    'smsVerifyCode':smsverifycode,
                    'childrenBirthday':'',
                    'isAjax':'true'}
        url2='http://www.bjguahao.gov.cn/order/confirm.htm'
        res1=s.post(url2,data=querystring,headers=headers)
        jres1=json.loads(res1.text)
        print(jres1['msg'])
        if jres1['msg'] is not None:
            print("抢成功了，退出")
            exit()
        else:
            continue

guahao()




