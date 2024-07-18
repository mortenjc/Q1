#!/usr/bin/env python3

import z80, sys, argparse
import memory, cpu, z80io, kbd
import programs as prg


def int38(C):
    oldpc = C.m.pc
    C.m.pc -= 2
    C.mem.writeu16(C.m.pc, oldpc)
    C.m.pc = 0x38


def main(args):
    irq_count = 0
    next_irq = 7000

    prgobj = prg.proglist[args.program]
    C = cpu.Cpu(prgobj)
    io = z80io.IO()
    io.verbose = False
    key = kbd.Key()
    C.reset()
    C.m.set_input_callback(io.handle_io_in) # input hooks (emulator support)

    icount = 0
    if not args.nodump:
        C.mem.hexdump(0x2000, 0xFFFF - 0x2000, icount) # dump RAM part of memory

    while True:
        icount += 1
        if icount >= args.stopafter:
            print(f'max instruction count reached, exiting ...')
            for l in C.bt:
                print(l)
            print(f'printed characters ({len(io.displaystr)}):')
            print(f'{io.displaystr}')
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

        # IO hook for output
        if bytes[0] == 0xD3:
            io.handle_io_out(bytes[1], C.m.a)

        if icount % args.dumpfreq == 0 and not args.nodump:
            C.mem.hexdump(0x2000, 0x10000 - 0x2000, icount) # dump RAM part of memory

        # if icount % 100000 == 0:
        #     print(f'Instruction count: {icount}')

        C.step() # does the actual emulation of the next instruction

        # if C.m.pc == 0x4d1: # wait for key 0xe ??
        #     sys.exit()

        if (icount % 1000):
            if key.kbhit():
                ch = ord(key.getch())
                if ch >= 32 and ch < 127:
                    print(f'{chr(ch)}')
                else:
                    print(f'{ch}')
                if ch == 0x222b:  # opt-b, hexdump
                    C.mem.hexdump(0x2000, 0x10000 - 0x2000, icount)
                elif ch == 0x8800: # fake key 0xe
                    io.keyin = 0xe
                    int38(C)
                elif ch == 0x0a:
                    io.keyin = 0x0d
                    int38(C)
                    # args.nodecode = False
                    # args.nodump = False
                elif ch == 27: # ESC
                    sys.exit()
                elif ch == 127:
                    io.keyin = 0x8 # BS
                    int38(C)
                elif ch == 181: # opt-m INS
                    io.keyin = 0x1e # INS
                    int38(C)
                else:
                    io.keyin = ch
                    int38(C)



if __name__ == "__main__":

    def auto_int(x):
        return int(x, 0)

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--stopafter", help = "stop after N instructions",
                        type = int, default = 6380)
    parser.add_argument("-p", "--poi", help = "Point of interest (PC)",
                        type = auto_int, default = 0x0d8a)
    parser.add_argument("--dumpfreq", help = "Hexdump every N instruction",
                        type = int, default = 256)
    parser.add_argument("-n", "--nodump", help = "Toggle hexdump", action='store_true')
    parser.add_argument("-d", "--nodecode", help = "Decode instructions", action='store_true')
    parser.add_argument("--program", help = "name of program to load, see programs.py",
                        type = str, default = "jdc_full")

    args = parser.parse_args()
    if args.stopafter == -1:
        args.stopafter = 1000000000

    main(args)
