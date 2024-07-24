
# Still doesn't work. System might need to be initialised
# also, don't know where the PL/1 stack resides
todec = {
    "descr": "test TODEC function at address 06",
    "start": 0x0006,
    "data": [
        ["file", "roms/SN615_SN580/IC25_2708.bin",  0x0000],
        ["file", "roms/SN615_SN580/IC26_2708.bin",  0x0400],
        ["file", "roms/SN615_SN580/IC27_2708.bin",  0x0800],
        ["file", "roms/SN615_SN580/IC31_2708.bin",  0x1800],
        ["file", "roms/SN615_SN580/IC32_2708.bin",  0x1C00],
        ["snippet", [0x31, 0x32, 0x33, 0x34, 0x35], 0x5000],
        ["snippet", [5, 0x00, 0x50], 0x420D],
    ],
    "funcs" : [],
    "pois" : [],
}


dummy = {
    "descr": "Dummy program (three nops)",
    "start": 0x2000,
    "data": [
        ["snippet", [0x00, 0x00, 0x00], 0x2000]
    ],
    "funcs" : [],
    "pois" : [],
}

loop = {
    "descr": "Loop program (three nops, an inc, and loop to start)",
    "start": 0x2000,
    "data": [
        ["snippet", [0x00, 0x00, 0x00], 0x2000], # nop
        ["snippet", [0x3C], 0x2003],             # inc a
        ["snippet", [0xC3, 0x00, 0x20], 0x2004]  # jp 2000h
    ],
    "funcs" : [],
    "pois" : [],
}

emucrash = {
    "descr": "Emulator exception (ix)",
    "start": 0x2000,
    "data": [
        ["snippet", [0xDD, 0xBE, 0x0F], 0x2000], # nop
    ],
    "funcs" : [],
    "pois" : [],
}


test1 = {
    "descr": "Clarification",
    "start": 0x0000,
    "data": [
        ["snippet", [0x04, 0x04, 0xC5, 0xdd, 0xE1, 0x00, 0x00], 0x0000],
    ],
    "funcs" : [],
    "pois" : [],
}
