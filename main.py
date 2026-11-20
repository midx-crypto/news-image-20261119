#!/usr/bin/env python3
"""Entry point: copy the vendored front-page image to /output/entry.png.

The image is built ahead of time by build.py (PIL, stdlib only besides
Pillow at build time). This program does no drawing and no network: it
copies entry.png next to this file into the output directory, atomically,
and validates the PNG magic bytes and the 1 MiB size cap.
"""
import hashlib
import os
import shutil
import sys
import tempfile

MAX_BYTES = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(src):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1

    with open(src, "rb") as fh:
        data = fh.read()
    if data[:8] != PNG_MAGIC:
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"entry.png is {len(data)} bytes, over the 1 MiB cap",
              file=sys.stderr)
        return 1

    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".png")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, dst)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise

    print("wrote", dst, len(data), "bytes",
          hashlib.sha256(data).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())
