#!/usr/bin/env python3
import argparse
from pathlib import Path
import subprocess

# Wrapper for yt-dlp to download an album
parser = argparse.ArgumentParser(description="yt-dlp album download")
_ = parser.add_argument('link', type=str)
_ = parser.add_argument('-d', '--dest', type=Path, default="~/Music/Albums")

args = parser.parse_args()
link = args.link
dest = args.dest.expanduser()
deststr = str(dest)
ytdlp_args = [
    'yt-dlp', '-x', '--audio-quality', '0', '--no-keep-video',
    '--embed-thumbnail', '--embed-metadata', '-o', "'%(title)s'"
]
# Maybe use pexpect instead?
_ = subprocess.run(ytdlp_args + args.link)
