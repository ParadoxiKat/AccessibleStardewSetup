# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from appdirs import user_data_dir
from dotenv import load_dotenv
from pathlib import Path
import logging
import wx
import ASS.installer_frame

APP_DIR = None

def get_app_dir():
	global APP_DIR
	if APP_DIR is None:
		# This creates a consistent application-specific directory across platforms
		APP_DIR = Path(user_data_dir("AccessibleStardewSetup", "Darkade Games"))
		APP_DIR.mkdir(parents=True, exist_ok=True)
	return APP_DIR

log_file_path = get_app_dir() / "ASS.log"
logging.basicConfig(filename=log_file_path, filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info('starting')

def main():
	load_dotenv()
	app = wx.App(False)
	ass = ASS.installer_frame.InstallerFrame(None, title="Accessible Stardew Setup", app_dir=get_app_dir())
	ass.Show()
	app.MainLoop()

if __name__ == "__main__":
	main()