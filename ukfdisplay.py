#!/usr/bin/env python
# coding: utf-8

# In[1]:


prelist=[]
afterlist=[]

with open("xuewei.txt","r",encoding='gb18030',errors='ignore') as f:
    for line in f.readlines():
        
        if line[0:15]=="ukffilterBefore":
            #img = np.zeros((1440,2560,3),np.uint8)
            #img.fill(100)
            #print(line)
            preleft=float(line.split("\t")[0].split(":")[1])
            pretop = float(line.split("\t")[1])
            preright = preleft + float(line.split("\t")[2])
            prebottom = pretop + float(line.split("\t")[3])
            pretuple = (round(preleft),round(pretop)),(round(preright),round(prebottom))
            #print(pretuple)
            #cv2.rectangle(img,pretuple[0],pretuple[1],(0,0,255),1)
            prelist.append(pretuple)
            #cv2.rectangle(img,(int(preleft),int(pretop)),(int(preright),int(prebottom)),(0,0,255),1)
            #cv2.imshow("test",img)
            #cv2.waitKey(100)
            #print(preleft,pretop)
        elif line[0:14]=="ukffilterAfter":
            #print(line)
            afterleft=float(line.split("\t")[0].split(":")[1])
            aftertop = float(line.split("\t")[1])
            afterright = afterleft + float(line.split("\t")[2])
            afterbottom = aftertop + float(line.split("\t")[3])
            aftertuple = (round(afterleft),round(aftertop)),(round(afterright),round(afterbottom))
            #print(pretuple)
            #cv2.rectangle(img,pretuple[0],pretuple[1],(0,0,255),1)
            afterlist.append(aftertuple)   

#cv2.destroyAllWindows()


# In[2]:


import cv2
import numpy as np

for pre,after in zip(prelist, afterlist):
    img = np.zeros((1440,2560,3),np.uint8)
    img.fill(100)
    cv2.namedWindow("test",0)
    #print(pre[0][0])
    cv2.rectangle(img,pre[0],pre[1],(0,0,255),3)
    cv2.putText(img,"Pre",(pre[0][0]-5,pre[0][1]-10),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),3)
    cv2.rectangle(img,after[0],after[1],(255,250,0),1)
    cv2.imshow("test",img)
    cv2.waitKey(100)

cv2.destroyAllWindows()
    
    
       


# In[ ]:




