#!/usr/bin/env python
#coding=utf8

from database import DictDatabase
import configpara

def singleton(cls, *args, **kw):  
    instances = {}  
    def _singleton():  
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _singleton  
 
@singleton
class ShellPara(object):
    def __init__(self):
        self.Init()

    def Init(self):
        self.target = ""
        self.script = []
        self.scanfile = []
        self.thread = 10
        self.timeout = 20
        self.callback = None
        self.nums = -1
        self.servertype = ''
        self.dbscripttype = ''
        self.recursion = True

        cp = configpara.ConfigPara()
        cp.Init()

        self.script = cp.scripttype.split(',')
        self.thread = int(cp.threadnum)
        self.timeout = int(cp.timeout)
        self.delaytime = int(cp.delaytime)
        self.SetScanFile(cp.scanfile)

    def SetTarget(self, tg):
        self.target = tg
        self.nums = -1

    def GetRecursion(self):
        return self.recursion

    def SetRecursion(self, val):
        self.recursion = bool(val)

    def GetScriptType(self):
        return self.script
    
    def SetScriptType(self, stype):
        if isinstance(stype, basestring):
            self.script = stype.split(",")
            cp = configpara.ConfigPara()
            cp.SetScriptType(stype)
        else:
            self.script = stype
            cp = configpara.ConfigPara()
            cp.SetScriptType(",".join(stype))

    def GetDBScriptType(self):
        return self.dbscripttype

    def SetDBScriptType(self, stype):
        if "auto" in stype or "scanfile" in stype:
            self.dbscripttype = ""
            return
        if not "common" in stype:
            stype = ["common",] + stype
        self.dbscripttype = stype

    def GetTimeOut(self):
        return self.timeout

    def SetTimeOut(self, timeout):
        cp = configpara.ConfigPara()
        cp.SetTimeout(int(timeout))
        self.timeout = int(timeout)

    def GetDelayTime(self):
        return self.delaytime

    def SetDelayTime(self, delaytime):
        cp = configpara.ConfigPara()
        cp.SetDelayTime(int(delaytime))
        self.delaytime = int(delaytime)

    def GetThreadNum(self):
        return self.thread

    def SetThreadNum(self, tn):
        cp = configpara.ConfigPara()
        cp.SetThreadNum(int(tn))
        self.thread = tn

    def GetPara(self):
        res = 'target: ' + self.target + '\n'
        res += 'script: '
        for i in self.GetDBScriptType():
            res += i + ','
        res += '\n'
        res += 'scanfile: '
        if self.scanfile:
            for i in self.scanfile:
                res += i + ','
        res += '\n'

        res += 'thread: ' 
        res += str(self.thread)
        res += '\n'

        res += 'timeout: ' 
        res += str(self.timeout)
        res += '\n'

        res += 'number: ' 
        res += str(self.nums)
        res += '\n'
        return res 

    def GetScanNum(self):
        if self.nums >= 0:
            return self.nums

        res = 0
        for i in self.GetDBScriptType():
            res += DictDatabase(i).nums()

        if self.scanfile:
            for t in self.scanfile:
                if not t: continue
                with open(t, 'rb') as fp:
                    res += len(fp.readlines())

        self.nums = res    
        return res

    def GetScanFile(self):
        return self.scanfile

    def SetScanFile(self, stype):
        if isinstance(stype, basestring):
            stype = stype.split(",")
        elif isinstance(stype, list):
            pass
        else:
            return

        if "" in stype: stype.remove("")
        cp = configpara.ConfigPara()
        cp.SetScanFile(stype)
        self.scanfile = stype

if __name__ == '__main__':
    tmp = ShellPara()
    tmp.target = "http://www.geostar.com.cn"
    print tmp.GetPara()
    #print tmp.GetScanNum()
