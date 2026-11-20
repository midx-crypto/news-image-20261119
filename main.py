#!/usr/bin/env python3
"""Entry program for make.fun bounty news-image-20261119 (round 3).

The entry image (entry.png, 1024x1024, drawn in code with Pillow by
build.py) is shipped in this repository. This program copies it
byte-for-byte to the output path given as the first command-line
argument, then verifies the copy's SHA-256 against the known hash.

Standard library only: hashlib, os, shutil, sys.
"""
import hashlib
import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
EXPECTED_SHA256 = "e30d77f09bbd7225678e9bc86ed0e8a93ce2c53dfeb7ba419b0774adaa72fa7a"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv):
    if len(argv) != 2:
        print("usage: python3 main.py <output-path>", file=sys.stderr)
        return 2
    out = argv[1]
    if not os.path.isfile(SOURCE):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    if sha256_of(SOURCE) != EXPECTED_SHA256:
        print("entry.png hash mismatch; refusing to copy", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    shutil.copyfile(SOURCE, out)
    if sha256_of(out) != EXPECTED_SHA256:
        print("output hash mismatch", file=sys.stderr)
        return 1
    print("wrote %s (sha256 %s)" % (out, EXPECTED_SHA256))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
