import os
import sys
import struct

def get_u32_le(buf, offset):
    return struct.unpack("<I", buf[offset:offset+4])[0]

def put_u32_le(buf, offset, n):
    buf[offset:offset+4] = struct.pack("<I", n)

extmap = {
    0x00000001: ".genh",   # ADPCM -> GENH / ".sdx_0"
    0x00000002: ".dmx",    # this container was found on Zone of the Enders HD Remaster
	0x00000003: ".nrm",
    0x00000004: ".pacb",   # has "PACB" magic not seen in any of the original versions the HD remaster was based on
    0x00000005: ".dmx",    # ditto
    0x00000006: ".bpx",    
    0x0000000c: ".pac",    # XBOX version of MGS2 - MPEG2 video format
    0x0000000d: ".pac",    # XBOX version of MGS2 - MPEG2 video format
	0x0000000e: ".pss",    # PS2 version of MGS2 - MPEG2 video format
	0x0000000f: ".ipu",    # PS2 version of MGS2 - MPEG2 video format
    0x00000020: ".m2v",    # this container is present even on all versions of the HD remaster(PS3, XBOX360, PSVITA), regardless of format
    0x00010001: ".sdx_1",
	0x00010004: ".sub_en", # it's a made-up container, becuase in the executable of those Metal Gear Solid PS2 games there's no indication of a container used for these formats
    0x00020001: ".sdx_2",
	0x00020004: ".sub_fr", # ditto
    0x00030001: ".msf",    # PS3 HD remaster audio format
	0x00030004: ".sub_de", # ditto
	0x00040001: ".xwma",   # XBOX360 HD remaster audio format
	0x00040004: ".sub_it", # ditto
	0x00050001: ".9tav",   # PSVITA HD remaster audio format
	0x00050004: ".sub_es", # ditto
	0x00060004: ".sub_jp", # ditto
	0x00070004: ".sub_jp", # ditto
    0x00100001: ".vag",    # VAG1/VAG2 format
    0x00110001: ".mtaf",   # MTAF format

    #0x00000002: ".xxxx",
    #0x00000005: ".xxxx",
    #0x00010006: ".xxxx",
    #0x00020006: ".xxxx",
    #0x00030006: ".xxxx",
    #0x00040006: ".xxxx",
    #0x00050006: ".xxxx",
    #0x00070006: ".xxxx",
}

STREAM_ID_ADPCM = 1

streams = {
}

def main(argv=sys.argv, argc=len(sys.argv)):
    if argc != 2:
        print("Usage: %s <sdt>" % argv[0])
        return 1

    sdt_path = os.path.realpath(argv[1])

    if not os.path.isfile(sdt_path):
        print("invalid path")
        return 1

    with open(sdt_path, "rb") as sdt:
        sdt_size = os.path.getsize(sdt_path)
        while (sdt.tell() < sdt_size):
            header = sdt.read(16)
            id = get_u32_le(header, 0x00)
            if id == 0xF0:
                # end
                break
            elif id == 0x10:
                # register stream
                sid = get_u32_le(header, 0x0C)

                if sid in streams:
                    print("0x%08X: stream already registered once: %08X" % (sdt.tell() - 16, sid))
                    return 1

                if sid in extmap:
                    path = "%s%s" % (os.path.splitext(sdt_path)[0], extmap[sid])
                else:
                    path = "%s_%08X.bin" % (os.path.splitext(sdt_path)[0], sid)

                streams[sid] = open(path, "w+b")

                if sid == STREAM_ID_ADPCM:
                    # reserve space for GENH header
                    streams[sid].write(b"\0" * 4096)
            elif id in streams:
                size = get_u32_le(header, 0x04) - 16
                streams[id].write( sdt.read(size) )
            else:
                print("0x%08X: unregistered stream / unknown header ID: %08X" % (sdt.tell() - 16, id))
                return 1

    # finalize GENH
    if STREAM_ID_ADPCM in streams:
        genh_size = streams[STREAM_ID_ADPCM].tell()

        # get proprietary header data
        streams[STREAM_ID_ADPCM].seek(4096)
        header = streams[STREAM_ID_ADPCM].read(16)
        sample_rate = (header[0x06] << 8) | header[0x07]
        channels = header[8]

        # fill in GENH header
        streams[STREAM_ID_ADPCM].seek(0)
        genh = bytearray(4096)
        genh[0x00:0x04] = b"GENH"                                               # 0x00 magic
        put_u32_le(genh, 0x04, channels)                                        # 0x04 channels
        put_u32_le(genh, 0x08, 2048 if channels > 1 else 0)                     # 0x08 interleave
        put_u32_le(genh, 0x0C, sample_rate)                                     # 0x0C sample rate
        put_u32_le(genh, 0x10, 0xFFFFFFFF)                                      # 0x10 loop start
        put_u32_le(genh, 0x14, (genh_size - 0x1010) // 16 * 28 // channels)     # 0x14 loop end
        put_u32_le(genh, 0x18, 0)                                               # 0x18 coding
        put_u32_le(genh, 0x1C, 0x1010)                                          # 0x1C audio start
        put_u32_le(genh, 0x20, 0x1000)                                          # 0x20 header size
        streams[STREAM_ID_ADPCM].write(genh)

    # clean up
    for stream in streams:
        streams[stream].close()

    return 0

if __name__ == "__main__":
    main()
