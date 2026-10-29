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

new_dirs = []
count = 0
for link in set(args.links):
    new_dirs.append("\t- " + dl_album(link, dest))
    count += 1
    if count % 5 == 0:
        time.sleep(600)
    else:
        time.sleep(60)

print(f'New directories: \n{"\n".join(new_dirs)}')
