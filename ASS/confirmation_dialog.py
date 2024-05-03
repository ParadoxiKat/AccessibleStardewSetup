# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import wx

class ConfirmationDialog(wx.Dialog):
    def __init__(self, parent, title, message):
        super(ConfirmationDialog, self).__init__(parent, title=title, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.SetSize((400, 200))
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Message text
        text = wx.StaticText(self, label=message)
        sizer.Add(text, 0, wx.ALL | wx.CENTER, 10)

        # Yes/No buttons
        yes_btn = wx.Button(self, id=wx.ID_YES, label="&Yes")
        no_btn = wx.Button(self, id=wx.ID_NO, label="&No")
        yes_btn.Bind(wx.EVT_BUTTON, self.on_yes)
        no_btn.Bind(wx.EVT_BUTTON, self.on_no)

        btn_sizer = wx.StdDialogButtonSizer()
        btn_sizer.AddButton(yes_btn)
        btn_sizer.AddButton(no_btn)
        btn_sizer.Realize()

        sizer.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer)
        no_btn.SetFocus()

        # Bind a hook to all char events
        self.Bind(wx.EVT_CHAR_HOOK, self.on_char_hook)

    def on_yes(self, event):
        self.EndModal(wx.ID_YES)

    def on_no(self, event):
        self.EndModal(wx.ID_NO)

    def on_char_hook(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_NO)
        else:
            event.Skip()  # Ensure other key events are not blocked
