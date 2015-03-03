#!/usr/bin/env python2

"""
A download script for Google Music using https://github.com/simon-weber/Unofficial-Google-Music-API.
More information at https://github.com/thebigmunch/gmusicapi-scripts.

Usage:
  gmdownload.py (-h | --help)
  gmdownload.py [-t TPL]... [options] [<output>]

Arguments:
  output                        Output file or directory name which can include a template pattern.
                                Defaults to name suggested by Google Music in your current directory.

Options:
  -h, --help                    Display help message.
  -c CRED, --cred CRED          Specify oauth credential file name to use/create. [Default: pwdauth]
  -s, --save                    Save credentials for future use. Warning: Credentials stored in plain text
  -l, --log                     Enable gmusicapi logging.
  -d, --dry-run                 Output list of songs that would be downloaded.
  -q, --quiet                   Don't output status messages.
                                With -l,--log will display gmusicapi warnings.
                                With -d,--dry-run will display song list.
  -m, --m3u8                    Output playlists in relative M3U8 format
  -t TPL, --template TPL        Template to apply to the relative paths in the m3u format.
                                (e.g. {artist} - {year} - {album}/{artist}-{trackNumber}-{title}.mp3)
"""

from __future__ import print_function, unicode_literals

import os
import sys

from docopt import docopt

from gmwrapper import MobileClientWrapper
from utils import safe_print


def main():
	cli = dict((key.lstrip("-<").rstrip(">"), value) for key, value in docopt(__doc__).items())

	print_ = safe_print if not cli['quiet'] else lambda *args, **kwargs: None

	if not cli['output']:
		cli['output'] = os.getcwd()

	if not cli['template']:
		cli['template'] = u'{artist} - {year} - {album}/{artist}-{trackNumber}-{title}.mp3'

	mmw = MobileClientWrapper(log=cli['log'])
	mmw.login(pwdauth_file=cli['cred'], save_cred=cli['save'])

	all_playlists = mmw.get_google_playlists()
	
	if all_playlists:
		if cli['dry-run']:
			print_("Found {0} playlists to download".format(len(all_playlists)))
			safe_print("\nPlaylists to download:\n")
			for playlist in all_playlists:
				safe_print("{0} by {1}".format(playlist['name'], playlist['ownerName']))
		else:
			print_("Downloading {0} playlists from Google Music\n".format(len(all_playlists)))
			mmw.download_playlist(all_playlists, output=cli['output'], template=cli['template'], m3u8=cli['m3u8'])
	else:
		safe_print("\nNo playlists to download")

	mmw.logout()
	print_("\nAll done!")


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.exit("\n\nExiting")
