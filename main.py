#!/usr/bin/env python3
"""Emit the locked news image for 21 November 2026.

The image (entry.png, a JPEG) was composed from the verified world news of
Saturday 21 November 2026 and frozen as a static file. This program does no
network access and no randomness: it reads the file sitting next to this
script, validates that it is a whole JPEG inside the competition limits, and
writes the identical bytes to the output directory.
"""

import os
import sys

MAX_BYTES = 1_048_576          # 1 MiB
MAX_WIDTH = 1024
MAX_HEIGHT = 1024

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"

# JPEG markers we need to understand while walking the segments.
SOI = b"\xff\xd8"
EOI = b"\xff\xd9"
# Start-of-frame markers that carry width and height (baseline and
# progressive variants, excluding the DHT/DAC/JPGn markers).
SOF_MARKERS = {
    0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
    0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
}
# Markers that stand alone with no length field after them.
STANDALONE_MARKERS = {0x01} | set(range(0xD0, 0xD8))


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def read_dimensions(data):
    """Walk the JPEG segments and return (width, height) from the SOF."""
    if not data.startswith(SOI):
        fail("entry.png does not start with the JPEG SOI marker (FF D8)")
    pos = 2
    while pos + 1 < len(data):
        if data[pos] != 0xFF:
            fail(f"expected a JPEG marker at byte {pos}, found "
                 f"0x{data[pos]:02X}")
        marker = data[pos + 1]
        if marker == 0xD9:  # EOI
            fail("reached the JPEG end marker without finding a "
                 "start-of-frame segment")
        if marker in STANDALONE_MARKERS:
            pos += 2
            continue
        if pos + 4 > len(data):
            fail("truncated JPEG segment header")
        length = int.from_bytes(data[pos + 2:pos + 4], "big")
        if length < 2 or pos + 2 + length > len(data):
            fail(f"segment marker 0xFF{marker:02X} has an invalid length")
        if marker in SOF_MARKERS:
            body = data[pos + 4:pos + 2 + length]
            if len(body) < 5:
                fail("start-of-frame segment is too short")
            height = int.from_bytes(body[1:3], "big")
            width = int.from_bytes(body[3:5], "big")
            return width, height
        if marker == 0xDA:  # SOS: compressed scan data follows
            fail("reached the scan data without finding a "
                 "start-of-frame segment")
        pos += 2 + length
    fail("JPEG data ends before a start-of-frame segment")


def validate(data):
    """Check size, completeness and dimensions; return (width, height)."""
    if len(data) > MAX_BYTES:
        fail(f"entry.png is {len(data)} bytes ({len(data) / 1024:.1f} KiB), "
             f"over the {MAX_BYTES // 1024} KiB limit")
    if not data.endswith(EOI):
        fail("entry.png does not end with the JPEG EOI marker (FF D9)")
    width, height = read_dimensions(data)
    if width == 0 or height == 0:
        fail(f"start-of-frame reports a zero dimension: {width}x{height}")
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        fail(f"image is {width}x{height}, over the 1024x1024 limit")
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    try:
        with open(source, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        fail(f"cannot read {source}: {exc}")

    width, height = validate(data)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    destination = os.path.join(out_dir, OUTPUT_NAME)
    try:
        with open(destination, "wb") as handle:
            handle.write(data)
    except OSError as exc:
        fail(f"cannot write {destination}: {exc}")

    print(f"wrote {destination} ({len(data)} bytes, {width}x{height} JPEG)")


if __name__ == "__main__":
    main()
