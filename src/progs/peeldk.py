

### From peel.dk
peeldk = {
    "descr": "Downloaded from peel.dk",
    "start": 0x0000,
    "data": [
        ["file", "roms/SN615_SN580/IC25_2708.bin", 0x0000],
        ["file", "roms/SN615_SN580/IC26_2708.bin", 0x0400],
        ["file", "roms/SN615_SN580/IC27_2708.bin", 0x0800],
        ["file", "roms/SN615_SN580/IC31_2708.bin", 0x1800],
        ["file", "roms/SN615_SN580/IC32_2708.bin", 0x1C00]
    ],
    "funcs" : [],
    "pois" : [],
    "known_ranges" : []
}

# I believe this is the code Karl Wacker is using
iws = {
    "descr": "Downloaded from peel.dk",
    "start": 0x0000,
    "data": [
        ["file", "roms/IWS_SN820/IC25_2708.bin", 0x0000],
        ["file", "roms/IWS_SN820/IC26_2708.bin", 0x0400],
        ["file", "roms/IWS_SN820/IC27_2708.bin", 0x0800],
        ["file", "roms/IWS_SN820/IC28_2708.bin", 0x0C00],
        ["file", "roms/IWS_SN820/IC29_2708.bin", 0x1000],
        ["file", "roms/IWS_SN820/IC31_2708.bin", 0x1800],
        ["file", "roms/IWS_SN820/IC32_2708.bin", 0x1C00]
    ],
    "funcs" : [],
    "pois" : {
        0x0000: 'reset START',
        0x0003: 'TOSTR',
        0x0006: 'TODEC',
        0x0009: 'UPDIS',
        0x000C: 'MUL',
        0x000F: 'DIV',
        0x0012: 'BICHAR',
        0x0015: 'NHL',
        0x0018: 'START',
        0x001B: 'KFILE',
        0x001E: 'KEYIN',
        0x0021: 'GETDN',
        0x0024: 'NKEY',
        0x0027: 'DISPLAY',
        0x002A: 'PRINTER',
        0x002D: 'CARB',
        0x0030: 'STOP',
        0x0033: 'PROCH',
        0x0036: 'INTRET',
        0x0039: 'INDEX',

        0x085e: 'call KEY[SEARCH]',
        0x0e58: 'key()'
        },
    "known_ranges" : [
        [0x0800, 0x0802, 'READ vec'],
        [0x0803, 0x0805, 'WRITE vec'],
        [0x0806, 0x0808, 'REWRITE vec'],
        [0x0809, 0x080b, 'KEY[SEARCH] vec'],
        [0x080c, 0x080e, 'OPEN vec'],
        [0x080f, 0x0811, 'LOADER vec'],
        [0x0812, 0x0814, 'CLOSE vec'],
        [0x0815, 0x0817, 'CLRDK vec'],
        [0x0818, 0x081a, 'REPORT vec'],
        [0x0830, 0x0930, 'open()']

    ]
}
