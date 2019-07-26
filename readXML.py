import xml.dom.minidom as xmldom
import os

def readxml(xmlfile):
    #xmlfile = 'C:/Users/bo.li/Desktop/1.xml'
    doc = xmldom.parse(xmlfile) #打开xml文件
    root = doc.documentElement #得到文档元素对象
    #print (root.nodeName) #得到节点的名字。还有nodeValue是结点的值，只对文本结点有效。nodeType是结点的类型

    #获得子标签的名字
    folder = root.getElementsByTagName('folder')
    #print (folder[0].nodeName)  #打印节点名称
    #print (folder[0].firstChild.data)  #打印标签值

    filename = root.getElementsByTagName('filename')
    #print (filename[0].nodeName)
    #print (filename[0].firstChild.data)

    path = root.getElementsByTagName('path')
    #print (path[0].nodeName)
    #print (path[0].firstChild.data)

    database = root.getElementsByTagName('database')
    #print (database[0].nodeName)
    #print (database[0].firstChild.data)

    width = root.getElementsByTagName('width')
    #print (width[0].nodeName)
    #print (width[0].firstChild.data)

    height = root.getElementsByTagName('height')
    #print (height[0].nodeName)
    #print (height[0].firstChild.data)

    depth = root.getElementsByTagName('depth')
    #print (depth[0].nodeName)
    #print (depth[0].firstChild.data)

    segment = root.getElementsByTagName('segmented')
    #print (segment[0].nodeName)
    #print (segment[0].firstChild.data)

    name = root.getElementsByTagName('name') #获取所有‘object’节点
    #print (name[0].nodeName + ": " + name[0].firstChild.data)
    #print (name[1].nodeName + ": " + name[1].nodeName)
    #print (name[2].nodeName + ": " + name[2].firstChild.data)

    xmin = root.getElementsByTagName('xmin')

    ymin = root.getElementsByTagName('ymin')

    xmax = root.getElementsByTagName('xmax')

    ymax = root.getElementsByTagName('ymax')

    rectlist = []
    namelist = []
    if len(name) > 0:
        for i in range(len(name)):
            rect = []
            rect.append(int(xmin[i].firstChild.data))
            rect.append(int(ymin[i].firstChild.data))
            rect.append(int(xmax[i].firstChild.data))
            rect.append(int(ymax[i].firstChild.data))
            rectlist.append(rect)
            namelist.append(name[i].firstChild.data)
    return rectlist, namelist