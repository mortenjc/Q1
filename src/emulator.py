#!/usr/bin/env python3

import z80, sys
import memory, cpu
import argparse
from collections import defaultdict

calldict = defaultdict(int)

def myfunc(a):
    func = a & 0xff
    calldict[func] += 1
    if func == 0x05:
        print(f';in (05): printer status: no error')
        return 0
    elif func == 0x01:
        if calldict[func] == 1:
            print(f';in (01): read key 0x0F')
            return 0x0f
        else:
            print(f';in (01): read key 0x0E')
            return 0x0e
    elif func == 0x0c:
        print(f';in (0C): unknown IO')
        return 0
    elif func == 0x1a:
        print(';in (1A): unknown IO II')
        return 0
    elif func == 0x04:
        print(f';in (04): display status 0')
        return 0
    else:
        print(f'unhandled in ({func})')
        sys.exit()


def out3(addr, value):
    if cpu.isprintable(value):
        return chr(value)
    else:
        return '~'


def main(args):
    C = cpu.Cpu()
    C.reset()
    C.m.set_input_callback(myfunc)
    C.m.pc = args.start

    out03 = ''

    icount = 0
    if not args.nodump:
        C.mem.hexdump(0x2000, 0xFFFF - 0x2000, icount) # dump RAM part of memory

    while True:
        icount += 1
        if icount >= args.stopafter:
            print(f'max instruction count reached, exiting ...')
            print(f'printed characters ({len(out03)}):')
            print(f'{out03}')
            print('-----')
            sys.exit()

        if C.m.pc in C.mem.funcs and not args.nodecode:
            print(f'; {C.mem.funcs[C.m.pc]}')

        if C.m.pc == args.poi and not args.nodecode: # PC of interest
            print('\n<<<<< pc of interest >>>>>\n')

        # Decode the instruction.
        inst_str, bytes, bytes_str = C.getinst()
        inst_str = C.decodestr(inst_str, bytes_str)
        if bytes[0] == 0xD3 and bytes[1] == 0x03:
            out03 += out3(bytes[1], C.m.a)
        if not args.nodecode:
            print(inst_str)



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
