#!/usr/bin/env python3
import argparse
from pathlib import Path
import re
import subprocess
import shutil


# Wrapper for yt-dlp to download an album
def main():
    parser = argparse.ArgumentParser(description="yt-dlp album download")
    _ = parser.add_argument('link', type=str)
    _ = parser.add_argument('-d',
                            '--dest',
                            type=Path,
                            default="~/Music/Albums")

    args = parser.parse_args()
    link: str = args.link
    dest: Path = args.dest.expanduser()
    dl_album(link, dest)


# Downloads playlist from link and move files to dest/{playlist_name}
def dl_album(link: str, dest: Path):
    ytdlp_args = [
        'yt-dlp', '-x', '--audio-quality', '0', '--no-keep-video',
        '--embed-thumbnail', '--embed-metadata', '-o', "'%(title)s'", link
    ]

    print(f'dlalbum:\n\tytdlp_args = {ytdlp_args}\n\tdest = {dest}')

    # Run yt-dlp on provided link (expected to be a playlist) and try to get
    # playlist name from the output
    proc = subprocess.run(ytdlp_args, capture_output=True, text=True)
    # [download] Downloading playlist: 15
    m = re.search(r"Downloading playlist: (.*)", proc.stdout, re.MULTILINE)
    if not m:
        raise ValueError(
            f"Could not find playlist name in output!\nOutput:\n{proc.stdout}")

    # Replace ':' for Android filesystem
    album_name = m.group(1).replace(":", "_")

    # Make directory based on album name and move all music files in cwd to it
    new_dest = dest / album_name
    _ = new_dest.mkdir(parents=True, exist_ok=True)

    # Just check for expected possible music file extensions for personal usage
    music_suffixes = [".mp3", ".opus", ".flac", ".wav"]

    moved: list[str] = []
    for p in Path.cwd().iterdir():
        if p.is_file() and p.suffix.lower() in music_suffixes:
            new_name = p.name.replace(":", "_")
            _ = shutil.move(p, new_dest / new_name)
            moved.append(new_name)

    print(f'Moved the following files to {new_dest}:\n{"\n".join(moved)}')


if __name__ == "__main__":
    main()
