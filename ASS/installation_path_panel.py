# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import wx

from ASS import BasePanel

class InstallationPathPanel(BasePanel):
	def __init__(self, parent):
		super(InstallationPathPanel, self).__init__(parent, "Choose Installation Path")
		self._executable_name = None
		self.setup_ui()

	def setup_ui(self):
		instruction_text = wx.StaticText(self, label="Please choose installation path:")
		self.path_text_ctrl = wx.TextCtrl(self, value="")
		self.path_text_ctrl.SetFocus()
		browse_button = wx.Button(self, label="&Browse")
		browse_button.Bind(wx.EVT_BUTTON, self.on_browse)

		# Check if we can prepopulate the path
		self.path_text_ctrl.SetValue(self.default_install_path)

		self.path_text_ctrl.Bind(wx.EVT_TEXT, self.on_path_text_change)  # Bind text change event

		# Layout
		content_sizer = wx.BoxSizer(wx.HORIZONTAL)
		content_sizer.Add(self.path_text_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
		content_sizer.Add(browse_button, flag=wx.ALL, border=5)

		self.main_sizer.Add(instruction_text, 0, wx.ALL | wx.EXPAND, 5)
		self.main_sizer.Add(content_sizer, 0, wx.EXPAND | wx.ALL, 5)

		# Nav buttons
		self.prev_button = self.add_nav_button("&Previous", self.on_prev)
		self.next_button = self.add_nav_button("&Next", self.on_next)
		self.next_button.Enable(self.is_path_valid(self.path_text_ctrl.GetValue()))

	def on_browse(self, event):
		# Create and show a directory chooser dialog
		with wx.DirDialog(self, "Choose installation directory", style=wx.DD_DEFAULT_STYLE) as dir_dialog:
			if dir_dialog.ShowModal() == wx.ID_OK:
				self.path_text_ctrl.SetValue(dir_dialog.GetPath())
				self.next_button.Enable(True)  # Enable the 'Next' button when a path is selected

	def on_path_text_change(self, event):
		# Enable the 'Next' button only if the text control is not empty
		path = self.path_text_ctrl.GetValue()
		self.next_button.Enable(self.is_path_valid(path))

	@property
	def executable_name(self):
		if self._executable_name is None:
			suffix = '.exe' if self.GetParent().platform == 'windows' else ''
			self._executable_name = f"Stardew Valley{suffix}"
		return self._executable_name

	@property
	def default_install_path(self):
		# Function to find and return a default installation path, if available
		frame = self.GetParent()
		try:
			os_paths = frame.sdv_path_info[frame.platform]
		except KeyError as e:
			raise Exception("Could not load os-specific path data") from e
		for path in os_paths:
			if os.path.exists(path) and os.path.isdir(path) and os.path.isfile(os.path.join(path, self.executable_name)):
				return path
		else:
			return ""

	def is_path_valid(self, path):
		return os.path.isdir(path) and os.path.isfile(os.path.join(path, "Stardew Valley.exe"))

	def on_next(self, event):
		from ASS import ComponentSelectionPanel
		frame = self.GetParent()
		frame.installation_path = self.path_text_ctrl.GetValue().strip()
		wx.CallAfter(frame.switch_panel, ComponentSelectionPanel)  # Switch to the Component selection panel

	def on_prev(self, event):
		from ASS import WelcomePanel
		wx.CallAfter(self.GetParent().switch_panel, WelcomePanel)  # Switch to the installation path panel