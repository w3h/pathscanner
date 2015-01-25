#!/usr/bin/env python
#coding=utf8

from path import Path
from utils.http import Http


class DirPath(Path):
    def __init__(self, url, db, path):
        Path.__init__(self, url, db, path)        

    def GetAction(self):
        pass

    def Run(self, info):
        res = self.Check(info)
        return res

    def Check(self, path):
        res = False
        path = self._url + path
        code = -1
        self.SetCode(code)

        try:
            ht = Http(path, int(self._sp.timeout))
            code = ht.head().code
        except Exception, e:
            self.SetResult(str(e))
            self.SaveDb(res)
            return res

        if code != 404 and code > 0:
            res = True
        
        self.SetCode(int(code))
        self.SaveDb(res)
        return res    

    def SaveDb(self, flag):
        if not self._db: return
        self._db.update(self._path[0], flag)

if __name__ == "__main__":
    kk = DirPath("http://www.geostar.com.cn", None, "/robots.txt")
    print kk.Run("/robots.txt")
    print kk.GetResult()
