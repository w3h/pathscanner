#!/usr/bin/env python
#coding=utf-8

import wx
import ui.MainFrame
import sys

class BoaApp(wx.App):
    def __init__(self,redirect,filename=None):  
        print 'App __init__'  
        wx.App.__init__(self,redirect,filename);

    def OnInit(self):
        self.main = ui.MainFrame.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        sys.exit = None
        return True

def main():
    application = BoaApp(redirect = False)
    application.MainLoop()
    
if __name__ == '__main__':
    main()
