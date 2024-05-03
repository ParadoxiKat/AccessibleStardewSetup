# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import wx

# Custom events for updating the GUI
avEVT_NOTIFY = wx.NewEventType()
EVT_NOTIFY = wx.PyEventBinder(avEVT_NOTIFY, 1)

class NotifyEvent(wx.PyCommandEvent):
	def __init__(self, etype, eid=-1, message=None):
		super(NotifyEvent, self).__init__(etype, eid)
		self._message = message

	def GetMessage(self):
		return self._message

avEVT_DOWNLOADS_COMPLETE = wx.NewEventType()
EVT_DOWNLOADS_COMPLETE = wx.PyEventBinder(avEVT_DOWNLOADS_COMPLETE, 1)

class DownloadsCompleteEvent(wx.PyCommandEvent):
	def __init__(self, etype, eid=-1):
		super(DownloadsCompleteEvent, self).__init__(etype, eid)

avEVT_INSTALLATION_COMPLETE = wx.NewEventType()
EVT_INSTALLATION_COMPLETE = wx.PyEventBinder(avEVT_INSTALLATION_COMPLETE, 1)

class InstallationCompleteEvent(wx.PyCommandEvent):
	def __init__(self, etype, eid=-1):
		super(InstallationCompleteEvent, self).__init__(etype, eid)

# List of symbols to export when using 'from events import *'
__all__ = (
	'avEVT_NOTIFY', 'EVT_NOTIFY', 'NotifyEvent',
	'avEVT_DOWNLOADS_COMPLETE', 'EVT_DOWNLOADS_COMPLETE', 'DownloadsCompleteEvent',
	'avEVT_INSTALLATION_COMPLETE', 'EVT_INSTALLATION_COMPLETE', 'InstallationCompleteEvent'
)
