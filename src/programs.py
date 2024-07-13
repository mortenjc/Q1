# New abstraction to make it possible to load different roms and/or
# custom code snippets into memory with a user defined start address


### From peel.dk
peeldk1 = {
    "descr": "Downloaded from peel.dk",
    "start": 0x0000,
    "data": [
        ["file", "roms/SN615_SN580/IC25_2708.bin", 0x0000],
        ["file", "roms/SN615_SN580/IC26_2708.bin", 0x0400],
        ["file", "roms/SN615_SN580/IC27_2708.bin", 0x0800],
        ["file", "roms/SN615_SN580/IC31_2708.bin", 0x1800],
        ["file", "roms/SN615_SN580/IC32_2708.bin", 0x1C00]
    ]
}

todec = {
    "descr": "test TODEC function at address 06",
    "start": 0x0006,
    "data": [
        ["file", "roms/SN615_SN580/IC25_2708.bin", 0x0000],
        ["file", "roms/SN615_SN580/IC26_2708.bin", 0x0400],
        ["file", "roms/SN615_SN580/IC27_2708.bin", 0x0800],
        ["file", "roms/SN615_SN580/IC31_2708.bin", 0x1800],
        ["file", "roms/SN615_SN580/IC32_2708.bin", 0x1C00],
        ["snippet", [0x31, 0x32, 0x33, 0x34, 0x35], 0x5000],
        ["snippet", [5, 0x00, 0x40], 0x3ffd],
    ]
}


### From (currently) unknown source

jdc_full = {
    "descr": "Combined Q1 image from IC25-IC32",
    "start": 0x0000,
    "data": [
        ["file", "roms/JDC/IC25.bin", 0x0000],
        ["file", "roms/JDC/IC26.bin", 0x0400],
        ["file", "roms/JDC/IC27.bin", 0x0800],
        ["file", "roms/JDC/IC28.bin", 0x0C00],
        ["file", "roms/JDC/IC29.bin", 0x1000],
        ["file", "roms/JDC/IC30.bin", 0x1400],
        ["file", "roms/JDC/IC31.bin", 0x1800],
        ["file", "roms/JDC/IC32.bin", 0x1C00]
    ]
}

jdc_small = {
    "descr": "Minimal images to finish boot (IC25-IC28)",
    "start": 0x0000,
    "data": [
        ["file", "roms/JDC/IC25.bin", 0x0000],
        ["file", "roms/JDC/IC26.bin", 0x0400],
        ["file", "roms/JDC/IC27.bin", 0x0800],
        ["file", "roms/JDC/IC28.bin", 0x0C00]
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
        ["snippet", [0x00, 0x00, 0x00], 0x2000], # nop
        ["snippet", [0x3C], 0x2003],             # inc a
        ["snippet", [0xC3, 0x00, 0x20], 0x2004]  # jp 2000h
    ]
}

emucrash = {
    "descr": "Emulator exception (ix)",
    "start": 0x2000,
    "data": [
        ["snippet", [0xDD, 0xBE, 0x0F], 0x2000], # nop
    ]
}


proglist = {
        "peeldk1"   : peeldk1,
        "jdc_full"  : jdc_full,
        "jdc_small" : jdc_small,
        "dummy"     : dummy,
        "loop"      : loop,
        "todec"     : todec,
        "emucrash"     : emucrash
    }
