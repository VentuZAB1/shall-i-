import struct, sys, re, os, glob

def lz4_block(src, out_len):
    dst = bytearray(); i = 0; n = len(src)
    while i < n:
        tok = src[i]; i += 1
        lit = tok >> 4
        if lit == 15:
            while True:
                b = src[i]; i += 1; lit += b
                if b != 255: break
        dst += src[i:i+lit]; i += lit
        if i >= n: break
        off = src[i] | (src[i+1] << 8); i += 2
        ml = tok & 15
        if ml == 15:
            while True:
                b = src[i]; i += 1; ml += b
                if b != 255: break
        ml += 4
        start = len(dst) - off
        for k in range(ml): dst.append(dst[start + k])
    return bytes(dst)

def chunks(path):
    data = open(path, 'rb').read()
    assert data[:8] == b'<roblox!', 'not binary rbxm'
    i = 32
    while i < len(data):
        name = data[i:i+4]; clen, ulen, _ = struct.unpack('<III', data[i+4:i+16]); i += 16
        if clen == 0:
            body = data[i:i+ulen]; i += ulen
        else:
            raw = data[i:i+clen]; i += clen
            if raw[:4] == b'\x28\xb5\x2f\xfd': body = b'<zstd>'
            else: body = lz4_block(raw, ulen)
        yield name, body
        if name == b'END\x00': break

pat = re.compile(rb'[^\n]{0,90}(CurrentCamera|workspace\.Camera|Camera\.CFrame|CameraType|\.Focus\s*=|BindToRenderStep)[^\n]{0,90}')
for path in sys.argv[1:]:
    blob = b''.join(b for _, b in chunks(path))
    pid = os.path.normpath(path).split(os.sep)[-3]
    names = set(m.group(1).decode('latin1') for m in re.finditer(rb'CreateToolbar\(\s*"([^"]{1,40})"', blob))
    hits = [m.group(0).decode('latin1', 'replace').strip() for m in pat.finditer(blob)]
    sets = [h for h in hits if re.search(r'(Camera\.CFrame|\.CFrame)\s*=|CameraType\s*=|Focus\s*=', h)]
    print(f"== {pid} toolbars={sorted(names)} zstd={b'<zstd>' in blob} camera-mentions={len(hits)} camera-SETS={len(sets)}")
    for h in sets[:10]: print("   SET:", h[:200])

def context(path, needle, before=600, after=900):
    blob = b''.join(b for _, b in chunks(path))
    for m in re.finditer(re.escape(needle), blob):
        s = blob[max(0, m.start()-before): m.end()+after].decode('latin1', 'replace')
        print("-----"); print(s)
