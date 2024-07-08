#!/usr/bin/env python3

import z80, sys
import memory
import argparse

calldict = {0x05:0, 0x04:0, 0x01:0, 0x0c:0, 0x1a:0}

def myfunc(a):
    func = a & 0xff
    calldict[func]+=1
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
        print(f'unknown IO')
        return 0
    elif func == 0x1a:
        print(';in (1A): unknown IO II')
        return 0
    elif func == 0x04:
        print(f';in (04): display staus')
        return 0
    else:
        print(f'unhandled in ({func})')
        sys.exit()


def main(args):
    e = z80
    m = z80.Z80Machine()
    m.set_input_callback(myfunc)
    b = z80._Z80InstrBuilder()


    mem = memory.Memory(m)
    # Clear all memory to 0xff
    mem.set(0, 65535, 0xff)
    # Load ROMs to assumed addresses
    mem.loadroms(mem.roms)

    m.pc = args.start

    out03 = ''

    icount = 0
    mem.hexdump(0x2000, 0xFFFF - 0x2000, icount) # dump RAM part of memory

    while True:
        icount += 1
        if icount >= args.stopafter:
            print(f'max instruction count reached, exiting ...')
            print(f'printed characters ({len(out03)}):')
            print(f'{out03}')
            print('-----')
            sys.exit()

        # Decode the instruction.

        MAX_INSTR_SIZE = 4
        instr = b.build_instr(m.pc, bytes(m.memory[m.pc:m.pc + MAX_INSTR_SIZE]))
        instr_str = f"{instr}"
        if instr_str[:9] == 'out (0x3)':
            out03 += chr(m.a)
            print(f'; out (0x3): 0x{m.a:02X} char: ({chr(m.a)})')

        # Get and verbalise the instruction bytes.
        instr_bytes = bytes(m.memory[instr.addr:instr.addr + instr.size])
        instr_bytes = ' '.join(f'{b:02X}' for b in instr_bytes)
        if m.pc in mem.funcs:
            print(f';{mem.funcs[m.pc]}')
        if args.nodecode:
            print(f'{m.pc:04X} {instr_bytes:12} ; {instr_str:15} | SP={m.sp:04X}, A={m.a:02X} BC={m.bc:04X}, DE={m.de:04X}, HL={m.hl:04X}')


        if m.pc == args.poi: # PC of interest
            print('\n<<<<< pc of interest >>>>>\n')

        if icount % args.dumpfreq == 0 and not args.nodump:
            mem.hexdump(0x2000, 0x10000 - 0x2000, icount) # dump RAM part of memory

        data = mem.getu32(m.pc)
        if data == 0xffffffff:
            print(f'all ones at {m.pc:04x}, exiting ...')
            sys.exit()


        # Limit runs to a single tick so each time we execute exactly one instruction.
        m.ticks_to_stop = 1
        m.run()



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
