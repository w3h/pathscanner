#!/usr/bin/env python
#coding=utf8

from shellpara import ShellPara

class Path(object):
    def __init__(self, url, db, path):
        self._url = url
        self._db = db
        self._path = path
        self._sp = ShellPara()
        self._result = ""
        self._code = -1

    def GetList(self):
        ret = []
        if not self._db:
            ret.append(self._path)
            return ret

        if self._path[1] == 's' or  self._path[1] == 'script':
            for i in eval(self._path[0]):
                ret.append(i)
        else:
            ret.append(self._path[0])

        return ret

    def Target(self):
        return self._url

    def GetResult(self):
        return self._result

    def SetResult(self, result):
        self._result = result
    
    def SetCode(self, code):
        self._code = int(code)

    def GetCode(self):
        return self._code

    def GetAction(self):
        pass

    def run(self, info):
        pass
