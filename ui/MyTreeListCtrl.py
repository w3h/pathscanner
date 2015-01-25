#!/usr/bin/env python
#coding=utf8
import wx
#import  images
import  wx.gizmos   as  gizmos

class MyTreeListCtrl(gizmos.TreeListCtrl):
    def __init__(self, parent):
        gizmos.TreeListCtrl.__init__(self, parent, -1, style = wx.TR_DEFAULT_STYLE | wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_HIDE_ROOT)
        self.parent = parent

    def Init(self):
        # create some columns
        self.AddColumn("Path")
        self.AddColumn("Code")
        self.AddColumn("Other")
        self.SetMainColumn(0) # the one with the tree in it...
        self.SetColumnWidth(0, 500)

        imglist = wx.ImageList(16, 16, True, 2)
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16,16)))
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16,16)))
        #tree.AssignImageList(imglist)
        self.SetImageList(imglist)

        self.root = self.AddRoot("The Result")  
        self.SetItemText(self.root, "", 1)
        self.SetItemText(self.root, "", 2)        
        self.Expand(self.root)

        self.BindEvents()

    def DeleteAll(self):
        item, cookie = self.GetFirstChild(self.root)
        while item:
            self.DeleteChildren(item)
            self.Delete(item)
            item, cookie = self.GetNextChild(self.root, cookie)

    def BindEvents(self):
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate)

    def AddNode(self, node):
        target = node[0]
        path = node[1]
        info = node[2]
        parent = None        
        flag = False

        item, cookie = self.GetFirstChild(self.root)
        while item:
            if self.GetItemText(item) == target:
                parent = item
                break
            item, cookie = self.GetNextChild(self.root, cookie)

        if not parent:
            parent = self.AppendItem(self.root, target)
            self.SetItemText(parent, "", 1)
            self.SetItemText(parent, "", 2)

        last = self.AppendItem(parent, path)
        self.SetItemText(last, info, 1)
        self.SetItemText(last, "", 2)
        self.Expand(parent)   

    def OnActivate(self, event):
        path = self.GetItemText(event.GetItem())
        parent = self.GetItemParent(event.GetItem())
        target = self.GetItemText(parent)
        if parent != self.root:
            import webbrowser  
            webbrowser.open(target+path)

        event.Skip()        
