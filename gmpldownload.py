#!/usr/bin/env python2

"""
A download script for Google Music using https://github.com/simon-weber/Unofficial-Google-Music-API.
More information at https://github.com/thebigmunch/gmusicapi-scripts.

Usage:
  gmdownload.py (-h | --help)
  gmdownload.py [-f FILTER]... [options] [<output>]

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
  -m, --m3u                     Output playlists in relative M3U format
  -f FILTER, --filter FILTER    Filter Google songs by field:pattern pair (e.g. "artist:Muse").
                                Songs can match any filter criteria.
                                This option can be set multiple times.
  -a, --all                     Songs must match all filter criteria.
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

	mmw = MobileClientWrapper(log=cli['log'])
	mmw.login(pwdauth_file=cli['cred'], save_cred=cli['save'])

	all_playlists = mmw.get_google_playlists(filters=cli['filter'], filter_all=cli['all'])
	
	if all_playlists:
		if cli['dry-run']:
			print_("Found {0} playlists to download".format(len(all_playlists)))
			safe_print("\nPlaylists to download:\n")
			for playlist in all_playlists:
				safe_print("{0} by {1}".format(playlist['name'], playlist['ownerName']))
		else:
			print_("Downloading {0} playlists from Google Music\n".format(len(all_playlists)))
			mmw.download_playlist(all_playlists, cli['output'], cli['m3u'])
	else:
		safe_print("\nNo playlists to download")

	mmw.logout()
	print_("\nAll done!")


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.exit("\n\nExiting")
