# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import github
import logging
import os
import re
import requests
from typing import Dict, Any, Optional
import wx

from ASS.events import avEVT_DOWNLOADS_COMPLETE, avEVT_NOTIFY, DownloadsCompleteEvent, NotifyEvent
from ASS.exceptions import ReleaseNotFoundException, RepositoryConfigurationError, RepositoryNotFoundException

logger = logging.getLogger(__name__)

class Downloader:
	def __init__(self, download_info: Dict[str, Any], token: Optional[str]=None, download_dir: Optional[str]=None, panel: Optional[wx.Panel]=None):
		if __name__ != '__main__' and panel is None: raise TypeError('Downloader must have a panel unless running directly on the command line')
		self.panel = panel
		if download_dir is None:
			download_dir = Path(os.path.abspath('.'))
		self.download_dir = download_dir
		self.github = github.Github(token)
		self.download_info = download_info
		logger.debug(f"Initializing Downloader with:\n{download_info}")
		self.repos = {}
		self.releases_cache = {}
		self.assets_cache = {}
		self.keep_running = True

	def get_repo(self, name: str) -> github.Repository:
		if name not in self.repos:
			repo_info = self.download_info.get(name)
			if not repo_info:
				raise RepositoryNotFoundException(f"Cannot load info for {name}")
			self.repos[name] = self.github.get_repo(repo_info['repository'])
		return self.repos[name]

	def get_release(self, name: str):
		repo = self.get_repo(name)
		if name not in self.releases_cache:
			self.releases_cache[name] = list(repo.get_releases())

		repo_info = self.download_info[name]
		include_prerelease = repo_info.get('include_prerelease', False)
		title_filter = repo_info.get('release_title_filter', None)

		filtered_releases = self.releases_cache[name]
		if title_filter:
			pattern = re.compile(title_filter)
			filtered_releases = [release for release in filtered_releases if pattern.match(release.title)]

		for release in filtered_releases:
			if include_prerelease or not release.prerelease:
				return release
		raise ReleaseNotFoundException(f"No suitable release found for {name}")

	def get_asset(self, name: str):
		release = self.get_release(name)
		if release.id not in self.assets_cache:
			self.assets_cache[release.id] = list(release.get_assets())

		assets = self.assets_cache[release.id]
		if not assets:
			raise AssetNotFoundException("No assets found for the release")

		asset_config = self.download_info[name].get('asset_selector', {})
		pattern = asset_config.get('pattern', None)
		match_selector = asset_config.get('match', False)
		if pattern is not None:
			compiled_pattern = re.compile(pattern)
			for asset in assets:
				if (match_selector and compiled_pattern.match(asset.name)) or (not match_selector and not compiled_pattern.match(asset.name)):
					return asset
		return assets[0]

	def download_asset(self, name: str):
		logger.debug(f'Attempting to download {name}')
		asset = self.get_asset(name)
		filename, ext = os.path.splitext(asset.name)
		local_file_path = self.download_dir / f"{filename}_{asset.id}{ext}"

		# Check if the file already exists to avoid re-downloading
		if local_file_path.exists():
			self.log(f"File already downloaded: {local_file_path}")
			return local_file_path

		# Download the file
		self.log(f"Downloading {asset.name} to {local_file_path}")
		response = requests.get(asset.browser_download_url, stream=True)
		with open(local_file_path, 'wb') as f:
			for chunk in response.iter_content(chunk_size=8192):
				if not self.keep_running: break
				f.write(chunk)
		if not self.keep_running and os.path.exists(local_file_path):
			os.remove(local_file_path)
			return None
		return local_file_path

	def log(self, message):
		wx.CallAfter(wx.PostEvent, self.panel, NotifyEvent(avEVT_NOTIFY, message=message))

	def download_all(self):
		for name, data in self.download_info.items():
			logger.debug(f'Downloading {name}')
			if not self.keep_running: return
			self.log(f"Downloading {name}...")
			try:
				path = self.download_asset(name)
				if path is None:
					self.log(f"Download of {name} canceled.")
				else:
					self.log(f"Downloaded {name} to \"{path}\"")
					data['download_path'] = path
			except requests.RequestException as e:
				self.log(f"Failed to download {name}: {e}")
		wx.CallAfter(wx.PostEvent, self.panel, DownloadsCompleteEvent(avEVT_DOWNLOADS_COMPLETE))

	def stop(self):
		self.keep_running = False

