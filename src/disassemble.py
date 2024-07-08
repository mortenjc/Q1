#!/usr/bin/env python3

import z80, sys
import memory, cpu
import argparse


def main(range):

    C = cpu.Cpu()
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
        [0x01e5, 0x01ea, 'set keyboard mode 2 (ASM IO page 10)'],
        [0x01eb, 0x01f2, 'prepare registers for copy and clearing'],
        [0x01f3, 0x01f7, 'copy jump tables from 003f:0047 to 4080:4088'],
        [0x01f8, 0x01fc, 'clear RAM from 4089 to 40ff'],
        [0x01fd, 0x0200, 'printer control - reset printer, raise ribbon'],
        [0x0201, 0x0218, 'printer status  - check result (FF?)'],
        [0x044E, 0x0456, 'print backspace E times?'],
        [0x0464, 0x0478, 'print Q1-lite klar til brug'],
        [0x04D1, 0x054F, 'read key(s)?'],
        [0x0556, 0x0562, 'called after printing line?']
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
