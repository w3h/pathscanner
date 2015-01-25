#!/usr/bin/env python
#coding=utf8

from path import Path

class CmsPath(Path):
    def __init__(self, url, db, path):
        Path.__init__(self, url, db, path)
        pass
    def GetList(self):
        pass
    def GetResult(self, info):
        pass
    def GetAction(self):
        pass
    
