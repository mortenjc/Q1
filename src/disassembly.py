#!/usr/bin/env python3

"""Module providing Z80 disassembly functionality"""

import sys
import argparse
import cpu
import match
import memory
import ros as r
import programs as prg


def disassemble(args, ranges):
    prgobj = prg.proglist[args.program]
    c = cpu.Cpu(prgobj)
    ros = r.ROS(c.mem)
    c.reset()

    for start, end, text in ranges:
        print(f'\n;{text}')
        c.m.pc = start
        while True:
            # Decode the instruction.
            inst_str, ibytes, bytes_str = c.getinst()

            annot = match.operandaddr(inst_str, ros.addrs)
            if annot == "":
                if c.m.pc in prgobj["pois"]:
                    annot = f'{prgobj["pois"][c.m.pc]}'

            print(f'{c.m.pc:04x} {bytes_str:12} ; {inst_str:20} | {annot}')

            c.m.pc += len(ibytes)

            if c.m.pc > end:
                #print('-------------------------------------')
                break




if __name__ == "__main__":


    print()

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
        except KeyError:
            print(f'please specify known_ranges for {args.program}')
            sys.exit()

    disassemble(args, known_ranges)
