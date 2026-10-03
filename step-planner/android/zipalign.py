#!/usr/bin/env python3
"""Minimal zipalign: rewrites an APK so every stored (uncompressed) entry starts on a 4-byte boundary."""
import struct, sys, zipfile

def align(src, dst, boundary=4):
    with zipfile.ZipFile(src) as zin, open(dst, "wb") as raw:
        zout = zipfile.ZipFile(raw, "w")
        for info in zin.infolist():
            data = zin.read(info)
            zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
            zi.compress_type = info.compress_type
            zi.external_attr = info.external_attr
            zi.extra = b""
            if info.compress_type == zipfile.ZIP_STORED:
                start = raw.tell() + 30 + len(info.filename.encode("utf-8"))
                need = (-start) % boundary
                if need:
                    pad = need if need >= 4 else need + boundary  # an extra field needs a 4-byte header
                    zi.extra = struct.pack("<HH", 0xD935, pad - 4) + b"\0" * (pad - 4)
            zout.writestr(zi, data)
        zout.close()

def check(path, boundary=4):
    bad = []
    with open(path, "rb") as f, zipfile.ZipFile(path) as z:
        for info in z.infolist():
            if info.compress_type != zipfile.ZIP_STORED:
                continue
            f.seek(info.header_offset + 26)
            n, m = struct.unpack("<HH", f.read(4))
            if (info.header_offset + 30 + n + m) % boundary:
                bad.append(info.filename)
    return bad

if __name__ == "__main__":
    if sys.argv[1] == "--check":
        bad = check(sys.argv[2])
        print("aligned" if not bad else "NOT aligned: " + ", ".join(bad))
        sys.exit(1 if bad else 0)
    align(sys.argv[1], sys.argv[2])
