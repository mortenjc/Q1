#!/usr/bin/env python3

import z80, sys
import memory, cpu
import argparse


def main(args):

    C = cpu.Cpu()
    C.reset()
    C.m.pc = args.start

    out03 = ''

    icount = 0
    C.mem.hexdump(0x2000, 0xFFFF - 0x2000, icount) # dump RAM part of memory

    while True:
        icount += 1
        if icount >= args.stopafter:
            print(f'max instruction count reached, exiting ...')
            print(f'printed characters ({len(out03)}):')
            print(f'{out03}')
            print('-----')
            sys.exit()

        # Decode the instruction.
        inst = C.getinst()


        if C.m.pc == args.poi: # PC of interest
            print('\n<<<<< pc of interest >>>>>\n')

        if icount % args.dumpfreq == 0 and not args.nodump:
            C.mem.hexdump(0x2000, 0x10000 - 0x2000, icount) # dump RAM part of memory

        C.step()



if __name__ == "__main__":

    def auto_int(x):
        return int(x, 0)

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--stopafter", help = "stop after N instructions",
                        type = int, default = 16380)
    parser.add_argument("-p", "--poi", help = "Point of interest (PC)",
                        type = auto_int, default = 0x0d8a)
    parser.add_argument("--dumpfreq", help = "Hexdump every N instruction",
                        type = int, default = 256)
    parser.add_argument("-n", "--nodump", help = "Toggle hexdump", action='store_true')
    parser.add_argument("-d", "--nodecode", help = "Decode instructions", action='store_false')
    parser.add_argument("-a", "--start", help = "start at specified address",
                        type = auto_int, default = 0)

    args = parser.parse_args()

    main(args)
