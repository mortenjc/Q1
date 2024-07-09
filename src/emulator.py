#!/usr/bin/env python3

import z80, sys
import memory, cpu, z80io
import argparse
from collections import defaultdict

calldict = defaultdict(int)

def out3(addr, value):
    if z80io.isprintable(value):
        return chr(value)
    else:
        return '~'


def main(args):
    C = cpu.Cpu()
    io = z80io.IO()
    C.reset()
    C.m.set_input_callback(io.handle_io_in)
    C.m.pc = args.start

    icount = 0
    if not args.nodump:
        C.mem.hexdump(0x2000, 0xFFFF - 0x2000, icount) # dump RAM part of memory

    while True:
        icount += 1
        if icount >= args.stopafter:
            print(f'max instruction count reached, exiting ...')
            print(f'printed characters ({len(io.displaystr)}):')
            print(f'{io.displaystr}')
            print('-----')
            sys.exit()

        if C.m.pc in C.mem.funcs and not args.nodecode:
            print(f'; {C.mem.funcs[C.m.pc]}')

        if C.m.pc == args.poi and not args.nodecode: # PC of interest
            print('\n<<<<< pc of interest >>>>>\n')

        # Decode the instruction.
        inst_str, bytes, bytes_str = C.getinst()
        inst_str = C.decodestr(inst_str, bytes_str)
        if not args.nodecode:
            print(inst_str)
        if bytes[0] == 0xD3:
            io.handle_io_out(bytes[1], C.m.a)




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
    parser.add_argument("-d", "--nodecode", help = "Decode instructions", action='store_true')
    parser.add_argument("-a", "--start", help = "start at specified address",
                        type = auto_int, default = 0)

    args = parser.parse_args()

    main(args)
