# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import wx
import wx.lib.scrolledpanel as scrolled

class CheckBoxItemPanel(wx.Panel):
	def __init__(self, parent, name, component_data):
		super(CheckBoxItemPanel, self).__init__(parent, style=wx.BORDER_SIMPLE)
		self.name = name
		is_mandatory = self.is_mandatory = component_data['is_mandatory']
		self.component_data = component_data
		self.SetSizer(wx.BoxSizer(wx.HORIZONTAL))

		# Main checkbox with name of mod
		self.main_checkbox = wx.CheckBox(self, label=name)
		self.main_checkbox.SetValue(component_data['is_mandatory'])
		self.main_checkbox.Bind(wx.EVT_CHECKBOX, self.on_main_checkbox)
		if is_mandatory:
			# Visually indicate that the checkbox is disabled
			self.main_checkbox.SetForegroundColour(wx.Colour(128, 128, 128))  # Grey color
			self.main_checkbox.SetToolTip("This component is required and cannot be deselected.")

		# Additional options as checkboxes, initially disabled
		asset_selector = component_data.get('asset_selector', None)
		if asset_selector is None:
			self.variant_checkbox = wx.CheckBox(self, label="No variants")
			self.enableVariant_checkbox = False
			self.variant_checkbox.SetValue(False)
		else:
			self.variant_checkbox = wx.CheckBox(self, label=asset_selector['name'])
			self.enableVariant_checkbox = True
			self.variant_checkbox.SetValue(asset_selector.get('match', False))
		self.variant_checkbox.Enable(self.enableVariant_checkbox)
		self.variant_checkbox.Bind(wx.EVT_CHECKBOX, self.on_variant_checkbox)

		self.prerelease_checkbox = wx.CheckBox(self, label="Include Pre&release")
		self.enablePrerelease_checkbox = component_data.get('offer_prerelease', False)
		self.prerelease_checkbox.Enable(self.enablePrerelease_checkbox)
		self.prerelease_checkbox.SetValue(component_data.get('include_prerelease', False))
		self.prerelease_checkbox.Bind(wx.EVT_CHECKBOX, self.on_prerelease_checkbox)

		# Add checkboxes to the horizontal sizer
		self.GetSizer().Add(self.main_checkbox, 1, wx.ALL | wx.CENTER, 5)
		self.GetSizer().Add(self.variant_checkbox, 1, wx.ALL | wx.CENTER, 5)
		self.GetSizer().Add(self.prerelease_checkbox, 1, wx.ALL | wx.CENTER, 5)

	def on_main_checkbox(self, event):
		# Enable/disable other checkboxes based on the main checkbox state
		if self.is_mandatory:
			self.main_checkbox.SetValue(True)
			return
		state = self.main_checkbox.IsChecked()
		self.variant_checkbox.Enable(state and enableVariant_checkbox)
		self.prerelease_checkbox.Enable(state and enablePrerelease_checkbox)

	def on_variant_checkbox(self, event):
		asset_selector = self.component_data.get('asset_selector', None)
		if asset_selector is not None:
			asset_selector['match'] = self.variant_checkbox.IsChecked()

	def on_prerelease_checkbox(self, event):
		if self.component_data.get('offer_prerelease', False):
			self.component_data['include_prerelease'] = self.prerelease_checkbox.IsChecked()

class CheckBoxGrid(scrolled.ScrolledPanel):
	def __init__(self, parent):
		super(CheckBoxGrid, self).__init__(parent)
		self.setup_ui()

	def setup_ui(self):
		self.SetSizer(wx.BoxSizer(wx.VERTICAL))
		self.SetupScrolling(scroll_x=False, scroll_y=True)

	def add_item(self, name, component_data):
		item = CheckBoxItemPanel(self, name, component_data)
		self.GetSizer().Add(item, 0, wx.EXPAND | wx.ALL, 5)
		self.Layout()
		self.SetupScrolling(scroll_x=False, scroll_y=True, scrollToTop=False)
