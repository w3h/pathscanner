#!/usr/bin/env python
#coding=utf8
import sqlite3
import sys

reload(sys)
sys.setdefaultencoding('utf8')


databasename = "./dit.s3db"
table = ['asp', 'aspx', 'jsp', 'php', 'common']
create_table_string = '''CREATE TABLE [%s] (
[ID] INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
[PATH] TEXT  NULL,
[TYPE] TEXT  NULL,
[SCAN_NUM] INTEGER DEFAULT '0' NULL,
[SUCCESS_NUM] INTEGER DEFAULT '0' NULL,
[RATE] FLOAT DEFAULT '0' NULL
);'''

def main():
    cx = sqlite3.connect(databasename)
    cur = cx.cursor()

    try:
        for info in table:
            num = 0
            cur.execute("PRAGMA table_info(%s)" % info)
            if not cur.fetchall():
                cur.execute(create_table_string % info)
            else:
                st = "select ID  from '" + info + "'" + "order by ID DESC"
                cur.execute(st)
                num = cur.fetchall()
                num = int(num[0][0])

            for line in open(info + ".txt", 'rb'):
                line = line.strip();
                #print line
                if not line:
                    continue

                cur.execute("select *  from '" + info + "' where PATH = ?", (line.decode('gbk'),))
                if len(cur.fetchall()) > 0:
                    continue

                print line
                num += 1
                cur.execute("insert into '" + info + "' values (?,?,?,?,?,?)", (num, line.decode('gbk'),"",0,0,0))
    except Exception,e:
        print e
    finally:
        cx.commit()
        cur.close()

if __name__ == "__main__":
    main()
