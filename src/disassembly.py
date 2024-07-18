#!/usr/bin/env python3

import z80, sys, argparse
import memory, cpu
import programs as prg


def main(range):
    prgobj = prg.proglist["jdc_full"]
    C = cpu.Cpu(prgobj)
    C.reset()

    for start, end, text in range:
        #print(f'Range 0x{start:04x} - 0x{end:04x}\n<<<<< {text} >>>>>')
        print(f'<<<<< {text} >>>>>')
        C.m.pc = start
        while True:
            # Decode the instruction.
            inst_str, bytes, bytes_str = C.getinst()

            func_desc = ""
            if C.m.pc in C.mem.pois:
                func_desc = f'{C.mem.pois[C.m.pc]}'
            print(f'{C.m.pc:04X} {bytes_str:12} ; {inst_str:15} | {func_desc}')

            C.m.pc += len(bytes)

            if C.m.pc > end:
                #print('-------------------------------------')
                break




if __name__ == "__main__":

    def auto_int(x):
        return int(x, 0)

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auto", help = "disassemble known ranges", action='store_true')
    parser.add_argument("-s", "--start", help = "start at specified address",
                        type = auto_int, default = 0)
    parser.add_argument("-e", "--end", help = "end at specified address",
                        type = auto_int, default = 0x0500)

    args = parser.parse_args()

    # (mostly) validated ranges
    known_ranges = [
        [0x0000, 0x003e, 'jump tables'],
        [0x003f, 0x0041, 'Return Address (copied to 4080)'],
        [0x0042, 0x0044, 'JP to interrupt routine (copied to 4083)'],
        [0x0045, 0x0047, 'JP to wait-for-keyboard-or-printer'],

        [0x0052, 0x0054, 'interrupt38 chain'],

        [0x01de, 0x01ee, 'interrupt routine()'],
        [0x01e5, 0x01ea, 'set keyboard mode 2 (ASM IO page 10)'],
        [0x01eb, 0x01f2, 'prepare registers for copy and clearing'],
        [0x01f3, 0x01f7, 'copy jump tables from 003f:0047 to 4080:4088'],
        [0x01f8, 0x01fc, 'clear RAM from 4089 to 40ff'],
        [0x01fd, 0x0200, 'printer control - reset printer, raise ribbon'],
        [0x0201, 0x020e, 'printer status  - check result (0 is good)'],
        [0x020f, 0x029f, 'DONE()?'],
        [0x02a0, 0x02b0, 'Display width?'],
        [0x02b1, 0x0367, 'interrupt processing routine()'],
        [0x0368, 0x0380, 'unknown 1'],
        [0x0381, 0x038e, 'text string - CLR, PRINTER FAULT'],
        [0x038f, 0x03cb, 'check printer status'],
        [0x03cd, 0x0409, 'unknown 3'],
        [0x0410, 0x0438, 'clear keyboard buffer, update display'],
        [0x0439, 0x044d, 'XXX'],
        [0x044e, 0x0457, 'print A, E times (entry 0x450)'],
        [0x0458, 0x047c, 'display() - string=HL, len=C'],
        [0x047d, 0x04a8, 'unkown'],
        [0x04a9, 0x04b2, 'wait for keyboard'],
        [0x04B3, 0x04CA, 'clear display?'],
        [0x04CB, 0x04D0, 'disable interrupt, get key?, enable interrupt'],
        [0x04D1, 0x04D7, 'wait for key 0x0E'],
        [0x04D8, 0x0547, 'read key(s)?'],
        [0x0548, 0x0552, 'unknown'],
        [0x0553, 0x0562, 'updis() - called after printing line?'],
        [0x0563, 0x0583, 'unknown'],

        [0x0599, 0x05a7, 'unknown (on key 0x9a?)'],
        [0x05b5, 0x05cd, 'unknown'],
        [0x05ce, 0x05d3, 'something with HEX last key'],
        [0x05d4, 0x05d9, 'Toggle INSERT mode (on key 0x1e)'],

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
        [0x0830, 0x0970, 'open()...'],

        [0x088e, 0x0949, 'read()'],
        [0x094a, 0x0974, 'write()'],
        [0x0975, 0x0b3a, 'rewrite()'],
        [0x0d1e, 0x0d6a, 'loader()'],
        [0x0d6b, 0x0d8a, 'clrdk() '],
        [0x0d8b, 0x0d8d, 'text string? - IWS'],
        [0x0d8e, 0x0de0, 'unknown'],
        [0x0de1, 0x0e4e, 'text strings - INDEX .. WEIRD ERR'],
        [0x0e4f, 0x0f4f, 'unknown'],
        [0x1003, 0x1005, 'write?'],
        [0x1144, 0x1284, 'write??']

        # [0x0439, 0x0551, 'UPDIS() ?'],
        # [0x0553, 0x0590, 'UPDIS() ?'],
        # [0x0077, 0x0106, 'TOSTR() ?'],
        # [0x015B, 0x01AB, 'TOINT() ?'],
        # [0x0439, 0x047C, 'unknown function']
    ]

    if args.auto:
        main(known_ranges)
    else:
        main([[args.start, args.end, 'Custom']])
