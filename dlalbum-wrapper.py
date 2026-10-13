#!/usr/bin/env python3
import argparse
from pathlib import Path
from dlalbum import dl_album
import time

# Wrapper for yt-dlp to download multiple albums/playlists
parser = argparse.ArgumentParser(description="yt-dlp album download")
_ = parser.add_argument('links', type=str, nargs='+')
_ = parser.add_argument('-d', '--dest', type=Path, default="~/Music/Albums")

args = parser.parse_args()
dest: Path = args.dest.expanduser()

for l in args.links:
    dl_album(l, dest)
    time.sleep(30)
