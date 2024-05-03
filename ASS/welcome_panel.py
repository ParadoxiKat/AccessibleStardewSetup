# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import wx
from ASS.base_panel import BasePanel
from ASS.installation_path_panel import InstallationPathPanel

DESCRIPTION = """Welcome to Accessible Stardew Setup!

This will install SMAPI, Kokoro, ProjectFluent, and Stardew-Access on your system.
*** YOU MUST HAVE ALREADY INSTALLED STARDEW VALLEY BEFORE PROCEEDING ***
"""

class WelcomePanel(BasePanel):
	def __init__(self, parent):
		super(WelcomePanel, self).__init__(parent, "Welcome!")

		# Setup specific content
		self.setup_ui()

	def setup_ui(self):
		welcome_text = wx.StaticText(self, label="Welcome to Accessible Stardew Setup!")
		# Use a TextCtrl for the description to improve accessibility
		welcome_description = wx.TextCtrl(self, value=DESCRIPTION,
				style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_AUTO_URL | wx.BORDER_NONE)
		welcome_description.SetBackgroundColour(self.GetBackgroundColour())  # To make it blend in
		welcome_description.SetForegroundColour(self.GetForegroundColour())  # Match text color
		# Set a minimum size to ensure the text control is adequately displayed
		welcome_description.SetMinSize((400, -1))  # Width of 400 and default height
		welcome_description.SetFocus()

		# Add elements to the main sizer
		self.main_sizer.Add(welcome_text, 0, wx.ALL | wx.CENTER, 10)
		self.main_sizer.Add(welcome_description, 0, wx.EXPAND | wx.ALL, 10)

		# Add specific navigation buttons
		self.add_nav_button("&Next", self.on_next)

	def on_next(self, event):
		from ASS import InstallationPathPanel
		wx.CallAfter(self.GetParent().switch_panel, InstallationPathPanel)  # Switch to the installation path panel