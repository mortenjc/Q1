#!/usr/bin/env python3

import argparse
import cpu as c
import kbd
import match
import memory
import ros as r
import sys
import z80
import z80io
import programs as prg


def int38(cpu, io, ch):
    io.keyin = ch
    oldpc = cpu.m.pc
    cpu.m.sp -= 2
    cpu.mem.writeu16(cpu.m.sp, oldpc)
    cpu.m.pc = 0x38


def main(args):
    prgobj = prg.proglist[args.program]
    funcs = prgobj["funcs"]
    cpu = c.Cpu(prgobj)
    io = z80io.IO(cpu.m)
    ros = r.ROS(cpu.mem)
    #io.verbose = True
    key = kbd.Key()
    cpu.reset()
    cpu.m.set_input_callback(io.handle_io_in)
    cpu.m.set_output_callback(io.handle_io_out)

    icount = 0
    if not args.nodump:
        cpu.mem.hexdump(0x2000, 0xFFFF - 0x2000, icount) # dump RAM part of memory

    while True:
        pc = cpu.m.pc
        icount += 1
        if icount >= args.stopafter:
            print(f'max instruction count reached, exiting ...')
            for l in cpu.bt:
                print(l)
            print(f'printed characters ({len(io.displaystr)}):')
            print(f'{io.displaystr}')
            sys.exit()

        if pc in funcs and not args.nodecode:
            print(f'; {funcs[pc]}')

        if pc == args.poi and not args.nodecode: # PC of interest
            print('\n<<<<< pc of interest >>>>>\n')

        # Decode the instruction.
        inst_str, bytes, bytes_str = cpu.getinst()
        inst_str2 = cpu.decodestr(inst_str, bytes_str)
        annot = match.operandaddr(inst_str, ros.addrs)
        if annot == "":
            if cpu.m.pc in prgobj["pois"]:
                annot = f'{prgobj["pois"][cpu.m.pc]}'
        if not args.nodecode:
            print(inst_str2, annot)


        if icount % args.dumpfreq == 0 and not args.nodump:
            cpu.mem.hexdump(0x2000, 0x10000 - 0x2000, icount) # dump RAM part of memory

        # main cpu emulation step
        cpu.step() # does the actual emulation of the next instruction

        if args.breakpoint == pc:
            print(f'\n<<<< BREAKPOINT at 0x{pc:04x} >>>>\n')
            ros.index()
            ros.file()
            ros.disk()
            cpu.exit()

        if args.trigger == pc:
            print(f'\n<<<< TRIGGER at 0x{pc:04x} >>>>\n')
            cpu.mem.hexdump(0x2000, 0x10000 - 0x2000, icount)
            args.nodecode = False
            io.verbose = True

        if pc ==0x4cb:
            print(io.displaystr)
            io.displaystr = ""
            ros.index()
            ros.file()
            ros.disk()
            print("<STOP>")

        if (icount % 1000) == 0: # int_disabled check?
            if key.kbhit():
                ch = ord(key.getch())
                if ch >= 32 and ch < 127:
                    print(f'{chr(ch)}')
                else:
                    print(f'{ch}')

                if ch == 0x222b:       # opt-b -> hexdump
                    cpu.mem.hexdump(0x2000, 0x10000 - 0x2000, icount)
                elif ch == 960:        # opt-p -> regdump
                    print(cpu.getregs())
                elif ch == 0x0a:       # LF -> CR
                    int38(cpu, io, 0x0d)
                elif ch == 169:        # opt-g GO
                    io.go = 1
                elif ch == 127:
                    int38(cpu, io, 0x04) # BS -> CORR
                elif ch == 231:
                    int38(cpu, io, 0x1b) # opt-c -> CLEAR ENTRY
                elif ch == 181:        # opt-m -> INSERT MODE
                    int38(cpu, io, 0x1e)
                elif ch == 170: # opt-a FDs
                    ros.index()
                    ros.file()
                    ros.disk()
                else:
                    int38(cpu, io, ch)


if __name__ == "__main__":

    def auto_int(x):
        return int(x, 0)

    parser = argparse.ArgumentParser()

    parser.add_argument("-b", "--breakpoint", help = "stop on BP, hexdump and backtrace",
        type = auto_int, default = 0x1FFFF)
    parser.add_argument("-t", "--trigger", help = "start decode at trigger address",
        type = auto_int, default = 0x1FFFF)
    parser.add_argument("-l", "--list", help = "showavailable programs",
        action='store_true')
    parser.add_argument("-s", "--stopafter", help = "stop after N instructions",
        type = int, default = -1)
    parser.add_argument("-p", "--poi", help = "Point of interest (PC)",
                        type = auto_int, default = 0x1ffff)
    parser.add_argument("--dumpfreq", help = "Hexdump every N instruction",
                        type = int, default = 256)
    parser.add_argument("-n", "--nodump", help = "Toggle hexdump", action='store_true')
    parser.add_argument("-d", "--nodecode", help = "Decode instructions", action='store_true')
    parser.add_argument("--program", help = "name of program to load, see programs.py",
                        type = str, default = "jdc")

    args = parser.parse_args()
    if args.stopafter == -1:
        args.stopafter = 1000000000

    if args.list:
        for p in prg.proglist:
            print(p)
        sys.exit()

    main(args)
