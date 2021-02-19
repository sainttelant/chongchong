#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import random
import os


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
        for file in filelist_src:
            path = os.path.join(os.path.abspath(src_path), file)
            if os.path.isdir(path):
                path1 = os.path.join(os.path.abspath(target_path), file)
                if not os.path.exists(path1):
                    os.mkdir(path1)
                copyandJiami(path, path1, key_file)
            else:
                path2 = os.path.join(os.path.abspath(target_path), file)
                neof = path2 + '.jm'
                crypt_files(path, neof, key_file,file)
        return True
    else:
        return False

def copyandJiemi(src_path, target_path,key_file):
    if not os.path.exists(target_path):
        os.mkdir(target_path)
    if os.path.isdir(src_path) and os.path.isdir(target_path):
        filelist_src = os.listdir(src_path)
        for file in filelist_src:
            path = os.path.join(os.path.abspath(src_path), file)
            if os.path.isdir(path):
                path1 = os.path.join(os.path.abspath(target_path), file)
                if not os.path.exists(path1):
                    os.mkdir(path1)
                copyandJiemi(path, path1, key_file)
            else:
                print("jiemiName:%s:"%(path))
                path2 = os.path.join(os.path.abspath(target_path), file)
                print("path2:",path2)
                path2_suffix = path2.split(".")[-1]
                print(path2_suffix)
                neof = path2.split("."+path2_suffix)[0]
                print("neof:",neof)
                crypt_file(path, neof, key_file)
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
                copyandJiami(args[1], newfolder, args[3])
            exit(0)
        if args[4]=="0":
            copyandJiemi(args[1],args[2],args[3])
            exit(0)

    print('Done!')





