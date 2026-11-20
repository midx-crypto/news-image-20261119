"""Entrypoint: build entry.png (stdlib only; drawing lives in build.py)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import build


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "")
    if out_dir:
        out = os.path.join(out_dir, "entry.png")
    else:
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build.build(out)
    # Validation: file exists, PNG magic, size <= 1 MiB, dimensions <= 1024x1024.
    if not os.path.isfile(out):
        raise SystemExit("missing output: " + out)
    size = os.path.getsize(out)
    if size > 1048576:
        raise SystemExit("entry.png too large: %d bytes" % size)
    with open(out, "rb") as fh:
        head = fh.read(8)
    if head != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG")
    import struct
    with open(out, "rb") as fh:
        fh.seek(16)
        w, h = struct.unpack(">II", fh.read(8))
    if w > 1024 or h > 1024:
        raise SystemExit("entry.png too big: %dx%d" % (w, h))
    print("wrote %s (%d bytes, %dx%d)" % (out, size, w, h))


if __name__ == "__main__":
    main()
