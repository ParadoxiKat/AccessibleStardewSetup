# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
import os
import shutil
import sys
import tempfile
import threading
import wx
import zipfile

from ASS import BasePanel, Downloader, Installer
from ASS.events import *

class DownloadAndInstallPanel(BasePanel):
	def __init__(self, parent):
		super(DownloadAndInstallPanel, self).__init__(parent, "Downloading and Installing Components")
		frame = self.GetParent()
		download_info = {k.replace('&', ''):v for k, v in frame.download_info.items()}
		self.downloader = Downloader(download_info, token=frame.token, download_dir=frame.app_dir, panel=self)
		self.installer = Installer(download_info, frame.installation_path, panel=self)
		self.setup_ui()
		self.Bind(EVT_DOWNLOADS_COMPLETE, self.on_downloads_complete)
		self.Bind(EVT_INSTALLATION_COMPLETE, self.on_installation_complete)
		self.Bind(EVT_NOTIFY, self.on_notify)
		self.download()

	def setup_ui(self):
		# Instruction text or label
		instruction_text = wx.StaticText(self, label="Downloading components, please wait...")
		self.main_sizer.Add(instruction_text, 0, wx.ALL | wx.EXPAND, 5)

		# Setup the read-only text box for download progress and messages
		self.output_textbox = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_SIMPLE)
		self.main_sizer.Add(self.output_textbox, 1, wx.EXPAND | wx.ALL, 5)
		self.output_textbox.SetFocus()

	def log_message(self, message):
		"""Utility function to append messages to the output text box."""
		self.output_textbox.AppendText(message + "\n")

	def download(self):
		"""Starts the download process in a thread."""
		threading.Thread(target=self.downloader.download_all, daemon=True).start()

	def install(self):
		with self.installer:
			threading.Thread(target=self.installer.install_all, daemon=True).start()

	def on_downloads_complete(self, event):
		self.install()

	def on_installation_complete(self, event):
		frame = self.GetParent()
		if frame.platform == 'windows' and frame.is_steam_install:
			from ASS import SteamLaunchOptionsPanel
			wx.CallAfter(self.GetParent().switch_panel, SteamLaunchOptionsPanel)
		else:
			from ASS import FinishPanel 
			wx.CallAfter(self.GetParent().switch_panel, FinishPanel)

	def on_notify(self, event):
		"""Update the text box with messages from the download / install process."""
		message = event.GetMessage()
		if message:
			self.log_message(message)

	def on_cancel(self, event):
		"""Stops the download process and potentially cleans up."""
		dialog_result = self.show_cancel_confirmation_dialog()
		if dialog_result == wx.ID_YES:
			self.downloader.stop()
			self.installer.stop()
			from ASS import InstallationReviewPanel
			wx.CallAfter(self.GetParent().switch_panel, InstallationReviewPanel)  # Navigate back to previous page

	def show_cancel_confirmation_dialog(self):
		message = "Are you sure you want to cancel the download?"
		dialog = wx.MessageDialog(self, message, "Confirm Cancellation", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		result = dialog.ShowModal()
		dialog.Destroy()
		return result