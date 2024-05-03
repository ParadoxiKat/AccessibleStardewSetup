# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import wx
from ASS import BasePanel, CheckBoxGrid

class ComponentSelectionPanel(BasePanel):
	def __init__(self, parent):
		super(ComponentSelectionPanel, self).__init__(parent, "Select Components to Install")
		self.setup_ui()

	def setup_ui(self):
		self.instructions = wx.StaticText(self, label="Select optional components to install:")
		self.main_sizer.Add(self.instructions, 0, wx.ALL | wx.EXPAND, 5)
		self.instructions.SetFocus()

		self.checkbox_grid = CheckBoxGrid(self)
		# add the items loaded from JSON
		for name, data in self.Parent.download_info.items():
			if not isinstance(data, dict): continue
			self.checkbox_grid.add_item(name, data)
		self.main_sizer.Add(self.checkbox_grid, 1, wx.EXPAND | wx.ALL, 5)

		self.add_nav_button("&Previous", self.on_prev)
		self.add_nav_button("&Next", self.on_next)

	def on_next(self, event):
		from ASS import InstallationReviewPanel
		wx.CallAfter(self.GetParent().switch_panel, InstallationReviewPanel)

	def on_prev(self, event):
		from ASS import InstallationPathPanel
		wx.CallAfter(self.GetParent().switch_panel, InstallationPathPanel)
