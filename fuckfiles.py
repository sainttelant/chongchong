
# coding: utf-8

# In[1]:

import os
dirpaths=[]
fileph=[]
filenms=[]


def aquireDetails(path):
    allthings=os.listdir(path)
    return allthings

def copyFiles(allthings):
    #print("current folder:",os.getcwd())
    for file in allthings:
        print("current processing files or folder:",file)
        Olddir = os.path.join(path, file)+"/"
        abspath=os.path.join(os.getcwd(),Olddir)
        abspath=os.path.abspath(__file__)
        print("current abspath:",abspath)
        if os.path.isdir(abspath):     #这个必须是绝对路径才能使用，晕！
            print("this is a folder,now,display it:",file)
            os.chdir(path+"/"+file)
            print("lianjie caozuo:::",path+"/"+file)
            print("current folder,should be entired,otherwise,the operation isn't correct!",os.getcwd())
            details=aquireDetails(os.getcwd())
            copyFiles(details)
        else:
            filename = os.path.splitext(file)[0];  
            filetype = os.path.splitext(file)[1]; 
            filePath=path+filename+filetype
            newname=path+filename
            print("copying operation now")
            #os.system("copy"+" "+filename+filetype+" "+filename+".html")
            #print ("current operation folder and processing details::",os.getcwd(),"copy"+" "+filename+filetype+" "+filename+".html")


    
        
if __name__ =="__main__":
    """
    #print "plz ensure the input folder only containing single layer folder,no folder inside anymore"
    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    print "<<<<<<<<<<    Rule One: plz ensure the input folder only containing>>>>>>>>>>>>>" 
    print "<<<<<<<<<<    single layer folder,no folder inside anymore        >>>>>>>>>>>>>>"
    print "<<<<<<<<<<    Rule Two: eg.input test11// or test11//dw_base      >>>>>>>>>>>>>>"
    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    """
    path=input("input the path of folders::")
    
    k=aquireDetails(path)
    copyFiles(k)
    print("files in above folders copied done!!!!!!!",fileph)
    






# In[ ]:

k


# In[ ]:



