import wx
import traceback
import sys

class DumpLogDialog(wx.Dialog):
	def __init__(self, parent, id, title, message=None):
		super(DumpLogDialog, self).__init__(parent, id, title, size=(400, 300))
		
		# Layout components
		vbox = wx.BoxSizer(wx.VERTICAL)
		
		# Message and traceback area
		error_message = message if message else "An unexpected error occurred:"
		self.error_info = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
		if message:
			self.error_info.AppendText(message + "\n\n")
		self.error_info.AppendText(self.get_formatted_traceback())
		
		# Copy to clipboard button
		copy_btn = wx.Button(self, label="&Copy ASS dump to clipboard")
		copy_btn.Bind(wx.EVT_BUTTON, self.on_copy_to_clipboard)
		
		# Close button
		exit_btn = wx.Button(self, label="&Exit")
		exit_btn.Bind(wx.EVT_BUTTON, self.on_exit)
		
		# Add components to vbox
		vbox.Add(self.error_info, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(copy_btn)
		hbox.Add(exit_btn, flag=wx.LEFT, border=10)
		vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
		
		self.SetSizer(vbox)
		
	def get_formatted_traceback(self):
		exc_type, exc_value, exc_traceback = sys.exc_info()
		tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
		return ''.join(tb_lines)

	def on_copy_to_clipboard(self, event):
		if wx.TheClipboard.Open():
			wx.TheClipboard.SetData(wx.TextDataObject(self.error_info.GetValue()))
			wx.TheClipboard.Close()
			wx.MessageBox("Traceback information copied to clipboard.", "Copied", wx.OK | wx.ICON_INFORMATION)

	def on_exit(self, event):
		self.Destroy()
		wx.CallAfter(self.GetParent().Close)
