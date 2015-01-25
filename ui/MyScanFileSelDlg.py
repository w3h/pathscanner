#!/usr/bin/env python
#coding=utf8
import os
import wx
from core.shellpara import ShellPara

class MyScanFileSelDlg(wx.MultiChoiceDialog):
    def __init__(self, parent):
        self.scanfile = []
        self.GetInitList()
        super(MyScanFileSelDlg, self).__init__(parent, "Select File: ", "Select Scan File", self.scanfile)
        self.SetClientSizeWH(300, 250)
        self.Center()
        self.InitSel()

    def GetInitList(self):
        dir = ".\\data"
        self.scanfile = []
        for root, dirs, files in os.walk(dir):
            for name in files:
                tp = os.path.splitext(name)[1]
                if tp in [".txt", ".csv"]:
                    self.scanfile.append(os.path.join(root, name))

    def InitSel(self):
        sp = ShellPara()
        sf = sp.GetScanFile()
        if not sf:
            return

        sellist = []
        for tt in sf:
            if not tt in self.scanfile:
                continue

            index = self.scanfile.index(tt)
            if index < 0:
                continue
            sellist.append(index)

        self.SetSelections(sellist)

    def SaveSel(self):
        ressel = [self.scanfile[i] for i in self.GetSelections()]
        sp = ShellPara()
        sp.SetScanFile(ressel)

    def ClearSel(self):
        sp = ShellPara()
        sp.SetScanFile([])