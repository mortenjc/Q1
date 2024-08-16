
### From https://datamuseum.dk/wiki/Bits:Keyword/COMPANY/JDC/Q1
# funcs, pois and known_ranges are the result of reverse engineering
# and emulation efforts

jdc = {
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
        # ["snippet", [0xff], 0x1000] # force different disk access path
    ],
    "funcs" : {
       0x0000: "jump to START",
       0x0038: "interrupt - jp 0x52",
       0x0052: "interrupt - jp 0x01de" ,
       0x01de: "interrupt routine()",
       0x01e5: "START()",
       0x01eb: "01eb setup registers for copying and clearing",
       0x01f3: "01f3 copy (function calls) from 0x003f:0x0047 to 0x4080:",
       0x01f8: "01f8 clear RAM from 4089 to 40ff",
       0x02b1: "02b1 interrupt3 ROM()",
       0x0410: "0410 write 0x20 from 4100 to 417f",
       0x04a9: "04a9 unknown_io()",
       0x04d1: "04d1 wait_for_key_0x0e()",
       0x0809: "KEY: A=key len, BC=fd address, DE=key pos in fd, HL=key address",
       0x0fb8: "0fb8 check_#_disk_selected()",
       0x4083: "4083 interrupt RAM()",
       0x4086: "4086 wait_for_kbd_or_printer()"
    },
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
        0x003C: 'SHIFTY',
        0x01e7: 'set keyboard mode 2 (ASM IO page 73)',
        0x01eb: 'prepare registers for copy and clearing' ,
        0x01f6: 'copy jump tables from 003f:0047 to 4080:4088',
        0x01fb: 'clear RAM from 4089 to 40ff',
        0x01fd: 'printer control - reset printer, raise ribbon',
        0x0201: 'printer status  - check result (0 is good)',
        0x020c: 'clear keyboard buffer, update display',
        0x020f: 'reset stack pointer to x4080',
        0x0213: 'CLRDK',
        0x021f: 'a = PLC (lsb of addr of last char loaded to printer buffer)',
        0x0221: 'ensure there are no buffered chars to print???',
        0x0224: 'UNKNOWN INPUT from 0xc',
        0x0226: 'check bit 6 - unknown',
        0x022f: 'UNKNOWN OUTPUT to 0xc',
        0x0231: 'clear display',
        0x0234: 'Get status for disk 2',
        0x0237: 'disk status == 0 -> Q1-Lite',
        0x0239: 'else if bit 3 (0x8) clear -> Q1-Magnus',
        0x023d: 'HL -> " Q1-Magnus klar til brug"',
        0x0244: 'HL -> " Q1-Lite"',
        0x0249: 'get display width',
        0x0252: '???',
        0x0258: 'print " Q1-Magnus/Lite"',
        0x0260: 'print " Klar til brug"',
        0x0264: 'get display status',
        0x0266: 'check if 40 or 80 bytes',
        0x0273: 'get keyboard input (returns when command is entered)',
        0x0276: 'clear display',
        0x0279: 'set return to Main loop',
        0x027f: 'LOADER',
        0x0282: 'USE OF FIELD REPORTED AS UNUSED',
        0x0287: 'jump to loaded program start???',
        0x028d: 'clear keyboard buffer, update display',
        0x028a: 'REPORT',
        0x0290: 'back to Main loop',
        0x0293: 'String "Q1 Lite"',
        0x0299: 'display(SPC)',
        0x02a4: '80 characters',
        0x02ab: '40 characters',
        0x037b: 'move printer carriage',
        0x0394: 'test for out of ribbon',
        0x039e: 'display PRINTER FAULT',
        0x03d5: 'check printer status',
        0x03d7: 'clear keyboard buffer, update display',
        0x03ea: 'ignore leading spaces (0x20)',
        0x03da: 'get keyboard input, result in a',
        0x03f0: 'update TOOK',
        0x041e: 'UNDER = 0x20 (character under curser)',
        0x0421: 'update display',
        0x0424: 'a = 0',
        0x0425: 'TOOK = 0 (chars used for keyboard)',
        0x0428: 'KSIZ = 0',
        0x042b: 'CURSE = 0',
        0x042e: 'ATCK = 0 (keyboard line open)',
        0x0431: 'HEXX = 0',
        0x0434: 'INSF = 0 (insert mode off)',
        0x0439: 'de <- #characters used for display',
        0x043F: 'display ctrl (0x05) Reset, Unbuffer',
        0x04d3: 'key: GO',
        0x04dc: 'key: STOP',
        0x04fe: 'key: CLEAR ENTRY',
        0x0560: 'z80 otir instruction - B bytes from HL to port C',
        0x0548: 'ATCK',
        0x054b: 'FUNKEY',
        0x0559: 'KSIZ',
        0x0503: 'key: INSERT MODE',
        0x0508: 'key: DEL CHAR',
        0x050d: 'key: REV TAB',
        0x0512: 'key: TAB',
        0x0517: 'key: 0x1a undocumented',
        0x051c: 'key: CORR',
        0x052b: 'key: CHAR ADV',
        0x0534: 'key: CLEAR ENTRY',
        0x0538: 'key: 0x08 undocumented',
        0x053e: 'key: TAB SET',
        0x0563: 'key: TAB CLR',
        0x056e: 'HEXX',
        0x0576: 'INSF',
        0x058c: 'CURSE (cursor position)',
        0x0597: 'update display',
        0x05bb: 'hl = tab positions',
        0x05d4: 'hl = INSF',
        0x0600: 'done - update cursor position and current size of line',
        0x0698: 'call divide() hl/10',
        0x0845: 'get disk# from index file',
        0x0775: 'call getkey?',
        0x0780: 'unknown input (0xc undocumented, rs232?)',

        0x080f: 'jump to loader()',
        0x083d: 'a = bit mask of allowed drives',
        0x0843: 'get next potential disk',
        0x0849: 'is disk available?',
        0x0851: 'Current record number on index?',
        0x0854: 'setup FD for INDEX (rpt, #records, record size)',
        0x085e: 'call KEY[SEARCH]',
        0x0869: 'call READ',
        0x086c: 'get disk# from index file',
        0x0870: 'THERE (address of file transfer)',
        0x08df: 'is Data record?',
        0x08dd: 'read byte from disk 2',
        0x08ee: 'read byte from disk 2',
        0x08f4: 'read byte from disk 2',
        0x0903: 'read byte from disk 2',
        0x0936: 'increment Record Number (LO)',
        0x093b: 'increment Record Number (HI)',
        0x0d1e: 'loader() - hl = FD for loaded file',
        0x0d21: 'call OPEN',
        0x0d2f: 'hl = Record #',
        0x0d3f: 'Read 1 record',
        0x0d41: 'call READ',
        0x0d74: 'check if "IWS" version',
        0x0d7b: 'call IWS specific code',
        0x0d90: 'clrdk()',
        0x0d98: 'print "CR?"',
        0x0d9c: '0x4 = Key not found',
        0x0da7: 'Start of error messages',
        0x0dab: 'Message separators have Bit 7 set',
        0x0db5: 'print:  "NOT FOUND"',
        0x0dba: 'string: " ON "',
        0x0dbd: 'print:  " ON"',
        0x0dc5: 'print:  "INDEX"',
        0x0dc8: 'STOP',
        0x0ddd: 'A=4 - fourth err msg: "NOT FOUND"',
        0x0fc4: 'deselect disks',
        0x0fcb: 'jump to 0xfda if no ROM in addr 0x1000',
        0x0fce: 'a = Disk #',
        0x0fd4: 'max disk # reached ?',
        0x0fd9: 'no, return ok?',
        0x0fea: '# records = 0x58 (88)',
        0x0fef: 'Records per Track = 0x82 (130)',
        0x0ff8: 'Record Length = 0x28 (24)',
        0x1094: 'set ERC (error count) to 32',
        0x1103: 'is end of record?',
        0x112d: 'jump to return of (unknown) disk function',
        0x11bf: 'write Data Record identifier 0x9b',
        0x11c5: 'write (hl+i) to disk, i = 0 to b ',
        0x11cb: 'write (hl+i) to disk, i = 0 to b ',
        0x11d2: 'write checksum',
        0x11dc: 'write end of record terminator 0x10',
        0x12c1: 'bc = record length',
        0x12e6: 'Store INDEX (curr rec no on index)',
        0x12e9: 'get l = disk# on INDEX',
        0x1303: 'select disk',
        0x130b: 'drive 1, track# = 255',
        0x130e: 'Skip 143 bytes (track 0)',
        0x1313: 'Skip 1023 bytes (track 0)',
        0x1316: 'Skip 1023 bytes (track 0)',
        0x1319: 'get disk status',
        0x131b: 'check if disk is ready',
        0x131d: 'goto error return',
        0x1320: 'return OK',
        0x1324: 'return error # 5 (inferred)',
        0x1325: 'rec before last',
        0x132e: 'set current record number on INDEX',
        0x1344: 'copy record number (hi+lo) to last reordnumber on INDEX FD',
        0x1351: 'get a = current record # on INDEX (LO)',
        0x1354: 'compare with same (LO) on INDEX FD',
        0x135a: 'compare with same (HI) on INDEX FD',
        0x1368: 'test for disk ready h*l times (0x27 * 0x10)',
        0x1381: 'drive was not ready for a while',
        0x1382: 'read byte (ID record)',
        0x1384: 'check if ID record (0x9e)',
        0x1389: 'get b = Track',
        0x138b: 'get c = Sector',
        0x138d: 'get a = check sum',
        0x1391: 'bad cksum, find next ID record',
        0x1397: 'store track# for current record',
        0x1393: 'ID Record, read with good cksum',
        0x1399: 'Track # for drive 1',
        0x139e: 'check for ?? end of tracks or not index track',
        0x13d2: 'skip 23 bytes',
        0x13dd: 'step direction UP',
        0x13e8: 'check if at Track 0',
        0x13ec: 'Track step bit',
        0x13f4: 'Skip 191 bytes',
        0x13fb: 'Double density?',
        0x13ff: 'Skip 307 bytes',
        0x13ce: 'select drive (and side)',
        0x140c: 'step to next track',
        0x140e: 'read byte from disk',
        0x1411: 'read byte from disk',
        0x1414: 'read byte from disk',
        0x1417: 'read byte from disk',
        0x1421: 'record number (HI) from INDEX FD',
        0x1424: 'record number (LO) from INDEX FD',
        0x142a: 'first track (HI) ?',
        0x141e: 'set ERC to 10',
        0x1446: 'Skip 279 bytes',
        0x145a: 'Data Record (0x9b)',
        0x1461: 'No Data Record found after 128 reads',
        0x146a: 'get disk status',
        0x146c: 'track 0 selected',
        0x1476: 'Track/Record',
        0x1482: 'get disk status',
        0x1489: 'read byte (ID record) from disk',
        0x148b: 'check if ID record (0x9e)',
        0x148f: 'read byte (TRACK#)    from disk',
        0x1494: 'read byte (SECTOR#)   from disk',
        0x1499: 'read byte (CHECK SUM) from disk',
        0x149d: 'return if checksum good',
        0X14a4: 'return error code 1?',
        0x14a9: 'read byte from disk',
        0x14ac: 'read byte from disk',
        0x14b3: 'checksum good if a = 0',
        0x14b7: 'end of record marker',
        0x15c5: 'error text "FORMAT ERR"',
        0x15d8: 'error text "ON"',
        0x15d3: 'call DISPLAY',
        0x15db: 'call DISPLAY',
        0x15e3: 'call DISPLAY',
        0x15ec: 'call STOP',
        0x15fe: 'call DISPLAY',
        0x1676: 'get a = # of records HI',
        0x1679: 'get a = # of records LO',
        0x1688: 'checksum on FILE FD?',
        0x1690: 'checksum on filename (increment)',
        0x1697: 'record len on INDEX FD (HI)',
        0x169c: 'record len on INDEX FD (LO)',
        0x16e7: 'hl = current record number',
        0x172e: 'hl = addr of ERC (disk error count)',
        0x1755: 'filename match on record',
        0x1779: 'checksum good on data record',
        0x177b: 'end-of-record marker',
        0x1800: 'PL/1 AAAA',
        0x1803: 'PL/1 return from subroutine?',
        0x1806: 'PL/1 CCCC',
        0x1809: 'PL/1 RUN Microcode Program',
        0x187c: 'Interpretive Program Counter',
        0x187f: 'get instruction (or data)',
        0x1882: 'jump if a > 63 (is address?)',
        0x1890: 'a = (0x18xx) xx = 2*a + 12; ex. instr 0xa is at 0x1820 -> jp 0x18a5',
        0x1894: 'jump to instruction code',
        0x1895: 'get original value of a',
        0x1896: 'get next byte of address',
        0x1899: 'push address on stack',
        0x189a: 'get next instr or address',
        0x189d: 'INST 00 - stack number from address on stack',
        0x18a5: 'INST 0A - add',
        0x18ac: 'INST 03 - store binary number at stack address',
        0x18b4: 'INST 0C - replace binary number with negation',
        0x18b5: 'call NhL routine',
        0x18bb: 'INST 0E - multiply binary',
        0x18bd: 'call MUL routine',
        0x18c5: 'call DIV routine',
        0x18cc: 'INST 15 - PUT data to specified device driver',
        0x18d0: 'increment IPC',
        0x18d3: 'Output routine for PUT',
        0x18f5: 'call TOSTR routine',
        0x1938: 'INST 1F - return from subroutine',
        0x1939: 'call GETDN routine',
        0x194a: 'INST 23 - get new line of keyboard input',
        0x1958: 'call TOSTR',
        0x1992: 'INST 06 - store a string of bytes',
        0x1aea: 'call CARB (ch to binary)',
        0x1b05: 'call BICHAR',
        0x1b0a: 'call TOSTR',
        0x1b24: 'call TODEC',
        0x1b45: 'call NHL (negate binary in hl)',
        0x1b5b: 'call KEY[SEARCH]',
        0x1b71: 'call READ',
        0x1b77: 'increment IPC',
        0x1b7e: 'call READ',
        0x1b81: 'set ONCODE = a',
        0x1ba0: 'run loaded program!',
        0x1ba3: 'call (error) REPORT',
        0x1baf: 'INST 2C - write on disk',
        0x1bb6: 'call WRITE',
        0x1bbc: 'INST 2D - rewrite on disk',
        0x1bc3: 'call REWRITE',
        0x1bca: 'call OPEN',
        0x1bdd: 'INST 08 - compare decimal',
        0x1bc9: 'INST 22 - open file',
        0x1c12: 'INST 09 - compare character strings',
        0x1c37: 'INST 07 - compare binary numbers',
        0x1c4d: 'INST 0B - add decimal',
        0x1cfb: 'INST 01 - stack float from address on stack',
        0x1cfc: 'push 8 0x00 on stack (subroutine?)',
        0x1d03: 'increment IPC',
        0x1d15: 'INST 04 - store float',
        0x1d2b: 'hl = IPC addr',
        0x1d3c: 'run microcode program',
        0x1d78: 'INST 05 - store decimal number as fixed point',
        0x1dbe: 'INST 0D - negate decimal?',
        0x1dcb: 'INST 02 - stack dec num from address on stack',
        0x1df5: 'call aaaa()',
        0x1df8: 'run microcode program',
        0x1eb3: 'INST 0F - multiply decimal',
        0x1fcc: 'run microcode program',
        0x1fd8: 'run microcode program',
        0x1fe4: 'run microcode program',
        0x1ff8: 'jump via 0x4f to 0x734',
        0x1ffc: 'run microcode program'


    },
    "known_ranges" : [
        [0x0000, 0x003e, 'jump tables'],
        [0x003f, 0x0041, 'Return Address (copied to 4080)'],
        [0x0042, 0x0044, 'JP to interrupt routine (copied to 4083)'],
        [0x0045, 0x0047, 'JP to wait-for-keyboard-or-printer'],

        [0x0052, 0x0054, 'interrupt38 chain'],

        [0x01de, 0x01e4, 'interrupt routine()'],
        [0x01e5, 0x020e, 'start()'],
        [0x020f, 0x0278, 'Main program loop'],
        [0x0279, 0x0292, 'load and run program'],
        [0x0293, 0x029f, 'print "Q1 Lite/Magnus ..."'],
        [0x02a0, 0x02b0, 'Display width?'],
        [0x02b1, 0x0367, 'interrupt processing routine()'],
        [0x0368, 0x0380, 'unknown'],
        [0x0381, 0x038e, 'text string - CLR, PRINTER FAULT'],
        [0x038f, 0x03cb, 'check printer status'],
        [0x03cd, 0x03d4, 'unknown'],
        [0x03d5, 0x0409, 'unknown'],
        [0x0410, 0x0438, 'clear keyboard buffer, update display'],
        [0x0439, 0x044d, 'XXX'],
        [0x044e, 0x0457, 'print A, E times (entry 0x450)'],
        [0x0458, 0x047c, 'display() - string=HL, len=C'],
        [0x047d, 0x04a8, 'unkown'],
        [0x04a9, 0x04b2, 'wait for keyboard'],
        [0x04B3, 0x04CA, 'clear display?'],
        [0x04CB, 0x04D0, 'disable interrupt, get key?, enable interrupt'],
        [0x04D1, 0x04D7, 'STOP, wait for key GO (0xe)'],
        [0x04D8, 0x0547, 'read_key()'],
        [0x0548, 0x0552, 'unknown'],
        [0x0553, 0x0562, 'updis() - called after printing line?'],
        [0x0563, 0x056d, 'handle tab clear (clears tab bit in hl?)'],
        [0x056e, 0x0587, 'unknown HEXX function?'],
        [0x0588, 0x0598, 'update cursor position and current size of line'],
        [0x0599, 0x05a7, 'unknown (on key 0x9a?)'],
        [0x05b5, 0x05cd, 'get tab position bit??'],
        [0x05ce, 0x05d3, 'something with HEX last key'],
        [0x05d4, 0x05d9, 'Toggle INSERT mode (on key 0x1e)'],
        [0x05da, 0x05e6, 'tab()'],
        [0x05e7, 0x05e8, 'unknown'],
        [0x05e9, 0x05f5, 'rev_tab()'],
        [0x05f6, 0x0606, 'del_char()'],
        [0x0607, 0x062a, 'hexx_input()?'],
        [0x062b, 0x0641, 'UNEXPLORED'],
        [0x0642, 0x0651, 'multiply() = de * bc'],
        [0x0652, 0x0689, 'divide() = hl / de'],
        [0x068a, 0x06b0, 'bin_to_string()'],
        [0x06b1, 0x0733, 'UNEXPLORED'],
        [0x0734, 0x0766, 'UNEXPLORED'],
        [0x0767, 0x0774, 'called from x003c (nibbl rotation?)'],
        [0x0775, 0x07ff, 'UNEXPLORED'],
        [0x0800, 0x0802, 'READ vec'],
        [0x0803, 0x0805, 'WRITE vec'],
        [0x0806, 0x0808, 'REWRITE vec'],
        [0x0809, 0x080b, 'KEY[SEARCH] vec'],
        [0x080c, 0x080e, 'OPEN vec'],
        [0x080f, 0x0811, 'LOADER vec'],
        [0x0812, 0x0814, 'CLOSE vec'],
        [0x0815, 0x0817, 'CLRDK vec'],
        [0x0818, 0x081a, 'REPORT vec'],
        [0x081b, 0x082f, 'unknown jump vectors'],
        [0x0830, 0x088d, 'open()'],
        [0x088e, 0x0949, 'read()'],
        [0x094a, 0x0974, 'write jump()'],
        [0x0975, 0x0b3a, 'rewrite()'],
        [0x0b3b, 0x0d1d, 'UNEXPLORED'],
        [0x0d1e, 0x0d6a, 'loader()'],
        [0x0d6b, 0x0d7d, 'clrdk() '],
        [0x0d7e, 0x0d8a, 'deselect all disks()'],
        [0x0d8b, 0x0d8d, 'text string? - IWS'],
        [0x0d8e, 0x0da6, 'report()'],
        [0x0da7, 0x0de0, 'print nth error message'],
        [0x0de1, 0x0e4e, 'text strings - INDEX .. WEIRD ERR'],
        [0x0e4f, 0x0fb7, 'key search()'],
        [0x0fb8, 0x0fe0, 'write()'],
        [0x0fe1, 0x0fff, 'Setup disk: Records:88, Rec per Track: 130, Rec len 24 bytes'],

        # 1000 - 17ff marked as unused in ROS Manual!
        [0x1000, 0x1002, 'UNEXPLORED'],
        [0x1003, 0x1005, 'write?'],
        [0x1006, 0x1008, 'UNEXPLORED'],
        [0x1009, 0x100b, 'key search jump vector'],
        [0x100c, 0x1014, 'UNEXPLORED'],
        [0x1015, 0x112e, 'unknown IWS code jump vector'],
        [0x112f, 0x113e, 'increment current record number (and return)'],
        [0x113f, 0x1143, 'return from (unknown) disk function'],
        [0x1144, 0x1284, 'write??'],
        [0x1285, 0x12c0, 'unknown (disk?) function'],
        [0x12c1, 0x12dd, 'Set PART1 and PART2'],
        [0x12de, 0x1324, 'Select disk, wait for drive/data ready'],
        [0x1325, 0x1343, 'Copy rec before last to ROS INDEX'],
        [0x1344, 0x1350, 'Adjust last record number???'],
        [0x1351, 0x1364, 'Compare ROS INDEX with INDEX FD???'],
        [0x1365, 0x140d, 'Search for valid ID Record'],
        [0x140e, 0x141a, 'skip 4*l + 3 bytes'],
        [0x141b, 0x1474, 'UNEXPLORED'],
        [0x1475, 0x147b, 'UNEXPLORED'],
        [0x147c, 0x14a7, 'search for INDEX file?'],
        [0x14a8, 0x1569, 'UNEXPLORED'],
        [0x156a, 0x158d, 'unknown IWS function i'],
        [0x158e, 0x1593, 'UNEXPLORED'],
        [0x1594, 0x15ab, 'unknown IWS function ii'],
        [0x15ac, 0x1604, 'unknown IWS functions'],
        [0x1605, 0x166a, 'ASCI CHARS ERROR MESSAGES'],
        [0x166b, 0x17ff, 'KEY ()?'],

        [0x1800, 0x180b, 'PL/1 jump vectors'],
        [0x180c, 0x1877, 'PL/1 instruction vectors'],
        [0x1878, 0x187b, 'return from subrouine?'],
        [0x187c, 0x1b80, 'run microcode program'],
        [0x1b81, 0x1ba2, 'return from file operations'],
        [0x1ba3, 0x1ccd, 'UNEXPLORED'],
        [0x1cce, 0x1d2a, 'aaaa()'],
        [0x1d2b, 0x1d33, 'increment IPC value'],
        [0x1d34, 0x1f52, 'UNEXPLORED'],
        [0x1f53, 0x1f61, 'cccc() - clear 16 bytes in scratch'],
        [0x1f62, 0x1fff, 'UNEXPLORED'],


    ]
}


psmcadd = {
    "descr": "first test of PL/1 program (add)",
    "start": 0x6000,
    "data": [
            ["file", "roms/JDC/full.bin", 0x0000],
            # PL/1 Interpretive Program Counter
            ["snippet", [0x00, 0x80],        0x40fe], # set IPC = x8000
            # Setup two numbers to be added, run PL/1 program
            ["snippet", [0x00],              0x6000], # nop (for trace)
            ["snippet", [0x21, 0x80, 0x40],  0x6001], # hl = 4080
            ["snippet", [0xf9],              0x6004], # SP = 4080
            ["snippet", [0x21, 0x10, 0x00],  0x6005], # hl = 0010
            ["snippet", [0xe5],              0x6008], # push hl
            ["snippet", [0x21, 0x20, 0x00],  0x6009], # hl = 0020
            ["snippet", [0xe5],              0x600c], # push hl
            ["snippet", [0xc3, 0x7c, 0x18],  0x600d], # run PL/1 program
            # PL/1 program
            ["snippet", [0x0a],              0x8000], # add two numbers
            ["snippet", [0x14],              0x8001], # one's compl
            ["snippet", [0x1f],              0x8002]  # return
    ],
    "funcs" : [],
    "pois" : {}
}

psmcmul = {
    "descr": "Q1 pseudo machine code program (multiply)",
    "start": 0x6000,
    "data": [
            ["file", "roms/JDC/full.bin", 0x0000],
            # PL/1 Interpretive Program Counter
            ["snippet", [0x00, 0x80],        0x40fe], # set IPC = x8000
            # Setup two numbers to be added, run PL/1 program
            ["snippet", [0x00],              0x6000], # nop (for trace)
            ["snippet", [0x21, 0x80, 0x40],  0x6001], # hl = 4080h
            ["snippet", [0xf9],              0x6004], # SP = 4080h
            ["snippet", [0x21, 0x01, 0x01],  0x6005], # hl = 257 (dec)
            ["snippet", [0xe5],              0x6008], # push hl
            ["snippet", [0x21, 0xff, 0x00],  0x6009], # hl = 255 (dec)
            ["snippet", [0xe5],              0x600c], # push hl
            ["snippet", [0xc3, 0x7c, 0x18],  0x600d], # run program
            # 'PL/1' program
            ["snippet", [0x0e],              0x8000], # multiply
            ["snippet", [0x1f],              0x8001]  # return
    ],
    "funcs" : [],
    "pois" : {}
}


psmcdiv = {
    "descr": "Q1 pseudo machine code program (divide)",
    "start": 0x6000,
    "data": [
            ["file", "roms/JDC/full.bin", 0x0000],
            # PL/1 Interpretive Program Counter
            ["snippet", [0x00, 0x80],        0x40fe], # set IPC = x8000
            # Setup two numbers to be added, run PL/1 program
            ["snippet", [0x00],              0x6000], # nop (for trace)
            ["snippet", [0x21, 0x80, 0x40],  0x6001], # hl = 0x4080
            ["snippet", [0xf9],              0x6004], # SP = 0x4080
            ["snippet", [0x21, 0xfd, 0x7f],  0x6005], # hl = 0x7fff
            ["snippet", [0xe5],              0x6008], # push hl
            ["snippet", [0x21, 0x99, 0x19],  0x6009], # hl = 0x1999
            ["snippet", [0xe5],              0x600c], # push hl
            ["snippet", [0xc3, 0x7c, 0x18],  0x600d], # run program
            # 'PL/1' program
            ["snippet", [0x10],              0x8000], # divide
            ["snippet", [0x1f],              0x8001]  # return
    ],
    "funcs" : [],
    "pois" : {}
}


psmcb2ch = {
    "descr": "Q1 pseudo machine code program (bin to char)",
    "start": 0x6000,
    "stop" : 0x1938,
    "data": [
            ["file", "roms/JDC/full.bin", 0x0000],
            # PL/1 Interpretive Program Counter
            ["snippet", [0x00, 0x80],        0x40fe], # set IPC = x8000
            # Setup two numbers to be added, run PL/1 program
            ["snippet", [0x00],              0x6000], # nop (for trace)
            ["snippet", [0x21, 0x80, 0x40],  0x6001], # hl = 0x4080
            ["snippet", [0xf9],              0x6004], # SP = 0x4080
            ["snippet", [0x21, 0xab, 0xcd],  0x6005], # hl = 0xabcd, unused
            ["snippet", [0xe5],              0x6008], # push hl
            ["snippet", [0x21, 0xff, 0x7f],  0x6009], # hl = 0x7fff (32767)
            ["snippet", [0xe5],              0x600c], # push hl
            ["snippet", [0xc3, 0x7c, 0x18],  0x600d], # run program
            # 'PL/1' program
            ["snippet", [0x19],              0x8000], # bin to character
            ["snippet", [0x1f],              0x8001]  # return
    ],
    "funcs" : [],
    "pois" : {}
}


psmcb2dec = {
    "descr": "Q1 pseudo machine code program (bin to decimal)",
    "start": 0x6000,
    "stop" : 0x1938,
    "data": [
            ["file", "roms/JDC/full.bin", 0x0000],
            # jump calls
            ["snippet",[0xc3, 0x0f, 0x02, 0xc3, 0xfd, 0x07, 0xc3, 0x15, 0x08], 0x4080],
            # PL/1 Interpretive Program Counter
            ["snippet", [0x00, 0x80],        0x40fe], # set IPC = x8000
            # Setup two numbers to be added, run PL/1 program
            ["snippet", [0x00],              0x6000], # nop (for trace)
            ["snippet", [0x21, 0x80, 0x40],  0x6001], # hl = 0x4080
            ["snippet", [0xf9],              0x6004], # SP = 0x4080
            ["snippet", [0x21, 0xff, 0x01],  0x6005], # hl = 0x01ff (to char)
            ["snippet", [0xe5],              0x6008], # push hl
            ["snippet", [0x21, 0x0b, 0x00],  0x6009], # hl = 0x000b unused?
            ["snippet", [0xe5],              0x600c], # push hl
            ["snippet", [0x21, 0x0c, 0x00],  0x600d], # hl = 0x000c unused?
            ["snippet", [0xe5],              0x6010], # push hl
            ["snippet", [0x21, 0x0d, 0x00],  0x6011], # hl = 0x000d unused?
            ["snippet", [0xe5],              0x6014], # push hl
            ["snippet", [0x21, 0x0e, 0x00],  0x6015], # hl = 0x000d unused?
            ["snippet", [0xe5],              0x6018], # push hl
            ["snippet", [0xc3, 0x7c, 0x18],  0x6019], # run program
            # 'PL/1' program
            ["snippet", [0x18],              0x8000], # bin to decimal
            ["snippet", [0x1f],              0x8001], # return
            ["snippet", [0x1f],              0x8002]  # return
    ],
    "funcs" : [],
    "pois" : {}
}


SCR = {
    "descr": "SCR program from felsökningsdiskett",
    "start": 0x4300,
    "stop" : 0x370,
    "data": [
            ["file", "roms/JDC/full.bin", 0x0000],
            ["snippet", [0xf3, 0x3e, 0x00, 0xd3, 0x0a, 0x3e, 0x05, 0xd3, 0x04, 0x16, 0x00, 0x7a, 0xd3, 0x03, 0x14, 0x7a],  0x4300],
            ["snippet", [0xfe, 0x80, 0xca, 0x36, 0x43, 0x2e, 0xff, 0x2d, 0xc2, 0x17, 0x43, 0xdb, 0x01, 0xfe, 0x00, 0xca],  0x4310],
            ["snippet", [0x0b, 0x43, 0xfe, 0x0e, 0xca, 0x0b, 0x43, 0xfe, 0x0f, 0xc2, 0x0b, 0x43, 0xdb, 0x01, 0xfe, 0x0e],  0x4320],
            ["snippet", [0xc2, 0x2c, 0x43, 0xc3, 0x0b, 0x43, 0x21, 0x42, 0x43, 0x0e, 0x03, 0x06, 0x2d, 0xed, 0xb3, 0xc3],  0x4330],
            ["snippet", [0x09, 0x43, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x54],  0x4340],
            ["snippet", [0x48, 0x49, 0x53, 0x20, 0x53, 0x50, 0x41, 0x43, 0x45, 0x20, 0x46, 0x4f, 0x52, 0x20, 0x52, 0x45],  0x4350],
            ["snippet", [0x4e, 0x54, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0x20, 0xfd],  0x4360]
    ],
    "funcs" : [],
    "pois" : {
        0x4312: 'print "THIS SPACE FOR RENT"',
        0x4318: 'delay',
        0x431b: 'get key',
        0x4336: 'hl -> "THIS SPACE FOR RENT"',
        0x433d: 'otir - write string to display'
    },
    "known_ranges" : [
        [0x4300, 0x4341, 'SCR()'],
        [0x4342, 0x436f, 'TEXT - THIS SPACE FOR RENT']
        ]
}
