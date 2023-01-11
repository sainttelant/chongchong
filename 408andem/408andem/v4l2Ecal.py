import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber

import subprocess
import time
import datetime
import os


def recordecal(a,b):
    print(a)
    subprocess.check_output(["ecal_rec.exe","-r","-n","ecal_mea","--whitelist","ARS4G0_ObjectListPb215","-d",b])
if __name__ == "__main__":
    now = datetime.datetime.now()
    currentdate = now.strftime("%Y-%m-%d")
   
    abspath = os.getcwd()
    if not os.path.exists(abspath+"ecals/%s/"%(currentdate)):
        os.makedirs(abspath+"ecals/%s/"%(currentdate))
        print("create folder for video recording!")
    recordpath = abspath+"ecals/%s/"%(currentdate)

    recordecal("begin to record ecal datas",recordpath)
