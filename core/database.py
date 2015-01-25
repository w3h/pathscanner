#!/usr/bin/env python
#coding=utf8
from __future__ import division
import sqlite3
import configpara
import threading

# thread lock
lock = threading.Lock()

class DictDatabase:
    def __init__(self, scriptType):
        try:
            self._sqlite_conn = sqlite3.connect(configpara.DICT_PATH, check_same_thread = False)
            self._sqlite_cursor = self._sqlite_conn.cursor()  
            self._scriptType = scriptType
        except:
            self._sqlite_conn = sqlite3.connect(configpara.DICT_PATH_AB, check_same_thread = False)
            self._sqlite_cursor = self._sqlite_conn.cursor()  
            self._scriptType = scriptType

    def getPaths(self):
        if not self._scriptType:
            print "[!] scriptType is invalid"
            return

        sql_select = "SELECT PATH,TYPE FROM %s order by RATE DESC;" % self._scriptType 
        self._sqlite_cursor.execute(sql_select)  
        return self._sqlite_cursor.fetchall()

    def nums(self):
        if not self._scriptType:
            print "[!] scriptType is invalid"
            return

        sql_select = "SELECT count(*) FROM %s;" % self._scriptType 
        self._sqlite_cursor.execute(sql_select)  
        return int(self._sqlite_cursor.fetchone()[0])

    def update(self, path, flag):
        if not path:
            print "[!] path is invalid"
            return
        if not self._scriptType:
            print "[!] scriptType is invalid"
            return

        try:
            lock.acquire(True)
            self._sqlite_cursor.execute("SELECT * FROM " + self._scriptType + " where PATH = ?;", (path,))

            for row in self._sqlite_cursor:
                scan_num = row[3] + 1
                success_num = row[4]
                if flag: success_num = row[4] + 1
                rate = "%.2f" % ((success_num / scan_num) * 100)
                inj = (scan_num, success_num, rate, path)
                self._sqlite_cursor.execute("update " + self._scriptType + " set SCAN_NUM = ?, SUCCESS_NUM = ?, RATE = ? where PATH = ?;", inj)
                self._sqlite_conn.commit()
        finally:
            lock.release()

if __name__ == "__main__":
    dd = DictDatabase("common")
    print dd.nums()
    for line in dd.getPaths():
        print str(line[0])
        dd.update(str(line[0]), False)
