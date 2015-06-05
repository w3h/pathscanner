#!/usr/bin/env python
#coding=utf8

import wx
import os
import wx.aui
from ui.MainThread import MainThread
from core.shellpara import ShellPara
import core.common as common
import wx.lib.agw.aui as aui
from ui.MyScanFileSelDlg import MyScanFileSelDlg
import datetime

VERSION = "V1.0"

[       wxID_FRAME1, 
        wxID_FRAME1PANEL1, 
        wxID_SELTARGET, 
        wxID_STOP, wxID_START, 
        wxID_TARGET, 
        wxID_TB_ASP, 
        wxID_TB_JSP, 
        wxID_TB_ASPX, 
        wxID_TB_PHP, 
        wxID_TB_CMS, 
        wxID_TB_WWW, 
        wxID_TB_AUTO,
] = [wx.NewId() for _init_ctrls in range(13)]

SCRIPT_TYPE_BT = {  wxID_TB_ASP : "asp", 
                    wxID_TB_ASPX : "aspx", 
                    wxID_TB_JSP : "jsp", 
                    wxID_TB_PHP : "php", 
                    wxID_TB_WWW : "scanfile",
                    wxID_TB_AUTO : "auto" }

def create(parent):
    return MainFrame(parent)

class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, ("PathScanner %s By W.HHH" % VERSION), size = (800, 600),
                          style = wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)
        # tell FrameManager to manage this frame        
        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        self.currnum = 0
        self.starttime = 0
        self.fileTarget = ""
        self.scanTarget = ""
        self.scanTargetCurrpos = 0

        self.InitUI()
        self.BindEvents()
        self.mainthread = MainThread(self)
        self.count = 0
        self.InitDefaultCmdPara()
        self.Center()

    def InitUI(self):
        self.InitMenuBar()
        self.InitStatusBar()
        self.InitToolBar()

    def InitToolBar(self):
        self.tb2 = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize, agwStyle=aui.AUI_TB_OVERFLOW | aui.AUI_TB_TEXT | aui.AUI_TB_HORZ_TEXT)
        self.tb2.SetToolBitmapSize(wx.Size(16, 16))
        tb2_bmp1 = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16))
        self.tb2.AddSimpleTool(wxID_TB_ASP, "ASP", tb2_bmp1, "ASP", aui.ITEM_CHECK)
        self.tb2.AddSimpleTool(wxID_TB_ASPX, "ASPX", tb2_bmp1, "ASPX", aui.ITEM_CHECK)
        self.tb2.AddSimpleTool(wxID_TB_PHP, "PHP", tb2_bmp1, "PHP", aui.ITEM_CHECK)
        self.tb2.AddSimpleTool(wxID_TB_JSP, "JSP", tb2_bmp1, "JSP", aui.ITEM_CHECK)
        self.tb2.AddSimpleTool(wxID_TB_AUTO, "AUTO", tb2_bmp1, "Automatically identify the type of script", aui.ITEM_CHECK)
        self.tb2.AddSimpleTool(wxID_TB_WWW, "...", tb2_bmp1, "Select the scan file", aui.ITEM_CHECK)
        self.tb2.AddSeparator()

        self.threadsc = wx.SpinCtrl(self.tb2, -1, "", (-1, -1), (50, -1))
        self.threadsc.SetRange(1, 100)
        self.threadsc.SetValue(10)
        self.timeoutsc = wx.SpinCtrl(self.tb2, -1, "", (-1, -1), (50, -1))
        self.timeoutsc.SetRange(1, 100)
        self.timeoutsc.SetValue(10)
        self.delaysc = wx.SpinCtrl(self.tb2, -1, "", (-1, -1), (50, -1))
        self.delaysc.SetRange(1, 600)
        self.delaysc.SetValue(5)

        self.tb2.AddControl(wx.StaticText(self.tb2, -1, label=' Threads', name='Thread Number'))
        self.tb2.AddControl(self.threadsc)
        self.tb2.AddControl(wx.StaticText(self.tb2, -1, label=' Timeout', name='Socket Timeout'))
        self.tb2.AddControl(self.timeoutsc)
        self.tb2.AddControl(wx.StaticText(self.tb2, -1, label=' Delay', name='Thread Delay'))
        self.tb2.AddControl(self.delaysc)
        self.tb2.Realize()

        tb4 = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize, agwStyle=aui.AUI_TB_OVERFLOW | aui.AUI_TB_TEXT | aui.AUI_TB_HORZ_TEXT)
        tb4.SetToolBitmapSize(wx.Size(16,16))
        tb4_bmp1 = wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16))
        txt = wx.StaticText(tb4, -1, label='Target ', name='Target')
        tb4.AddControl(txt)

        self.target = wx.ComboBox(tb4, wxID_TARGET, name='Target', choices=['http://www.geostar.com.cn'], size=(500,-1))
        tb4.AddControl(self.target)
        self.seltarget = wx.Button(tb4, wxID_SELTARGET, label='...', name='SelTarget', style=wx.BU_EXACTFIT)
        tb4.AddControl(self.seltarget)
        self.start = wx.Button(tb4, wxID_START, label='Start', name='Start', style=wx.BU_EXACTFIT)
        tb4.AddControl(self.start)
        self.stop = wx.Button(tb4, wxID_STOP, label='Stop', name='Stop', style=wx.BU_EXACTFIT)
        tb4.AddControl(self.stop)
        self.start.Enable()
        self.stop.Disable()
        tb4.Realize()
                      
        self.LogText = self.CreateTextCtrl()
        self.LogPane = wx.aui.AuiPaneInfo()
        self.LogPane.Name("log").Caption("Log").Bottom().CloseButton(False).MaximizeButton(True)
        self._mgr.AddPane(self.LogText, self.LogPane)

        self.tree = self.CreateTreeCtrl()
        self.TreePane = wx.aui.AuiPaneInfo()
        self.TreePane.Name("result").Caption("Result").Center().CloseButton(False).MaximizeButton(True)
        self._mgr.AddPane(self.tree, self.TreePane)                                      
                      
        # add the toolbars to the manager
        self._mgr.AddPane(self.tb2, wx.aui.AuiPaneInfo().
                          Name("tb2").Caption("Toolbar 2").
                          ToolbarPane().Top().Row(1).
                          LeftDockable(False).RightDockable(False))

        self._mgr.AddPane(tb4, wx.aui.AuiPaneInfo().
                          Name("tb4").Caption("Sample Bookmark Toolbar").
                          ToolbarPane().Top().Row(2).
                          LeftDockable(False).RightDockable(False))

        self._mgr.Update()


    def InitMenuBar(self):
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, "&Widget Inspector\tF6", "Show the wxPython Widget Inspection Tool")
        item = menu.Append(wx.ID_EXIT, "E&xit\tCtrl-Q", "Exit demo")
        self.Bind(wx.EVT_MENU, self.OnExitApp, item)
        menuBar.Append(menu, "&File")   

        menuSetting = wx.Menu()
        item = menuSetting.Append(-1, "&Scan File", "Select scan file")
        self.Bind(wx.EVT_MENU, self.OnSelScanFile, item)
        menuBar.Append(menuSetting, "&Setting")  

        menuHis = wx.Menu()
        menuBar.Append(menuHis, "&Histary") 

        self.SetMenuBar(menuBar)

    def InitStatusBar(self):
        self.statusbar = self.CreateStatusBar(3, wx.ST_SIZEGRIP)
        self.statusbar.SetStatusWidths([-2, -1, -1])
        self.statusbar.SetStatusText(u"Init Status Bar", 0)
        self.statusbar.SetStatusText(u"", 1)
        self.statusbar.SetStatusText(u"", 2)

    def InitDefaultCmdPara(self):
        self.cmdpara = ShellPara()
        print self.cmdpara.script
        for ss in self.cmdpara.script: 
            for (k,v) in  SCRIPT_TYPE_BT.items(): 
                if ss == v:
                    self.tb2.FindTool(k).SetState(aui.AUI_BUTTON_STATE_CHECKED)

        self.UpdateScriptType()
        self.timeoutsc.SetValue(self.cmdpara.GetTimeOut())
        self.threadsc.SetValue(self.cmdpara.GetThreadNum())
        self.delaysc.SetValue(self.cmdpara.GetDelayTime())

    def CreateTextCtrl(self):
        text = ("")
        textctrl = wx.TextCtrl(self,-1, text, wx.Point(0, 0), wx.Size(150, 90), wx.NO_BORDER | wx.TE_MULTILINE)
        return textctrl

    def CreateTreeCtrl(self):
        import MyTreeListCtrl
        tree = MyTreeListCtrl.MyTreeListCtrl(self)
        tree.Init()
        return tree

    def BindEvents(self):
        self.Bind(wx.EVT_BUTTON, self.OnSelTarget, id = self.seltarget.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnStart, id = self.start.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnStop, id = self.stop.GetId())

        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=wxID_TB_ASP)
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=wxID_TB_ASPX)
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=wxID_TB_JSP)
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=wxID_TB_PHP)
        self.Bind(wx.EVT_TOOL, self.OnToolWWWClick, id=wxID_TB_WWW)
        self.Bind(wx.EVT_TOOL, self.OnToolAutoClick, id=wxID_TB_AUTO)

        self.Bind(wx.EVT_SPINCTRL, self.OnSCChange, self.threadsc)
        self.Bind(wx.EVT_TEXT, self.OnSCChange, self.threadsc)
        self.Bind(wx.EVT_SPINCTRL, self.OnSCChange, self.timeoutsc)
        self.Bind(wx.EVT_TEXT, self.OnSCChange, self.timeoutsc)
        self.Bind(wx.EVT_SPINCTRL, self.OnSCChange, self.delaysc)
        self.Bind(wx.EVT_TEXT, self.OnSCChange, self.delaysc)

    def OnSelTarget(self, evt):
        sel = wx.FileSelector("Choose a file",  os.getcwd())
        self.target.SetLabelText(str(sel)) 
        self.fileTarget = str(sel)

    def OnStartByTarget(self, tt):
        if not tt: return
        self.GetCmdPara(tt)
        if not self.CheckCmdPara(): return

        self.start.Disable()
        self.stop.Enable()
        self.threadsc.Disable()
        self.AddTargetList()
        self.cmdpara.GetScanNum()
        self.currnum = 0

        self.ThreadLogMessage("start scan...\n")
        self.ThreadLogMessage(self.cmdpara.GetPara())
        self.mainthread.startscan()

    def GetFirstTarget(self):
        tmp = self.target.GetValue()
        if not os.path.isfile(tmp):
            return tmp
        else:
            self.fileTarget = tmp
            self.scanTargetCurrpos = 0

        with open(self.fileTarget) as fp:
            lines = fp.readlines()
            return lines[0].strip()

    def GetNextTarget(self):
        if not os.path.isfile(self.fileTarget):
            return None

        with open(self.fileTarget) as fp:
            lines = fp.readlines()
            self.scanTargetCurrpos = self.scanTargetCurrpos + 1
            if self.scanTargetCurrpos >= len(lines):
                return None

            return lines[self.scanTargetCurrpos].strip()

    def OnStart(self, evt):
        self.ClearResult()
        ft = self.GetFirstTarget()
        if not ft:
            wx.MessageBox(u"扫描目标对象不能为空！", u"错误")
            return

        # init log file
        common.InitLog(ft)
        self.OnStartByTarget(ft)

    def OnStop(self, evt):
        self.stop.Disable()
        self.mainthread.stopscan()

    def OnOpenStartBt(self, evt):
        self.start.Enable()
        self.stop.Disable()

    def OnExitApp(self, evt):
        self.mainthread.stopscan()
        self.mainthread.stop()
        self.mainthread.join()
        self.Close(True)

    def OnSelScanFile(self, event):
        checkstate = (self.tb2.FindTool(wxID_TB_WWW).GetState() & aui.AUI_BUTTON_STATE_CHECKED)
        if not checkstate:
            wx.MessageBox(u"请先选择文件扫描模式！", u"警告")
            return

        dlg = MyScanFileSelDlg(self)
        if dlg.ShowModal() == wx.ID_OK:
            dlg.SaveSel()
        dlg.Destroy()

    def OnToolWWWClick(self, event):
        evid = event.GetId()
        tb = event.GetEventObject()
        checkstate = (tb.FindTool(evid).GetState() & aui.AUI_BUTTON_STATE_CHECKED)

        # file select
        if checkstate:
            for (k,v) in SCRIPT_TYPE_BT.items():
                if k == wxID_TB_WWW: continue
                tb.FindTool(k).SetState(aui.AUI_BUTTON_STATE_NORMAL)
            tb.RefreshOverflowState()

            dlg = MyScanFileSelDlg(self)
            if dlg.ShowModal() == wx.ID_OK:
                dlg.SaveSel()
            dlg.Destroy()
        else:
            self.cmdpara.SetScanFile("")

        self.UpdateScriptType()
        return

    def OnToolAutoClick(self, event):
        evid = event.GetId()
        tb = event.GetEventObject()
        checkstate = (tb.FindTool(evid).GetState() & aui.AUI_BUTTON_STATE_CHECKED)
        if checkstate:
            for (k,v) in SCRIPT_TYPE_BT.items():
                if k == wxID_TB_AUTO: continue
                tb.FindTool(k).SetState(aui.AUI_BUTTON_STATE_NORMAL)

        dlg = MyScanFileSelDlg(self)
        dlg.ClearSel()

    def OnToolClick(self, event):
        tb = event.GetEventObject()
        tb.FindTool(wxID_TB_AUTO).SetState(aui.AUI_BUTTON_STATE_NORMAL)
        tb.FindTool(wxID_TB_WWW).SetState(aui.AUI_BUTTON_STATE_NORMAL)

        dlg = MyScanFileSelDlg(self)
        dlg.ClearSel()

        tb.RefreshOverflowState()
        self.UpdateScriptType()

    def OnSCChange(self, evt):
        tb = evt.GetEventObject()
        if tb == self.timeoutsc:
            setcallfun = self.cmdpara.SetTimeOut
        elif  tb == self.threadsc:
            setcallfun = self.cmdpara.SetThreadNum
        elif  tb == self.delaysc:
            setcallfun = self.cmdpara.SetDelayTime
        else:
            return

        tmp = tb.GetValue()
        tb.SetValue(tmp)
        setcallfun(tmp)

    def AddTargetList(self):
        for t in self.target.Items:
            if t == self.cmdpara.target:
                return

        self.target.Append(self.cmdpara.target)

    def UpdateScriptType(self):
        stype = []
        for (k,v) in SCRIPT_TYPE_BT.items(): 
            checkstate = (self.tb2.FindTool(k).GetState() & aui.AUI_BUTTON_STATE_CHECKED)
            if checkstate: stype.append(v)

        self.cmdpara = ShellPara()
        self.cmdpara.SetScriptType(stype)

    def GetCmdPara(self, tt):
        self.cmdpara.SetTarget(tt)
        self.GetScriptType()

    def CheckCmdPara(self):
        if not self.cmdpara.target:
            wx.MessageBox(u"请选择扫描对象！", u"警告")
            return False

        stype = []
        for (k,v) in SCRIPT_TYPE_BT.items():
            checkstate = (self.tb2.FindTool(k).GetState() & aui.AUI_BUTTON_STATE_CHECKED)
            if checkstate: stype.append(v)

        if not stype:
            wx.MessageBox(u"请选择扫描类型！", u"警告")
            return False

        if wxID_TB_WWW in stype:
            if not self.cmdpara.scanfile:
                wx.MessageBox(u"请选择扫描文件！", u"警告")
                return False
            else:
                return True

        script = self.cmdpara.GetScriptType()
        if "auto" in script:
            script = []
            tmp = common.GetScriptType(self.cmdpara.target)
            if tmp: script = [tmp,]

        if not script:
            wx.MessageBox(u"无法识别脚本类型，请指定！", u"警告")
            return False

        self.cmdpara.SetDBScriptType(script)
        return True

    def GetScriptType(self):
        stype = []
        for (k,v) in  SCRIPT_TYPE_BT.items(): 
            checkstate = self.tb2.FindTool(k).GetState() & aui.AUI_BUTTON_STATE_CHECKED
            if checkstate:
                stype.append(v)

        self.cmdpara.SetScriptType(stype)

    def ClearResult(self):
        # clear tree
        self.tree.DeleteAll()
        # clear logtext
        self.LogText.Value = ""
        # clear para
        self.cmdpara.Init()

    def ThreadLogMessage(self, msg):
        msg = "[%s] %s" % (common.GetCurrTime(), msg)
        self.LogText.AppendText(msg)

    def ThreadScanMessage(self, msg):
        self.tree.AddNode(msg)
        urlpath = msg[0] + msg[1]
        info = msg[2]
        common.WriteLog(urlpath, info)

    def ThreadStatusMessage(self, msg):
        index = int(msg[1])
        if index == 0:
            self.statusbar.SetStatusText(str(msg[0]), int(msg[1]))
            return

        # index = 1,2
        self.FlushBarTime()

    def FlushBarTime(self, fin = False):
        sn = self.cmdpara.GetScanNum()
        if sn == 0: return
        self.currnum += 1
        progress = 100 - (((sn - self.currnum) * 100 ) / sn)
        info = "Scan Progress: " + str(progress)+ "%"
        if fin and (progress != 100):
            self.statusbar.SetStatusText("", 1)
        else:
            self.statusbar.SetStatusText(info, 1)

        currtime = datetime.datetime.now()
        tm = ((currtime - self.starttime) / self.currnum) * (sn - self.currnum)
        if tm == 0 or fin:
            resttime = currtime - self.starttime
            info = "Running Time: " + str(resttime)
            self.statusbar.SetStatusText(info, 2)
        else:
            info = "Remaining Time: %s " % tm
            self.statusbar.SetStatusText(info, 2)

    def ThreadFinishMessage(self):
        self.ThreadLogMessage("Finished ...")
        self.ThreadStatusMessage(["Finished ...", 0])

        self.threadsc.Enable()
        self.OnOpenStartBt("Enable")
        self.threadsc.Enable()

        self.FlushBarTime(True)

        # scan next target
        nt = self.GetNextTarget()
        if nt: self.OnStartByTarget(nt)

