from selenium import webdriver

from time import sleep 
import traceback

# 用户名，密码 
username = u"sainttelant" 
passwd = u"xue11wei"

 # cookies值得自己去找, 下面两个分别是上海, 营口东 
starts = u"%u6B66%u660C%2CWCN" 
ends = u"%u54C8%u5C14%u6EE8%2CHBB" 
 # 时间格式2016-01-31 
dtime = u"2017-01-18" 
 # 车次，选择第几趟，0则从上之下依次点击 
order = 0 
 ###乘客名 
pa=[u"陆宇明",u"钱学",u"王波"]
# """网址""" 
ticket_url = "http://digital.zjgws.gov.cn/yygh/servlet/SysAction?urlType=index" 
login_url = "https://zjgsmwy.com/sso/login?service=https%3A%2F%2Fzjgsmwy.com%2Fsso%2Foauth2.0%2FcallbackAuthorize&auth2param=%E5%BC%A0%E5%AE%B6%E6%B8%AF%E9%A2%84%E7%BA%A6%E6%8C%82%E5%8F%B7-zjgyygh" 
initmy_url = "http://digital.zjgws.gov.cn/yygh/servlet/SysAction?urlType=index" 

browser=webdriver.firefox()
browser.get(inimy_url)
  
def login():
    
    b.find_by_text(u"登录").click() 
    sleep(3) # sleep是让程序休眠的意思，这里休眠3秒钟
    b.fill("username", username) 
    sleep(1) 
    b.fill("password", passwd) 
    sleep(1) 
    print (u"等待验证码，自行输入...") 
    while True: 
        if b.url != initmy_url: 
            sleep(1) 
        else: 
            break 
  
def huoche(): 
    global b # b这时候变成了全局变量，在huoche（）这个函数里面，b产生了变化，那么在下面函数再调用b的时候，那么使用的b则是函数huoche（）发生变化了的b，不是之前一开始定义的b
    b = Browser(driver_name="chrome") 
    b.visit(ticket_url) 
  
    while b.is_text_present(u"登录"): 
        sleep(1) 
        login() 
        if b.url == initmy_url: 
            break 
  
    try: 
        print(u"挂号打劫，抢号页面，哈哈，我曹来啦") 
 
         # 开始点击自选专家
        b.find_by_text(u'自选专家').click()
        sleep(1)
        b.find_by_tag_name(u"tr").click()
      
    except:
        
        print('尼玛币')
if __name__ == "__main__": 
    huoche() 
