
# coding: utf-8

# In[ ]:

import os
import time
from collections import deque
 


def change_file_name(path):  #传入的就是文件名, 这个函数的目的是修改inl函数，确保改名不覆盖 
    print("放入到change_name的路径：",path)
    path_arr = path.split('.')
    #filename_pre=path_arr[0]
    if len(path_arr)==1:
        #print("这个文件有问题，没有后缀名,经验证可以打开，直接copy，哈哈：",path_arr[0])
        return None
    elif len(path_arr)==2:
        filename_pre=path_arr[0]
        filename_after=path_arr[1]
        if filename_after=="cpp":
            dst_file='%s.%s'%(filename_pre+"_cpp","html")
            #print("CPP filename:",dst_file)
            return dst_file
        elif filename_after=="hpp":
            dst_file='%s.%s'%(filename_pre+"_hpp","html")
            #print("CPP filename:",dst_file)
            return dst_file
        elif filename_after=="inl":
            dst_file = '%s.%s'%(filename_pre+"_inl","html")
            #print("CPP filename:",dst_file)
            return dst_file
        else:
            dst_file="%s.%s"%(filename_pre+"_"+filename_after,"html")
            return dst_file
        
def restoreFiles(path):
    pinjie=path.split(".")[0]
    path_arr = path.split('_')[-1].split(".")  #取倒数第一个_为分界线
    #print('path_arr:',path_arr)
    #filename_pre=path_arr[0]
    if len(path_arr)==1:
        #print("这个文件有问题，没有后缀名,经验证可以打开，直接copy，哈哈：",path_arr[0])
        return None
    elif len(path_arr)==2:
        realsuffix=path_arr[0]
        pinjieh="_"+realsuffix
        dst_file=pinjie.replace(pinjieh,"")+"."+realsuffix
        return dst_file  

def getDirAndCopyFile(sourcePath,targetPath):
    if not os.path.exists(sourcePath):
        return
    if not os.path.exists(targetPath):
        os.makedirs(targetPath)
     
    #遍历文件夹
    for fileName in os.listdir(sourcePath):
        #拼接原文件或者文件夹的绝对路径
        absourcePath = os.path.join(sourcePath, fileName)
        #拼接目标文件或者文件加的绝对路径
        abstargetPath = os.path.join(targetPath, fileName)
        #判断原文件的绝对路径是目录还是文件
        if os.path.isdir(absourcePath):
            #是目录就创建相应的目标目录
            os.makedirs(abstargetPath)
            #递归调用getDirAndCopyFile()函数
            getDirAndCopyFile(absourcePath,abstargetPath)#是文件就进行复制
        if os.path.isfile(absourcePath):
            nameoffile=absourcePath.split('/')[-1]
            #print("是文件，打印当前的absourcePath的文件名:",nameoffile)
            
            newname=change_file_name(nameoffile)
            #print('newname:',newname)
            rbf = open(absourcePath,"rb")
            need2removedstr=abstargetPath.split('/')[-1]
            prepinjie=abstargetPath.replace(need2removedstr,"")
            if newname!=None:
                abstargetPathNew=os.path.join(prepinjie,newname)
                wbf = open(abstargetPathNew,"wb")
                while True:
                    content = rbf.readline(1024*1024)
                    if len(content)==0:
                        break
                    wbf.write(content)
                    wbf.flush()
                rbf.close()
                wbf.close()
            elif newname==None:
                #print("这他妈文件有问题，没有后缀名，我就直接copy操作了，下面跟一下它的路径：",abstargetPath)
                wbf = open(abstargetPath,"wb")
                while True:
                    content = rbf.readline(1024*1024)
                    if len(content)==0:
                        break
                    wbf.write(content)
                    wbf.flush()
                rbf.close()
                wbf.close()
                
def getDirAndCopyFileR(sourcePath,targetPath):
    if not os.path.exists(sourcePath):
        return
    if not os.path.exists(targetPath):
        os.makedirs(targetPath)
     
    #遍历文件夹
    for fileName in os.listdir(sourcePath):
        #拼接原文件或者文件夹的绝对路径
        absourcePath = os.path.join(sourcePath, fileName)
        #拼接目标文件或者文件加的绝对路径
        abstargetPath = os.path.join(targetPath, fileName)
        #判断原文件的绝对路径是目录还是文件
        if os.path.isdir(absourcePath):
            #是目录就创建相应的目标目录
            os.makedirs(abstargetPath)
            #递归调用getDirAndCopyFile()函数
            getDirAndCopyFileR(absourcePath,abstargetPath)#是文件就进行复制
        if os.path.isfile(absourcePath):
            nameoffile=absourcePath.split('/')[-1]
            #print("是文件，打印当前的absourcePath的文件名:",nameoffile)
            
            newname=restoreFiles(nameoffile)
            print('newname in main function:',newname)
            rbf = open(absourcePath,"rb")
            need2removedstr=abstargetPath.split('/')[-1]
            prepinjie=abstargetPath.replace(need2removedstr,"")
            if newname!=None:
                abstargetPathNew=os.path.join(prepinjie,newname)
                wbf = open(abstargetPathNew,"wb")
                while True:
                    content = rbf.readline(1024*1024)
                    if len(content)==0:
                        break
                    wbf.write(content)
                    wbf.flush()
                rbf.close()
                wbf.close()
            elif newname==None:
                #print("这他妈文件有问题，没有后缀名，我就直接copy操作了，下面跟一下它的路径：",abstargetPath)
                wbf = open(abstargetPath,"wb")
                while True:
                    content = rbf.readline(1024*1024)
                    if len(content)==0:
                        break
                    wbf.write(content)
                    wbf.flush()
                rbf.close()
                wbf.close()
        
if __name__ == '__main__':
    startTime = time.clock()
    print("请问master：“您是要破解文件成html，还是解码成源程序，破解选1，还原选0”")
    InputFlag=input("请输入你的选择：破解请输入1，还原请输入0:")
    if InputFlag=="1":
        sourcePath = input("请输入源路径：")
        targetPath = input("请输入copy路径：")
        getDirAndCopyFile(sourcePath,targetPath)
        #时间是用来计算复制总共消耗了多少时间
        endTime = time.clock()
        time_mi = endTime // 60
        time_s = endTime // 1 % 60
        time_ms = ((endTime * 100) // 1) % 100
        print ("总用时:%02.0f:%02.0f:%2.0f" % (time_mi, time_s, time_ms))
    elif InputFlag=="0":
        sourcePath = input("请输入html文件的路径：")
        targetPath = input("请输入还原保存路径：")
        getDirAndCopyFileR(sourcePath,targetPath)
        
        #时间是用来计算复制总共消耗了多少时间
        endTime = time.clock()
        time_mi = endTime // 60
        time_s = endTime // 1 % 60
        time_ms = ((endTime * 100) // 1) % 100
        print ("总用时:%02.0f:%02.0f:%2.0f" % (time_mi, time_s, time_ms))
        


# In[ ]:



