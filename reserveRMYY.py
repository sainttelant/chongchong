from bs4 import BeautifulSoup
import requests
import urllib.request
import random
#from PIL import ImageGrab
from PIL import ImageEnhance
from PIL import ImageFilter
from PIL import Image
import pytesseract
import sys
import os
from pytesseract import *

url='http://www.syy.org.cn/'
def get_zjgrenminyy(url):
    web_data=requests.get(url)
    soup=BeautifulSoup(web_data.text,'lxml')
    print(soup.prettify())

get_zjgrenminyy(url)

def getCodePic():  
    randNum = random.random()  
    url = 'https://zjgsmwy.com/sso/servlet/getCode?'+str(randNum)  
    resp = urllib.request.urlopen(url)  
    tmp_pic="c:\\t.gif"  
    open(tmp_pic,"wb").write(resp.read())  
    return tmp_pic

def Handle_Image(Docu_Name,Dist):
    im = Image.open('%s'%(Dist+Docu_Name)+'.gif')  #打开对应目录的png格式的验证码图片
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im=im.convert('RGB')
    im = im.convert('L') #转为黑白图片
    data=im.getdata()
    return im

def qingli2(im):
    for x in range(1,w):    
                #获取目标像素点左右位置
                    left = x - 1
                    right = x + 1
                    
                    for y in range(1,h):
                        
        #获取目标像素点上下位置
                        up = y - 1
                        down = y + 1
                        if x <=12 or x >= (w - 11):
                            im.putpixel((x,y),255)          
                        elif y <= 3 or y >= (h - 3):
                            im.putpixel((x,y),255)
                        elif x>12 and x<(w-11) and y>3 and y<(h-3):
                            up_color = im.getpixel((x,up))
                            down_color = im.getpixel((x,down))
                            left_color = im.getpixel((left,y))
                            left_down_color = im.getpixel((left,down))
                            right_color = im.getpixel((right,y))
                            right_up_color = im.getpixel((right,up))
                            right_down_color = im.getpixel((right,down))
                            left_up_color = im.getpixel((left,up))
                            if down_color <= 60 and left_color >= 240 and left_down_color >=240 and right_color >=240 and right_down_color >=240:
                                im.putpixel((x,y),255)
                                im.save("test2.png","png")
						#去除横线干扰线
                            elif right_color <= 60 and down_color >=240 and right_down_color >=240 and up_color >=240 and right_up_color >=240:
                                im.putpixel((x,y),255)
                                im.save("test3.png","png")
						#去除斜线干扰线
                            elif left_color >=240 and right_color >=240 and up_color >=240 and down_color >=240:
                                im.putpixel((x,y),255)
    else:
        im.save("test1.png","png")
    return im

def Pytess(im):
        threshold = 140
        table = []

        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)

        rep = {'O':'0',
            'I':'1',
            'L':'1',
            'Z':'2',
            'S':'8',
            'Q':'0',
            '}':'7',
            '*':'',
            'E':'6',
            ']':'0',
            '`':'',
            'B':'8',
            '\\':'',
            ' ':''
        }
        im=im.convert('L')
        out = im.point(table,'1')
  
        try:
            text = pytesseract.image_to_string(out)
            text = text.strip()
            text = text.upper()
        except :
            text = 0
            print(text)
        for r in rep:

            text = text.replace(r,rep[r])

        return text

getCodePic()
Dist='C:\\'
Docu_Name='t'
Docu_Names='t'
im=Handle_Image(Docu_Name,Dist)

w,h=im.size
im=qingli2(im)
im.show()

text=Pytess(im)
print(text)







