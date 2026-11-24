"""Entry program for news-image-20261124.

Copies the vendored entry.png to $MAKEFUN_OUTPUT_DIR/entry.png.
Python 3.13 standard library only; no network; deterministic.
"""

import hashlib
import os
import struct
import sys

EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def fail(message):
    print("error: " + message, file=sys.stderr)
    sys.exit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    dst = os.path.join(out_dir, "entry.png")

    with open(src, "rb") as fh:
        data = fh.read()

    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("entry.png is not a PNG (bad magic)")
    if len(data) < 33 or data[12:16] != b"IHDR":
        fail("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if width != EXPECTED_WIDTH or height != EXPECTED_HEIGHT:
        fail("entry.png is %dx%d, expected %dx%d"
             % (width, height, EXPECTED_WIDTH, EXPECTED_HEIGHT))
    if len(data) > 1048576:
        fail("entry.png is %d bytes, over the 1 MiB cap" % len(data))

    digest = hashlib.sha256(data).hexdigest()
    os.makedirs(out_dir, exist_ok=True)
    with open(dst, "wb") as fh:
        fh.write(data)

    with open(dst, "rb") as fh:
        written = fh.read()
    if written != data:
        fail("written entry.png does not match the vendored file")
    print("entry.png: %dx%d, %d bytes, sha256 %s"
          % (width, height, len(data), digest))


if __name__ == "__main__":
    main()
