#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import random
import os
import zipfile
import shutil

def copy_dir(src_path, target_path):
    if os.path.isdir(src_path) and os.path.isdir(target_path):
        filelist_src = os.listdir(src_path)
        for file in filelist_src:
            path = os.path.join(os.path.abspath(src_path), file)
            if os.path.isdir(path):
                path1 = os.path.join(os.path.abspath(target_path), file)
                if not os.path.exists(path1):
                    os.mkdir(path1)
                copy_dir(path, path1)
            else:
                with open(path, 'rb') as read_stream:
                    contents = read_stream.read()
                    path1 = os.path.join(target_path, file)
                    with open(path1, 'wb') as write_stream:
                        write_stream.write(contents)
        return True

    else:
        return False

def copyandJiami(src_path, target_path,key_file):

    if os.path.isdir(src_path) and os.path.isdir(target_path):
        filelist_src = os.listdir(src_path)
        logfile ="cryptlog.txt"
        logfile_path = os.path.join(os.getcwd(), logfile)
        for file in filelist_src:
            if file[0]==".":
                continue
            path = os.path.join(os.path.abspath(src_path), file)
            if os.path.isdir(path):
                if file =="navi":
                    print("this is navi link folder!!--continue!!")
                    continue
                path1 = os.path.join(os.path.abspath(target_path), file)
                if not os.path.exists(path1):
                    os.mkdir(path1)
                copyandJiami(path, path1, key_file)
            else:

                # 直接copy .patch结尾的文件
                if ".patch" in file:
                    #使用shutil 进行拷贝文件
                    """
                    path1 = os.path.join(os.path.abspath(target_path), file)
                    shutil.copy(path, path1)
                    """
                    print("this file %s ends with .patch, continue!!!"%(file))
                    path1 = os.path.join(os.path.abspath(target_path), file)
                    print("its absolute path is:",path1)
                    # 输出文件log 
                    
                    with open(logfile_path, "a") as log:
                        log.write("its absolute path is:%s"%path1+"\n\n")
                elif ".so" in file and file.split(".")[-1]=="so":
                    print("this file is so,just copy it")
                    path1 = os.path.join(os.path.abspath(target_path), file)
                    shutil.copy(path, path1)
                    with open(logfile_path, "a") as log:
                        log.write("Copy %s to the destination:%s"%(file,os.path.abspath(target_path))+"\n\n")
                elif ".a" in file and file.split(".")[-1] == "a":
                    print("this file is .a file, just copy it")
                    path1 = os.path.join(os.path.abspath(target_path), file)
                    shutil.copy(path, path1)
                    with open(logfile_path, "a") as log:
                        log.write("Copy %s to the destination:%s"%(file,os.path.abspath(target_path))+"\n\n")
                elif file.split(".")[-1]=="zip" and ".zip" in file:
                    print("this file is .zip file, just copy it")
                    path1 = os.path.join(os.path.abspath(target_path), file)
                    shutil.copy(path, path1)
                    with open(logfile_path, "a") as log:
                        log.write("Copy %s to the destination:%s"%(file,os.path.abspath(target_path))+"\n\n")
                else:
                    path2 = os.path.join(os.path.abspath(target_path), file)
                    neof = path2 + '.jm'
                    #crypt_files(path, neof, key_file,file)
                    supercrypt_files(path,neof,key_file,file)
        return True
    else:
        return False

def copyandJiemi(src_path, target_path,key_file):
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    if os.path.isdir(src_path) and os.path.isdir(target_path):
        logfile ="jiemiLog.txt"
        logfile_path = os.path.join(os.getcwd(), logfile)

        filelist_src = os.listdir(src_path)
        for file in filelist_src:
            if file[0]==".":
                continue
            path = os.path.join(os.path.abspath(src_path), file)
            if os.path.isdir(path):
                path1 = os.path.join(os.path.abspath(target_path), file)
                if not os.path.exists(path1):
                    os.mkdir(path1)
                copyandJiemi(path, path1, key_file)
            else:
                if ".patch" in file:
                    print("this file %s ends with .patch, manually copy!!!"%file)
                    patch_file_path = os.path.join(os.path.abspath(target_path),file)
                    print("this patch file's destination path is:",patch_file_path)
                    with open(logfile_path,"a") as jiemilog:
                        jiemilog.write("patch file path should be manually copied to the %s"%patch_file_path+"\n\n")

                elif ".so" in file and file.split(".")[-1]=="so":
                    print("this file is so,just copy it")
                    path1 = os.path.join(os.path.abspath(target_path), file)
                    shutil.copy(path, path1)
                    with open(logfile_path, "a") as log:
                        log.write("Copy %s to the destination:%s"%(file,os.path.abspath(target_path))+"\n\n")
                elif ".a" in file and file.split(".")[-1] == "a":
                    print("this file is .a file, just copy it")
                    path1 = os.path.join(os.path.abspath(target_path), file)
                    shutil.copy(path, path1)
                    with open(logfile_path, "a") as log:
                        log.write("Copy %s to the destination:%s"%(file,os.path.abspath(target_path))+"\n\n")
                elif file.split(".")[-1]=="zip" and ".zip" in file:
                    print("this file is .zip file, just copy it")
                    path1 = os.path.join(os.path.abspath(target_path), file)
                    shutil.copy(path, path1)
                    with open(logfile_path, "a") as log:
                        log.write("Copy %s to the destination:%s"%(file,os.path.abspath(target_path))+"\n\n")

                else:
                    print("jiemiName:%s:"%(path))
                    path2 = os.path.join(os.path.abspath(target_path), file)
                    print("path2:",path2)
                    path2_suffix = path2.split(".")[-1]
                    #print(path2_suffix)
                    neof = path2.split("."+path2_suffix)[0]
                    print("neof:",neof)
                    newpath = Super_jiemifiles(path, neof,key_file)
                    print("newpath:",newpath)
                    crypt_file(path, newpath, key_file)
        return True
    else:
        return False


def gen_key():
    c=list(range(100))
    #random.shuffle(c)
    return c
 
def save_keyfile(k,f):
    fo=open(f,'wb')
    fo.write(bytes(k))
    fo.close()

def get_key(f):
    fi=open(f,'rb')
    k=fi.read()
    fi.close()
    return k

def crypt_file(fi,fo,key_file):
    print("Jiemi inputfile:",fi)
    print("Jiemi outputfile:",fo)
    print("key_file",key_file)
    if fi == " " or fo == " " or key_file == " ":
        return
    k=get_key(key_file)
    try:
        f=open(fi,'rb')
        fc=f.read()
        fe=open(fo,'wb')
        flen=len(fc)
        buff=[]
        for i in range(flen):
            c=i%len(k)
            fo=fc[i]^k[c]
            buff.append(fo)
        fe.write(bytes(buff))
        f.close()
        fe.close()
    except:
        print("it happened wired things! open a directory probably")

def Super_jiemifiles(fi,fo, key_file):
    print("Input Jiemifiles:",fi)
    print("Output Jiemifiles:",fo)
    #取到加密的文件name
    filename = fo.split("/")[-1]
    prefix_name = fo.split(filename)[0]
    print('prefix_name：',prefix_name)
    print("filename:",filename)
    if "nimabi" in filename and filename[0] == "n" and filename[2]=="m":
        filename=filename.split("nimabi")[1]
        filename = prefix_name + filename
        return filename
    else:
        jiemifilename = Jiemi_filename(filename, key_file)
        print("huanyuan name:", jiemifilename)
        # 构造真实的绝对路径
        absolutepath = fo.split(filename)[0]  + jiemifilename
        print("absolutepath:", absolutepath)
        return absolutepath

def Jiemi_filename(name,key_file):
    print("jiemi's filename:",name)
    name = name.encode('utf-8')
    print(name, type(name))
    # length of namebytes
    k = get_key(key_file)
    namelength = len(name)
    buff = []
    tmp = ""
    for i in range(namelength):
        c = i % len(k)
        tmp = name[i] ^ k[c]
        buff.append(tmp)
        # 转成bytes
    cryptname = bytes(buff)
    # 转成str类型返回
    cryptname = cryptname.decode()
    return  cryptname

def crypt_filename(name,key_file):
    print("filename:",name)
    # 将字符串转成bytes
    name = name.encode('utf-8')
    print(name, type(name))

    #length of namebytes
    k = get_key(key_file)
    namelength= len(name)
    buff =[]
    tmp = ""
    for i in range(namelength):
        c=i%len(k)
        tmp=name[i]^k[c]
        buff.append(tmp)
    #转成bytes
    cryptname = bytes(buff)
    #转成str类型返回
    cryptname=cryptname.decode()
    notallowed =["?","*",":","<",">","/","\\",'|',"\""]
    for elments in notallowed:
        if elments in cryptname:
            print("newname contains illegal character, use original name")
            # 加上一个标志字符前缀
            return "nimabi"+bytes.decode(name)

    print("use crypt name to process")
    return cryptname

def crypt_files(fi,fo,key_file,name):
    print("fi",fi)
    print("f0",fo)
    print("key_file",key_file)
    if fi == " " or fo == " " or key_file == " ":
        return
    k=get_key(key_file)
    f=open(fi,'rb')
    fc=f.read()
    fe=open(fo,'wb')
    flen=len(fc)
    buff=[]
    for i in range(flen):
        c=i%len(k)
        fo=fc[i]^k[c]
        buff.append(fo)
    fe.write(bytes(buff))
    f.close()
    fe.close()

def supercrypt_files(fi,absfo,key_file,name):
    """
    这种方法无能为力了，因为windows含有八种字符不能作为名字使用
    共有九个敏感字符，分别是 ? * : " < > \ / |
    改进一下，出现以上字符用原来的名称

    """
    print("fi",fi)
    print("absfo:",absfo)
    print("key_file",key_file)
    if fi == " " or key_file == " ":
        return
    k=get_key(key_file)

    f=open(fi,'rb')
    fc=f.read()

    #生成新的name
    absfo = absfo.split(name)[0]
    print("absfo:", absfo)
    newname = crypt_filename(name, key_file)
    newname = absfo+newname+".jm"
    print("filenewname:",newname)
    

    try:
        fe = open(newname,"wb")
        flen=len(fc)
        buff=[]
        for i in range(flen):
            c=i%len(k)
            fo=fc[i]^k[c]
            buff.append(fo)
        fe.write(bytes(buff))
        
    except:
        print("it uses nimabi name anyway!!!!!")
        newname = "nimabi"+ name
        newname = absfo+newname+".jm"
        fe=open(newname,"wb")
        print("after reopen files........!!!!")
        flen=len(fc)
        buff=[]
        for i in range(flen):
            c=i%len(k)
            fo=fc[i]^k[c]
            buff.append(fo)
        fe.write(bytes(buff))
    f.close()
    fe.close()
    




if __name__=='__main__':
    print(">>>>>>>>>>USE instruction<<<<<<<<<<")
    print("first to generate a Key file------")
    print("plz run : python3 jiamijiemi yaoshi.txt")
    print(" generate keyfile!!!!!! at first")
    print("plz run : python3 jiamijiemi <Input folder><output folders> <Keyfile> <1:jiami>")
    print("plz run : python3 jiamijiemi <Input folder><output folders> <Keyfile> <0:jiemi>")
    print("plz run Name JiaMI test : python3 jiamijiemi <FilesName> <Keyfile>")
    args=sys.argv
    arg_num=len(args)
    if arg_num==2:
        neokey=gen_key()
        save_keyfile(neokey,args[1])
        print('Key file has been generated:%s' % (args[1]))
        exit(0)

    if arg_num == 3:
        nameJiami = crypt_filename(args[1],args[2])
        print ("nameJiami:",nameJiami)
        print(type(nameJiami))

        nameJiemi = crypt_filename(nameJiami,args[2])
        print ("nameJiemi:",nameJiemi)



    if arg_num ==5:
        if args[4]=="1":
            newfolder = os.getcwd()
            newfolder = newfolder + "/" + args[2]
            print("outputfiles:",args[2])
            if os.path.exists(newfolder) == False:
                os.makedirs(newfolder)
                if args[1].split(".")[-1] == "zip":
                    print("input folder is zip file!!!")
                    crypt_bz2file(args[1],newfolder,args[3])
                else:
                    print("inputfiles'suffix:",args[1].split(".")[-1])
                    copyandJiami(args[1], newfolder, args[3])
            exit(0)
        if args[4]=="0":
            copyandJiemi(args[1],args[2],args[3])
            exit(0)

    print('Done!!!!!')





