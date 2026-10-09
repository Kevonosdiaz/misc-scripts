#!/usr/bin/env python3
import argparse
from pathlib import Path
import subprocess

# Small wrapper to invoke kepubify and move results to library dir
parser = argparse.ArgumentParser(description="Small kepubify wrapper")
_ = parser.add_argument('path', type=Path)
_ = parser.add_argument('-d',
                        '--dest',
                        type=Path,
                        default="~/Documents/library/")

args = parser.parse_args()
path = args.path.expanduser()
dest = args.dest.expanduser()
pathstr = str(path)
deststr = str(dest)
print(f'pathstr = {pathstr}\ndeststr = {deststr}')

_ = subprocess.run(["kepubify", pathstr])

if path.is_file():
    # Expect converted file to exist now,
    # try to move it to dest directory after stripping '_converted'
    conv = pathstr.replace('.epub', '_converted.kepub.epub')
    cleaned = conv.replace('_converted', '')
    old_path = Path(conv)
    new_path = Path(deststr + "/" + cleaned)

    # Make destination directory if needed
    new_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        _ = old_path.rename(new_path)
        print(f'Wrote to {new_path} successfully.')
    except FileNotFoundError:
        print(f'Source file {old_path} was not found')
    except OSError as e:
        print(f'OSError: {e}')

elif path.is_dir():
    # Expect *_converted directory to exist now,
    # try to move it into destination dir
    conv = pathstr + "_converted"
    old_path = Path(conv)
    new_path = Path(deststr + "/" + pathstr)

    # Make destination directory if needed
    new_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        _ = old_path.rename(new_path)
        print(f'Wrote to {new_path} successfully.')
    except FileNotFoundError:
        print(f'Source file {old_path} was not found')
    except OSError as e:
        print(f'OSError: {e}')

else:
    print("Provided path neither file nor dir. Aborting.")
