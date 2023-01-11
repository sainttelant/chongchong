#import ecal.core.core as ecal_core
#from ecal.core.subscriber import StringSubscriber

import subprocess
import time
import datetime
import os


def recordecal(a,b):
    print(a)
    subprocess.call(["ecal_rec.exe","-r","-n","ecal_mea","--whitelist","ARS4G0_ObjectListPb215","-d",b],shell=True)
if __name__ == "__main__":
    now = datetime.datetime.now()
    currentdate = now.strftime("%Y-%m-%d")
   
    if not os.path.exists("F:/%s/"%(currentdate)):
        os.mkdir("F:/%s/"%(currentdate))
        print("create folder for video recording!")
    recordpath = "F:/%s/"%(currentdate)

    recordecal("begin to record ecal datas",recordpath)
