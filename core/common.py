#!/usr/bin/env python
#coding=utf8

from database import DictDatabase
from path import Path
from dirpath import DirPath
from cmspath import CmsPath
from Queue import Queue
import configpara
from utils.http import Http
import re
import urlparse
import htmllib
import formatter
import os

__all__ = [
    "AddTasks",
    "AddTasksFromPath",
    "AddTasksToList",
    "GetHtml",
    "PathToScriptType",
    "HtmlToScriptType",
    "GetScriptType",
    "GetServerType",
    "CheckHostOnline",
    "GetHostFilename",
    "InitLog",
    "WriteLog",
]

def AddTasksToList(url, scripttype, lst):
    db = DictDatabase(scripttype)
    for i in db.getPaths():
        if scripttype == 'cmstype':
            path = CmsPath(url, db, i)
            lst.append(path)
        else:
            path = DirPath(url, db, i)
            lst.append(path)

def AddTasks(url, scripttype, queue):
    db = DictDatabase(scripttype) 
    for i in db.getPaths():
        if scripttype == 'cmstype':
            path = CmsPath(url, db, i)
            queue.put(path)
        else:            
            path = DirPath(url, db, i)
            queue.put(path)

def AddTasksFromPath(url, path, queue):
    if not os.path.exists(path):
        return
    for line in open(path, 'rb').readlines():
        line = line.strip()
        path = DirPath(url, None, line)
        queue.put(path)

def GetHtml(host):
    try:
        ht = Http(host, int(configpara.DEFAULT_TIMEOUT_TIME))
        ret = ht.get().data
        return ret
    except Exception,e:
        return ""

def PathToScriptType(path):
    if not path: return ''
    index = path.rfind('.')
    if index < 0:
        return ''

    tmptype = path[index:]
    tmptype = tmptype.replace(".", '')
    if tmptype.lower() in ['do', 'action']:
        return 'jsp'
    if tmptype.lower() in configpara.DICT_TABLE_NAME:
        return tmptype
    else:
        return ''

def HtmlToScriptType(host, info):
    ret = []
    parser=htmllib.HTMLParser(formatter.NullFormatter())  
    parser.feed(info)
    for i in parser.anchorlist:
        result = urlparse.urlparse(str(i))  
        hosturl = result.scheme + "://" + result.netloc 
        if result.scheme != "" and result.scheme != "http" and result.scheme != "https": continue
        if result.netloc != "" and not (result.netloc in host): continue
        path = result.path.strip()
        if not path: continue

        tmptype = PathToScriptType(result.path)
        if tmptype: return tmptype

    return ret
    

def GetScriptType(url):
    stype = PathToScriptType(url)
    if stype: return stype

    info = GetHtml(url)
    stype = HtmlToScriptType(url, info)
    if stype: return stype

    result = urlparse.urlparse(url)  
    hosturl = result.scheme + "://" + result.netloc 
    stype = PathToScriptType(result.path)
    if stype: return stype
    if not result.path: return ''

    info = GetHtml(hosturl)
    stype = HtmlToScriptType(hosturl, info)
    return stype

def GetServerType(url):
    try:
        ht = Http(url, int(configpara.DEFAULT_TIMEOUT_TIME))
        data = ht.head('').data
    except Exception,e:
        return ""

    rep = re.compile("Server: (.*)\r")
    info = rep.findall(str(data))
    info = ''.join(info)
    if info: server = str(info).strip()
    return server


def CheckHostOnline(host):
    try:
        ht = Http(host, int(configpara.DEFAULT_TIMEOUT_TIME))
        data = ht.head('').data
        return True
    except Exception,e:
        return False

def GetHostFilename(url):
    result = urlparse.urlparse(url) 
    logname = "./output/" + result.netloc + ".html"
    return logname


def InitLog(url):
    logname = GetHostFilename(url)
    with open(logname, 'w') as fp: fp.write(configpara.headinfo)

def WriteLog(url, code):
    if code == 404 or code <= 0: 
        return

    logname = GetHostFilename(url)
    info = '<a href="' + url + '">' + url + '</a>' 
    info = info + '<font face="Verdana" color="#FF0000" size="2"> HTTP/1.1 ' + str(code) + '</font><br>'
    with open(logname, 'a') as fp: fp.write(info)

def GetCurrTime():
    import datetime
    now = datetime.datetime.now()
    otherStyleTime = now.strftime("%H:%M:%S")
    return otherStyleTime

if __name__ == "__main__":
    #qt = Queue()
    #AddTasks("http://www.geostar.com.cn", "php", qt)
    #print qt
    #print GetScriptType("http://www.geostar.com.cn/1.phpp")
    #print GetServerType("http://172.16.28.132")
    #print CheckHostOnline("http://172.16.28.132")
    InitLog("http://www.geostar.com.cn")
