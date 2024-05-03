# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

class DownloadedFileNotFoundException(FileNotFoundError):
	"""Exception raised when downloaded file is not found."""
	pass

class ReleaseNotFoundException(Exception):
	"""Exception raised when no suitable release is found."""
	pass

class RepositoryConfigurationError(Exception):
	"""Exception raised for errors in the repository configuration."""
	pass

class RepositoryNotFoundException(Exception):
	"""Exception raised when repository info is not found."""
	pass

class UnsupportedOSError(OSError):
	"""Exception raised when running on an OS not supported by SDV / SMAPI."""
	pass


__all__ = (
	"DownloadedFileNotFoundException",
	"ReleaseNotFoundException",
	"RepositoryConfigurationError",
	"RepositoryNotFoundException",
	"UnsupportedOSError"
)