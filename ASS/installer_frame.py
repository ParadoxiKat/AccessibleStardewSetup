# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import os
import sys
import wx

from ASS import ConfirmationDialog, WelcomePanel
from ASS.exceptions import UnsupportedOSError

INSTALLER_FILENAME = "data/installer.json"

class InstallerFrame(wx.Frame):
	def __init__(self, *args, **kwargs):
		app_dir = kwargs.pop('app_dir', None)
		super(InstallerFrame, self).__init__(*args, **kwargs)
		if app_dir is None:
			raise TypeError("No app was supplied")
		elif not os.path.exists(app_dir):
			raise FileNotFoundError(f"No such directory {os.path.abspath(app_dir)}")
		elif not os.path.isdir(app_dir):
			raise NotADirectoryError(f"{os.path.abspath(app_dir)} exists but is not a directory.")
		self.app_dir = app_dir
		if not os.path.exists(INSTALLER_FILENAME):
			raise FileNotFoundError(f"Could not load {os.path.abspath(INSTALLER_FILENAME)}")
		self.token = os.environ.get('ASS_GITHUB_TOKEN')
		with open(INSTALLER_FILENAME, encoding="utf-8") as f:
			installer_config = json.load(f)
			self.download_info = installer_config['download_info']
			self.sdv_path_info = installer_config['sdv_path_info']
		self.installation_path = None
		self.setup_ui()
		self.SetSize(800, 600)
		self.Center()

		# Setup global accelerator for the Escape key
		self.setup_accelerators()

		self.post_init_ui()

	def setup_ui(self):
		# Define colors for dark mode
		self.SetBackgroundColour('#333333')  # Dark gray background
		self.SetForegroundColour('#E0E0E0')  # Light gray text
		self.panel = None
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.sizer)
		self.CreateStatusBar()
		self.GetStatusBar().SetBackgroundColour('#222222')
		self.GetStatusBar().SetForegroundColour('#FFFFFF')

	def post_init_ui(self):
		# This method will be called after the UI setup is complete
		self.switch_panel(WelcomePanel)


	def switch_panel(self, new_panel_class, *args):
		"""Switches the current panel to a new one specified by new_panel_class."""
		if self.panel:  # Remove the current panel if it exists
			self.panel.Destroy()
		self.panel = new_panel_class(self, *args)  # Create an instance of the new panel
		self.sizer.Add(self.panel, 1, wx.EXPAND)
		self.Layout()  # Re-layout to accommodate the new panel
		self.Fit()  # Fit the frame snugly around the contents
		self.update_title(self.panel.title)
		self.apply_dark_theme_to_panel(self.panel)

	def update_title(self, title_suffix):
		title = self.GetTitle().split(" - ")[0]
		if title_suffix is not None:
			title = f"{title} - {title_suffix}"
		self.SetTitle(title)

	def apply_dark_theme_to_panel(self, panel):
		"""Applies dark theme colors to a panel and its children recursively."""
		panel.SetBackgroundColour('#333333')
		panel.SetForegroundColour('#E0E0E0')
		for child in panel.GetChildren():
			if isinstance(child, wx.Panel):
				self.apply_dark_theme_to_panel(child)
			elif isinstance(child, (wx.StaticText, wx.Button, wx.TextCtrl)):
				child.SetBackgroundColour('#333333')
				child.SetForegroundColour('#E0E0E0')

	@property
	def platform(self):
		# Acts as a string property returning the appropriate OS name for the SMAPI zip
		if sys.platform == 'win32':
			return 'windows'
		elif sys.platform == linux:
			return 'linux'
		elif sys.platform == 'darwin':
			return 'macOS'
		else:
			raise UnsupportedOSError('Smapi is not supported on {sys.platform}')

	@property
	def is_steam_install(self):
		return self.installation_path is not None and 'steamapps' in self.installation_path.lower()

	def setup_accelerators(self):
		# ID for the cancel operation
		self.ID_CANCEL = wx.NewIdRef()
		self.Bind(wx.EVT_MENU, self.on_cancel, id=self.ID_CANCEL)

		# Create an accelerator table
		accel_tbl = wx.AcceleratorTable([
			(wx.ACCEL_NORMAL, wx.WXK_ESCAPE, self.ID_CANCEL)
		])
		self.SetAcceleratorTable(accel_tbl)

	def on_cancel(self, event):
		# Show the custom confirmation dialog
		dialog = ConfirmationDialog(self, "Confirm Cancellation", "Are you sure you want to cancel the installation?")
		if dialog.ShowModal() == wx.ID_YES:
			self.Close()
		dialog.Destroy()

	def dump_log(self, message=None):
		from ASS.dump_log_dialog import DumpLogDialog
		dlg = DumpLogDialog(self, wx.ID_ANY, "Error!!!", message=message)
		dlg.ShowModal()
		dlg.Destroy()