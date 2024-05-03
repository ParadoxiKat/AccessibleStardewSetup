# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
import os
from requests.structures import CaseInsensitiveDict
import psutil 
import shutil
import vdf
import wx

from ASS.base_panel import BasePanel

logger = logging.getLogger(__name__)

class SteamLaunchOptionsPanel(BasePanel):
	def __init__(self, parent):
		super(SteamLaunchOptionsPanel, self).__init__(parent, "Add Steam Launch Options?")
		self.cancel_button.Hide()
		self.cancel_button.Enable(False)
		self._configs = None
		self._launch_options = None
		self.sdv_path = 		self.GetParent().installation_path
		self.setup_ui()

	@property
	def appid(self):
		try:
			with open(os.path.join(self.sdv_path, 'steam_appid.txt')) as f:
				appid = f.read()
		except Exception as e:
			appid = None
		return appid or "413150"

	@property
	def steam_userdata_path(self):
		if 'steamapps' not in self.sdv_path: return None
		steam_path = self.sdv_path.split(f'{os.path.sep}steamapps')[0]
		userdata_path = os.path.join(steam_path, "userdata")
		if not os.path.exists(userdata_path): raise FileNotFoundError(f"Could not find userdata directory at {userdata_path}")
		elif not os.path.isdir(userdata_path): raise NotADirectoryError("{userdata_path} is not a directory???")
		return userdata_path

	@property
	def localconfigs(self):
		configs = {}
		if self._configs is None:
			try:
				for accountid  in os.listdir(self.steam_userdata_path):
					config_path = os.path.join(self.steam_userdata_path, accountid, "config", "localconfig.vdf")
					if not os.path.exists(config_path): raise FileNotFoundError(f"Could not load Steam config from {config_path}")
					with open(config_path, encoding='utf-8') as f:
						lconfig = vdf.load(f, mapper=CaseInsensitiveDict)
					name = lconfig["UserLocalConfigStore"]["friends"]["PersonaName"]
					if self.appid not in lconfig["UserLocalConfigStore"]["Software"]["Valve"]["Steam"]["apps"]: continue
					configs[name] = {"path": config_path, "data": lconfig}
				self._configs = configs
			except Exception as e:
				logger.debug(f"Failed to modify steam launch options due to: {e}")
				raise
		return self._configs

	@property
	def launch_options(self):
		if self._launch_options is None:
			smapi_path = os.path.join(self.sdv_path, "StardewModdingAPI.exe")
			loptions = f'"{smapi_path}" %command%'
			self._launch_options = loptions
		return self._launch_options

	def setup_ui(self):
		# Instruction text
		instruction_text = wx.StaticText(self, label="Would you like to attempt adding SMAPI launch options to Steam?\nPlease ensure Steam is exited before proceeding.")
		instruction_text.SetFocus()
		self.main_sizer.Add(instruction_text, 0, wx.ALL | wx.EXPAND, 10)

		# Checkbox for user to choose if they want to add launch options
		self.launch_option_checkbox = wx.CheckBox(self, label="&Add LaunchOptions to Steam?")
		self.main_sizer.Add(self.launch_option_checkbox, 0, wx.ALL | wx.EXPAND, 5)

		# Next button to proceed
		next_button = self.add_nav_button("&Next", self.on_next)

	def _get_steam_process(self):
		for process in psutil.process_iter(['name']):
			if "steam" in process.name().lower() and process.exe().lower().endswith('steam.exe'):
				return process
		return None

	def is_steam_running(self):
		"Check if the Steam process is currently running."
		steam = self._get_steam_process()
		if steam is not None:
			return steam.is_running
		return False

	def prompt_steam_exit(self):
		"Prompt the user to exit Steam with a custom dialog."
		dlg = wx.Dialog(self, title="Steam is running")
		vbox = wx.BoxSizer(wx.VERTICAL)
		msg = wx.StaticText(dlg, label="Please exit Steam to continue.")
		vbox.Add(msg, flag=wx.ALL|wx.CENTER, border=10)
		retry_btn = wx.Button(dlg, label="&Retry")
		cancel_btn = wx.Button(dlg, label="&Cancel")
		retry_btn.Bind(wx.EVT_BUTTON, lambda evt: self.retry_steam_check(dlg))
		cancel_btn.Bind(wx.EVT_BUTTON, lambda evt: dlg.Destroy())
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(retry_btn)
		hbox.Add(cancel_btn, flag=wx.LEFT, border=5)
		vbox.Add(hbox, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)
		dlg.SetSizer(vbox)
		dlg.ShowModal()

	def retry_steam_check(self, dlg):
		"Retry checking if Steam has been closed."
		if not self.is_steam_running():
			dlg.Destroy()
			self.add_steam_launch_options()
		# If Steam is still running, do nothing and let the user try to close it again.

	def add_steam_launch_options(self):
		"Add launch options to Steam."
		for name, info in self.localconfigs.items():
			try:
				path = info["path"]
				lconfig = info['data']
				lconfig["UserLocalConfigStore"]["Software"]["Valve"]["Steam"]["apps"][self.appid]['LaunchOptions'] = self.launch_options
			except Exception as E:
				logger.exception("Failed adding launch options to config")
				raise
			try:
				shutil.copy2(path, path+".bak")
			except Exception as e:
				logger.exception(f"Failed to back up {path}")
				raise
			with open(path, 'w', encoding='utf-8', newline='') as f:
				vdf.dump(lconfig, f, pretty=True)

	def on_cancel(self, event):
		"Overridden to do nothing or to show a message that canceling is not an option anymore."
		wx.MessageBox("Canceling is not available at this stage.", "Cannot Cancel", wx.OK | wx.ICON_INFORMATION)

	def on_next(self, event):
		if self.launch_option_checkbox.IsChecked():
			if self.is_steam_running():
				self.prompt_steam_exit()
			else:
				self.add_steam_launch_options()
		from ASS.finish_panel import FinishPanel 
		wx.CallAfter(self.GetParent().switch_panel, FinishPanel)
