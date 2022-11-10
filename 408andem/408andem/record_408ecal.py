import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber

import subprocess

def recordecal(a):
    print(a)
    subprocess.call(["ecal_rec.exe","-r","-n","ecal_mea","--whitelist","ARS4G0_ObjectListPb215","-d","F:/"],shell=True)
if __name__ == "__main__":
    recordecal("begin to record ecal")
