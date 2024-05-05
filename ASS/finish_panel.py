# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import sys
import urllib
import wx

from ASS import BasePanel

class FinishPanel(BasePanel):
	def __init__(self, parent):
		super(FinishPanel, self).__init__(parent, "Finishing Up")
		self.setup_ui()

	def setup_ui(self):
		# Hide or disable the cancel button as it's not needed on the final screen
		self.cancel_button.Hide()
		self.cancel_button.Enable(False)
		
		# Instruction text indicating completion
		completion_text = wx.TextCtrl(self, value="Setup has completed successfully!", style=wx.TE_READONLY | wx.TE_MULTILINE)
		completion_text.SetFocus()
		self.main_sizer.Add(completion_text, 0, wx.ALL | wx.CENTER, 10)

		# Optional shortcuts
		self.setup_shortcuts()

		# Finish button to close the application
		finish_button = wx.Button(self, label="&Finish")
		finish_button.Bind(wx.EVT_BUTTON, self.on_finish)
		self.nav_sizer.Add(finish_button, 0, wx.ALL | wx.CENTER, 5)
		
		self.Layout()

	def setup_shortcuts(self):
		if sys.platform != "win32": return
		# Create checkboxes for each optional shortcut
		self.desktop_shortcut = wx.CheckBox(self, label="Create &Desktop Shortcut for Mods Folder")
		self.docs_shortcut = wx.CheckBox(self, label="Create Shortcut for D&ocumentation")
		self.wiki_shortcut = wx.CheckBox(self, label="Create Shortcut for &Wiki")

		# Add checkboxes to the main sizer
		self.main_sizer.Add(self.desktop_shortcut, 0, wx.ALL | wx.EXPAND, 5)
		self.main_sizer.Add(self.docs_shortcut, 0, wx.ALL | wx.EXPAND, 5)
		self.main_sizer.Add(self.wiki_shortcut, 0, wx.ALL | wx.EXPAND, 5)

	def on_finish(self, event):
		# Perform any cleanup or final actions before closing
		# Check if any shortcuts were requested and create them
		if self.desktop_shortcut.IsChecked():
			self.create_shortcut("Mods Folder")
		if self.docs_shortcut.IsChecked():
			self.create_shortcut("Documentation")
		if self.wiki_shortcut.IsChecked():
			self.create_shortcut("Wiki")

		self.GetParent().Close() 

	def create_shortcut(self, target):
		if sys.platform == 'win32':
			import win32com.client
			desktop = win32com.client.Dispatch("WScript.Shell").SpecialFolders("Desktop")
			if target == "Mods Folder":
				self._create_shortcut_win32(os.path.join(desktop, "Stardew Valley Mods"), os.path.join(self.GetParent().installation_path, "Mods"), description="Stardew Valley Mods Directory")
			elif target == "Documentation":
				self._create_shortcut_win32(os.path.join(desktop, "Stardew Access Documentation"), os.path.join(self.GetParent().installation_path, "Mods", "stardew-access", "docs", "README.html"), is_url=True, description="Stardew Access Documentation")
			elif target == "Wiki":
				self._create_shortcut_win32(os.path.join(desktop, "Stardew Valley Wiki"), "https://stardewvalleywiki.com/Stardew_Valley_Wiki", is_url=True, description="Stardew Valley Wiki")

	def _create_shortcut_win32(self, path, target, is_url=False, arguments='', start_in='', icon='', description=''):
		import win32com.client
		shell = win32com.client.Dispatch('WScript.Shell')
		path += '.url' if is_url else '.lnk'
		if os.path.exists(path):
			os.remove(path)
		shortcut = shell.CreateShortcut(path)
		
		if is_url:
			if '://' not in target and os.path.exists(target):
				target = target.replace('\\', '/').replace(' ', '%20')
				target = f'file:///{target}'
			shortcut.TargetPath = target  # URL
		else:
			shortcut.TargetPath = target  # File path to executable, document, or directory
			shortcut.Arguments = arguments
			shortcut.WorkingDirectory = start_in if start_in else os.path.dirname(target)
			shortcut.Description = description

		shortcut.Save()
