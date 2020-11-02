#!/usr/bin/env python
# coding: utf-8

# In[16]:


import sys
import os
import math 
import matplotlib.pyplot as plt 
from matplotlib.pyplot import MultipleLocator
import numpy as np

def readtxtfile(name):
    list_x = []
    list_y = []
    with open(name+'.txt','r') as f:
        lines= f.readlines()
        for line in lines:
            x = line.strip().split(",")[0]
            y = line.strip().split(",")[1]
            list_x.append(x)
            list_y.append(y)
        return list_x, list_y

def draw(l_x, l_y,label_name,colorc):
    plt.scatter(l_x, l_y ,color=colorc,label= label_name)
   
    plt.ylabel('Y axis')
    plt.xlabel('X axis')

    
        

        
if __name__ == "__main__":
    name = input("input the name of txt:")
    name1 = input("input the name of leftb data")
    name2 = input("input the name of rightb data")
    plt.title('polyLine Chart')
    a, b= readtxtfile(name)
    c, d = readtxtfile(name1)
    e,f = readtxtfile(name2)
    namestring="sandian"
    color1 = "r"
    color2 ='b'
    color3 ='g'
    draw(a, b, namestring,color1)
    draw(c, d, namestring,color2)
    draw(e, f, namestring,color3)
    plt.show()
    


# In[8]:


import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
#从pyplot导入MultipleLocator类，这个类用于设置刻度间隔
  
x_values=list(range(11))
y_values=[x**2 for x in x_values]
plt.plot(x_values,y_values,c='green')
plt.title('Squares',fontsize=24)
plt.tick_params(axis='both',which='major',labelsize=14)
plt.xlabel('Numbers',fontsize=14)
plt.ylabel('Squares',fontsize=14)
x_major_locator=MultipleLocator(1)
#把x轴的刻度间隔设置为1，并存在变量里
y_major_locator=MultipleLocator(10)
#把y轴的刻度间隔设置为10，并存在变量里
ax=plt.gca()
#ax为两条坐标轴的实例
ax.xaxis.set_major_locator(x_major_locator)
#把x轴的主刻度设置为1的倍数
ax.yaxis.set_major_locator(y_major_locator)
#把y轴的主刻度设置为10的倍数
plt.xlim(-0.5,11)
#把x轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白
plt.ylim(-5,110)
#把y轴的刻度范围设置为-5到110，同理，-5不会标出来，但是能看到一点空白
plt.show()


# In[ ]:




