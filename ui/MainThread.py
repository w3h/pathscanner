#!/usr/bin/env python
#coding=utf8

import wx
import threading
import core.common as common
from Queue import Queue
import time
import datetime

class MainThread(threading.Thread):
    def __init__(self, window):
        threading.Thread.__init__(self)
        self.window = window
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        self.messageDelay = 0.1
        self.timeToScan = threading.Event()
        self.timeToScan.clear()
        self.threads = []
        self.tasks = Queue()
        self.count = 0
        self.start()

    def SendStatusMsg(self, msg):
        wx.CallAfter(self.window.ThreadStatusMessage, [msg, 0])

    def stop(self):
        self.timeToQuit.set()

    def stopscan(self):
        self.timeToScan.clear()
        self.stopsub()
        self.SendStatusMsg("Stop Scan ...")

    def startscan(self):
        self.SendStatusMsg("Start Scan ...")
        self.timeToScan.set()

    def run(self):
        while True:
            if self.timeToQuit.isSet():
                break

            self.timeToQuit.wait(self.messageDelay)
            if not self.timeToScan.isSet():
                continue

            self.window.starttime = datetime.datetime.now()
            for i in xrange(self.window.cmdpara.thread):
                thread = WorkerThread(self)
                self.threads.append(thread)

            self.SendStatusMsg("Init Scan List ..")

            for t in self.window.cmdpara.GetDBScriptType():
                common.AddTasks(self.window.cmdpara.target, t, self.tasks)

            for t in self.window.cmdpara.GetScanFile():
                common.AddTasksFromPath(self.window.cmdpara.target, t, self.tasks)

            self.SendStatusMsg("Scanning ...")

            for t in self.threads:
                try:
                    t.start()
                except:
                    pass

            # wait thread
            for t in self.threads:
                t.join()

            self.stopscan()
            time.sleep(2)
            self.clearqueue()

    def stopsub(self):
        for t in self.threads:
            t.stop()

        for t in self.threads:
            self.threads.remove(t)

    def clearqueue(self):
        while not self.tasks.empty():
            self.tasks.get()
        wx.CallAfter(self.window.ThreadFinishMessage)

class WorkerThread(threading.Thread):
    def __init__(self, mainthread):
        threading.Thread.__init__(self)
        self.mainthread = mainthread
        self.window = mainthread.window
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        self.messageDelay = 0

    def stop(self):
        self.timeToQuit.set()

    def run(self):
        while True:
            if self.mainthread.tasks.empty():
                break
            qp = self.mainthread.tasks.get()
            if self.timeToQuit.isSet():
                break

            # delay time
            self.messageDelay = self.window.cmdpara.GetDelayTime() * 0.1
            self.timeToQuit.wait(self.messageDelay)

            for i in qp.GetList():
                res = qp.Run(i)
                info = str(qp.GetCode())

                if res:
                    msg = [qp.Target(), i, info]
                    wx.CallAfter(self.window.ThreadScanMessage, msg)

                targer = qp.Target() + i
                msg = "%s %s\n" % (targer, info)
                wx.CallAfter(self.window.ThreadLogMessage, msg)
                wx.CallAfter(self.window.ThreadStatusMessage, ["", 1])
