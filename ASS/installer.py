# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import logging
import os
import shutil
import sys
import tempfile
import time
from typing import Dict, Any, Optional
import wx
import zipfile

from ASS.events import avEVT_INSTALLATION_COMPLETE, avEVT_NOTIFY, InstallationCompleteEvent, NotifyEvent
from ASS.exceptions import DownloadedFileNotFoundException

logger = logging.getLogger(__name__)

class Installer:
	def __init__(self, download_info: Dict[str, Any], sdv_dir: str, panel: Optional[wx.Panel]=None):
		if __name__ != '__main__' and panel is None: raise TypeError('Installer must have a panel unless running directly on the command line')
		self.panel = panel
		self.download_info = download_info
		self.sdv_dir = sdv_dir
		logger.debug(f"Initializing Installer with:\n{download_info}")
		self.keep_running = True
		self._temp_dir = tempfile.TemporaryDirectory()
		
	def __enter__(self):
		self.temp_dir = self._temp_dir.__enter__()
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		if self._temp_dir:
			self._temp_dir.__exit__(exc_type, exc_val, exc_tb)
			logger.debug(f"Temporary directory at {self.temp_dir} cleaned up")

	@property
	def mod_temp_dir(self):
		modtemp = os.path.join(self.temp_dir, "Mods")
		if not os.path.exists(modtemp):
			os.mkdir(modtemp)
		return modtemp

	@property
	def sdv_mods_dir(self):
		mods_dir = os.path.join(self.sdv_dir, "Mods")
		if not os.path.exists(mods_dir): raise FileNotFoundError(f"{mods_dir} does not exist...")
		elif not os.path.isdir(mods_dir): raise NotADirectoryError(f"{mods_dir} is not a directory???")
		else: return mods_dir

	def _retrieve_and_validate_download_path(self, name):
		try:
			downloaded_file_path = self.download_info[name]['download_path']
		except KeyError as e:
			raise Exception("Could not read downloaded file path from download_info") from e
		if not os.path.exists(downloaded_file_path): raise DownloadedFileNotFoundException(f'Could not find downloaded file for {name} at "{downloaded_file_path}"')
		return downloaded_file_path

	def _unpack_smapi_installer(self, smapi_installer_filename):
		# Open SMAPI installer zip file
		with open(smapi_installer_filename, 'rb') as installer_file:
			# Create ZipFile instance from opened file
			smapi_zip = zipfile.ZipFile(installer_file)
			# Create the OS appropriate path for the internal install.dat file we need
			install_dat_internal_path = f'{smapi_zip.namelist()[0]}internal/{self.panel.GetParent().platform}/install.dat'
			# Extract just this file to our temporary directory and store it's extracted path
			install_dat_extracted_path = smapi_zip.extract(install_dat_internal_path, path=self.temp_dir)
		return install_dat_extracted_path

	def _unpack_install_dat(self, install_dat_extracted_path):
		# Open the temporarily stored install.dat
		with open(install_dat_extracted_path, 'rb') as install_dat:
			install_zip = zipfile.ZipFile(install_dat)
			# Extract contents directly to SDV directory
			install_zip.extractall(self.sdv_dir)

	def install_smapi(self):
		self.log("Installing SMAPI")
		smapi_installer_filename = self._retrieve_and_validate_download_path("SMAPI")
		# Extract OS appropriate smapi install.dat (actually a zip file) to temp dir
		install_dat_extracted_path = self._unpack_smapi_installer(smapi_installer_filename)
		# Unpack the extracted install.dat into the Stardew Valley directory
		self._unpack_install_dat(install_dat_extracted_path)
		# Copy SDV's deps.json file for SMAPI
		shutil.copyfile(os.path.join(self.sdv_dir, "Stardew Valley.deps.json"), os.path.join(self.sdv_dir, "StardewModdingAPI.deps.json"))
		self.log(f"Installed SMAPI to {self.sdv_dir}")

	def _unpack_mod(self, mod_install_filename):
		# Open mod file
		with open(mod_install_filename, 'rb') as mod_file:
			# Create ZipFile instance from opened file
			mod_zip = zipfile.ZipFile(mod_file)
			# Extract the file to our temporary Mods directory
			mod_zip.extractall(path=self.mod_temp_dir)

	def install_mod(self, name, leave_in_temp=False):
		mod_install_filename = self._retrieve_and_validate_download_path(name)
		self._unpack_mod(mod_install_filename)
		if not leave_in_temp:
			shutil.copytree(self.mod_temp_dir, self.sdv_dir, dirs_exist_ok=True)
			shutil.rmtree(self.mod_temp_dir)
			self.log(f"Installed {name} to {self.sdv_mods_dir}.")

	def log(self, message):
		wx.CallAfter(wx.PostEvent, self.panel, NotifyEvent(avEVT_NOTIFY, message=message))

	def install_all(self):
		# SMAPI must be installed first
		logger.debug('Installing SMAPI')
		self.install_smapi()
		for name in self.download_info.keys():
			# Skip SMAPI as we already installed it
			if name == 'SMAPI': continue
			if not self.keep_running: return
			downloaded_file_path = self._retrieve_and_validate_download_path(name)
			message = f"Installing {name} from {downloaded_file_path}..."
			logger.debug(message)
			self.log(message)
			self.install_mod(name, True)
		logger.debug(f"Copying {self.mod_temp_dir} to {self.sdv_dir}")
		shutil.copytree(self.mod_temp_dir, os.path.join(self.sdv_dir, "Mods"), dirs_exist_ok=True)
		time.sleep(1)
		self.log(f"Installed mods to {self.sdv_mods_dir}.")
		wx.CallAfter(wx.PostEvent, self.panel, InstallationCompleteEvent(avEVT_INSTALLATION_COMPLETE))

	def stop(self):
		self.keep_running = False

