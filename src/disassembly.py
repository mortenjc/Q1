#!/usr/bin/env python3

"""Module providing Z80 disassembly functionality"""

import argparse
import cpu
import memory
import sys
import programs as prg


def main(ranges):
    prgobj = prg.proglist[args.program]
    c = cpu.Cpu(prgobj)
    c.reset()

    for start, end, text in ranges:
        print(f'<<<<< {text} >>>>>')
        c.m.pc = start
        while True:
            # Decode the instruction.
            inst_str, bytes, bytes_str = c.getinst()

            func_desc = ""
            if c.m.pc in prgobj["pois"]:
                func_desc = f'{prgobj["pois"][c.m.pc]}'
            print(f'{c.m.pc:04x} {bytes_str:12} ; {inst_str:15} | {func_desc}')

            c.m.pc += len(bytes)

            if c.m.pc > end:
                #print('-------------------------------------')
                break




if __name__ == "__main__":

    def auto_int(x):
        return int(x, 0)

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auto", help = "disassemble known ranges", action='store_true')
    parser.add_argument("-l", "--list", help = "showavailable programs", action='store_true')
    parser.add_argument("-s", "--start", help = "start at specified address",
                        type = auto_int, default = 0)
    parser.add_argument("-e", "--end", help = "end at specified address",
                        type = auto_int, default = 0x0500)
    parser.add_argument("--program", help = "name of program to load, see programs.py",
                        type = str, default = "jdc")

    args = parser.parse_args()

    if args.list:
        for p in prg.proglist:
            print(p)
        sys.exit()

    known_ranges = [[args.start, args.end, 'Custom']]
    if args.auto:
        try:
            known_ranges = prg.proglist[args.program]["known_ranges"]
        except:
            print(f'please specify known_ranges for {args.program}')
            sys.exit()

    main(known_ranges)
