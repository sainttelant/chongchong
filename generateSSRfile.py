#!/usr/bin/env python
# coding: utf-8

# In[15]:


import json

def generateconfig(l_server,l_serverPort,l_password,l_methods):
    """
    #这里面传进来的是信息队列，以l打头
    """
    configs =[]
 
    for i in range(len(l_server)):
        if l_methods[i] == None:
            l_methods[i] =""
        file = {
            "server":l_server[i],
            "server_port":l_serverPort[i],
            "local_address": "127.0.0.1",
            "local_port":1080,
            "password":l_password[i],
            "timeout":300,
            "method":l_methods[i],
            "fast_open": False,
            "workers": 1,
            "prefer_ipv6": False
        }
        configs.append(file)
    return configs

def write2json(l_configs):
    for i in range(len(l_configs)):
        with open("/etc/shadowsocks/config%d.json"%(i),'w') as f:
            json.dump(l_configs[i],f)
            print("write %d file to /etc/shadowsocks/"%(i))
            
    
    




