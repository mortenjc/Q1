# New abstraction to make it possible to load different roms and/or
# custom code snippets into memory with a user defined start address

q1_full = {
    "descr": "Combined Q1 image from IC25-IC32",
    "start": 0x0000,
    "data": [
        ["file", "roms/IC25.bin", 0x0000],
        ["file", "roms/IC26.bin", 0x0400],
        ["file", "roms/IC27.bin", 0x0800],
        ["file", "roms/IC28.bin", 0x0C00],
        ["file", "roms/IC29.bin", 0x1000],
        ["file", "roms/IC30.bin", 0x1400],
        ["file", "roms/IC31.bin", 0x1800],
        ["file", "roms/IC32.bin", 0x1C00]
    ]
}

q1_small = {
    "descr": "Minimal images to finish boot (IC25-IC28)",
    "start": 0x0000,
    "data": [
        ["file", "roms/IC25.bin", 0x0000],
        ["file", "roms/IC26.bin", 0x0400],
        ["file", "roms/IC27.bin", 0x0800],
        ["file", "roms/IC28.bin", 0x0C00]
    ]
}


dummy = {
    "descr": "Dummy program (three nops)",
    "start": 0x2000,
    "data": [
        ["snippet", [0x00, 0x00, 0x00], 0x2000]
    ]
}

loop = {
    "descr": "Loop program (three nops and loop back)",
    "start": 0x2000,
    "data": [
        ["snippet", [0x00, 0x00, 0x00], 0x2000],
        ["snippet", [0xC3, 0x00, 0x20], 0x2003]
    ]
}


proglist = {
        "q1_full"  : q1_full,
        "q1_small" : q1_small,
        "dummy"    : dummy,
        "loop"    : loop
    }
