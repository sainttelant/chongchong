#!/usr/bin/env python
# coding: utf-8

# In[3]:



#coding:UTF-8
"""
里面用到的主要是os和字符串的截取，可以参考
"""

import os

def aquireDetails(path):
    allthings=os.listdir(path)
    return allthings

def judgeFiles(path,allthing):
    filenames=[]
    for files in allthing:
        abspath=os.path.join(path,files)
        #print("abspath:",abspath)
        if os.path.isdir(abspath):
            print ("it is a folder,ingore it")
        if os.path.isfile(abspath):
            
            """
            reference
            str='https://www.guahao.com/department/125809921947822000?isStd='
            print(str.split('department/')[1].split('?')[0])
            print(str.replace('department/','').replace("https://www.guahao.com/",''))
            """
            tailname=files.split(".")[-1]
            if tailname=="lib":
                
                
                filenames.append(files)
    return filenames

def saveFileNameIntotxt(file,list_thing):
    for filename in list_thing:
        file.write(filename+"\n")
    
    

if __name__=="__main__":
    #print("it begins to get libfilenames") 
    #print("it opened a txt files to store libfile names")
    currentPath=os.getcwd()
    k=aquireDetails(currentPath)
    a=judgeFiles(currentPath,k)
    with open("libfile.txt","w+") as f:
        saveFileNameIntotxt(f,a)
    f.close()
    print("finish aquire lib files'names")







# In[ ]:




