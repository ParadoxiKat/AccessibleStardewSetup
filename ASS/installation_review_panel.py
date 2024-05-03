# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import wx

from ASS import BasePanel

class InstallationReviewPanel(BasePanel):
	def __init__(self, parent):
		super(InstallationReviewPanel, self).__init__(parent, "Review Components Selected for Install")
		self.setup_ui()

	def setup_ui(self):
		# Layout elements
		instruction_text = wx.StaticText(self, label="Review components to be installed:")
		self.main_sizer.Add(instruction_text, 0, wx.ALL | wx.EXPAND, 5)

		# Setup the read-only text box
		self.review_textbox = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_SIMPLE)
		self.review_textbox.SetValue(self.get_selected_components())
		self.main_sizer.Add(self.review_textbox, 1, wx.EXPAND | wx.ALL, 5)
		self.review_textbox.SetFocus()

		# Add navigation buttons
		self.add_nav_button("&Previous", self.on_prev)
		self.add_nav_button("&Install", self.on_install)

	def get_selected_components(self):
		selected_components = []
		download_info = self.GetParent().download_info
		for name, component_data in download_info.items():
			# remove '&' used to mark button names as hotkeys
			name = name.replace('&', '')
			asset_selector = component_data.get('asset_selector', None)
			if asset_selector is not None and asset_selector.get('match', False):
				variant = ' ' + asset_selector.get('name', 'Unnamed variant')
			else:
				variant = ''
			include_prerelease = ' (including prerelease versions)' if component_data.get('include_prerelease', False) else ''
			selected_components.append(f'{name}{variant}{include_prerelease}')
		return '\n'.join(selected_components)

	def on_prev(self, event):
		from ASS import ComponentSelectionPanel
		wx.CallAfter(self.GetParent().switch_panel, ComponentSelectionPanel)

	def on_install(self, event):
		from ASS import DownloadAndInstallPanel
		wx.CallAfter(self.GetParent().switch_panel, DownloadAndInstallPanel)