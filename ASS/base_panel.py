# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import wx

class BasePanel(wx.Panel):
	def __init__(self, parent, title):
		super(BasePanel, self).__init__(parent)
		self.title = title
		
		# Setup the main content layout
		self.main_sizer = wx.BoxSizer(wx.VERTICAL)
		
		# Setup the navigation bar
		self.setup_navigation()

		# Set the sizer for the panel
		self.SetSizer(self.main_sizer)

	def setup_navigation(self):
		"""Setup navigation controls that are common across all panels."""
		self.nav_sizer = wx.BoxSizer(wx.HORIZONTAL)
		
		# Cancel button is common to all panels
		self.cancel_button = self.add_nav_button("&Cancel", self.on_cancel)
		
		# Add navigation bar to the main sizer
		self.main_sizer.Add(self.nav_sizer, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

	def on_cancel(self, event):
		# Prompt the user to confirm cancellation
		message = "Are you sure you want to cancel the installation?"
		caption = "Confirm Cancellation"
		style = wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
		dialog = wx.MessageDialog(self, message, caption, style)
		
		if dialog.ShowModal() == wx.ID_YES:
			wx.CallAfter(self.GetParent().Close)  # Only close if the user confirms

		dialog.Destroy()

	def add_nav_button(self, label, handler):
		"""Utility method to add buttons to the navigation bar with optional hotkey."""
		button = wx.Button(self, label=label)
		button.Bind(wx.EVT_BUTTON, handler)
		self.nav_sizer.Add(button, 0, wx.ALL, 5)
		self.Layout()  # Update the layout after adding a button
		return button

