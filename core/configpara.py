#! /usr/bin/env python
#coding=utf-8
import ConfigParser
import os

headinfo = '''<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
<style type="text/css">
<!--
body {  FONT-FAMILY: verdana;  font-size: 10pt; color: #000000} 
-->
</style>
<title>PathScanner v1.0 Report</title>
</head>

<body bgcolor="#FFFFFF">

<p align="left"><font face="Verdana" size="3">
PathScanner v1.0 report
</font></p>
<hr>'''

LOG_PATH        = "./log/logmsg.log"
DICT_PATH_AB    = "D:/pathscanner/" + "./data/dit.s3db"
DICT_PATH       = "./data/dit.s3db"
DICT_TABLE_NAME = ["common", "asp", "jsp", "php", "aspx", ]
CONFIG_FILE_NAME = './config.conf'
DEFAULT_TIMEOUT_TIME = 10
DEFAULT_THREAD_NUM = 10
DEFAULT_SCRIPT_TYPE = "auto"
DEFAULT_DELAY_TIME = 5

def singleton(cls, *args, **kw):  
    instances = {}  
    def _singleton():  
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _singleton  
 
@singleton
class ConfigPara:
    def __init__(self):
        self.scripttype = DEFAULT_SCRIPT_TYPE
        self.threadnum = DEFAULT_THREAD_NUM
        self.timeout = DEFAULT_TIMEOUT_TIME
        self.delaytime = DEFAULT_DELAY_TIME
        self.scanfile = ""

    def Init(self):
        if not os.path.exists(CONFIG_FILE_NAME):
            self.__InitConfFile__()
            return

        try:
            config = ConfigParser.ConfigParser()
            config.read(CONFIG_FILE_NAME)
            tmp = config.get("GLOBAL", "scripttype")
            self.scripttype = tmp
            tmp = config.get("GLOBAL", "threadnum")
            self.threadnum = int(tmp)
            tmp = config.get("GLOBAL", "timeout")
            self.timeout = int(tmp)            
            tmp = config.get("GLOBAL", "delaytime")
            self.delaytime = int(tmp)
            tmp = config.get("GLOBAL", "scanfile")
            self.scanfile = tmp
            self.config = config
        except:
            self.__InitConfFile__()
            return

    def __InitConfFile__(self):
        self.__init__()
        with open(CONFIG_FILE_NAME, 'wb') as fp: pass
        config = ConfigParser.ConfigParser()
        config.add_section("GLOBAL")
        config.set("GLOBAL", "scripttype", self.scripttype)
        config.set("GLOBAL", "threadnum", self.threadnum)
        config.set("GLOBAL", "timeout", self.timeout)
        config.set("GLOBAL", "delaytime", self.delaytime)
        config.set("GLOBAL", "scanfile", self.scanfile)
        with open(CONFIG_FILE_NAME, "w+") as fp:
            config.write(fp)

        self.config = config

    def SaveItem(self, item, value):
        self.config.set("GLOBAL", item, value)
        with open(CONFIG_FILE_NAME, "w+") as fp:
            self.config.write(fp)

    def SetScriptType(self, st):
        if isinstance(st, basestring):
            self.scripttype = st
            self.SaveItem("scripttype", st)
            return

        if not st:
            self.SaveItem("scripttype", '')
        else:
            self.SaveItem("scripttype", ','.join(st))
        self.scripttype = st

    def SetThreadNum(self, tn):
        self.SaveItem("threadnum", int(tn))
        self.threadnum = int(tn)

    def SetTimeout(self, t):
        self.SaveItem("timeout", int(t)) 
        self.timeout = int(t)

    def SetDelayTime(self, t):
        self.SaveItem("delaytime", int(t))
        self.delaytime = int(t)

    def SetScanFile(self, st):
        if not st:
            self.SaveItem("scanfile", '')
        else:
            self.SaveItem("scanfile", ','.join(st))
        self.scanfile = st

if __name__ == "__main__":
    cp = ConfigPara()
    cp.Init()
    print cp.scripttype
    print cp.threadnum
    print cp.timeout
    cp.SetScriptType("jsp")
    cp.SetThreadNum("20")
    cp.SetTimeout("30")
    print cp.scripttype
    print cp.threadnum
    print cp.timeout    
