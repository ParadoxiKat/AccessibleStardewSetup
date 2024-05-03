# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys

from .base_panel import BasePanel
from .downloader import Downloader
from .installer import Installer
from .welcome_panel import WelcomePanel

from .checkbox_grid import CheckBoxItemPanel, CheckBoxGrid
from .component_selection_panel import ComponentSelectionPanel
from .confirmation_dialog import ConfirmationDialog
from .download_and_install_panel import DownloadAndInstallPanel
from .downloader import Downloader
from .finish_panel import FinishPanel
from .installation_path_panel import InstallationPathPanel
from .installation_review_panel import InstallationReviewPanel
from .installer_frame import InstallerFrame
if sys.platform == 'win32':
	from .steam_launch_options_panel import SteamLaunchOptionsPanel
else:
	SteamLaunchOptionsPanel = None
from .welcome_panel import WelcomePanel

__all__ = tuple([ mod for mod in 
	[
		"BasePanel",
		"CheckBoxGrid",
		"CheckBoxItemPanel",
		"ComponentSelectionPanel",
		"ConfirmationDialog",
		"DownloadAndInstallPanel",
		"Downloader",
		"FinishPanel",
		"InstallationPathPanel",
		"InstallationReviewPanel",
		"Installer",
		"InstallerFrame",
		"SteamLaunchOptionsPanel",
		"WelcomePanel"
	] if mod is not None
])