#!/usr/bin/env python3

import z80, sys
import memory
import argparse


def main(args):
    e = z80
    m = z80.Z80Machine()
    b = z80._Z80InstrBuilder()

    # Clear all memory to 0
    mem = memory.Memory(m)
    mem.set(0, 65535, 0)

    # Load ROMs to assumed addresses
    mem.load("roms/IC25.BIN", 0x0000)
    mem.load("roms/IC26.BIN", 0x0400)
    mem.load("roms/IC27.BIN", 0x0800)
    mem.load("roms/IC28.BIN", 0x0C00)
    mem.load("roms/IC29.BIN", 0x1000)
    mem.load("roms/IC30.BIN", 0x1400)
    mem.load("roms/IC31.BIN", 0x1800)
    mem.load("roms/IC32.BIN", 0x1C00)


    icount = 0
    mem.hexdump(0x2000, 0x10000 - 0x2000, icount) # dump RAM part of memory

    while True:
        icount += 1
        if icount >= args.stopafter:
            print(f'max instruction count reached, exiting ...')
            sys.exit()

        # Decode the instruction.
        MAX_INSTR_SIZE = 4
        instr = b.build_instr(m.pc, bytes(m.memory[m.pc:m.pc + MAX_INSTR_SIZE]))
        instr_str = f"{instr}"
        # Get and verbalise the instruction bytes.
        instr_bytes = bytes(m.memory[instr.addr:instr.addr + instr.size])
        instr_bytes = ' '.join(f'{b:02X}' for b in instr_bytes)
        print(f'{m.pc:04X} {instr_bytes:12} ; {instr_str:15} | SP={m.sp:04X}, A={m.a:02X} BC={m.bc:04X}, DE={m.de:04X}, HL={m.hl:04X}')


        if m.pc == args.poi: # PC of interest
            print('\n<<<<< pc of interest >>>>>\n')

        if icount % 256 == 0 and not args.nodump:
            mem.hexdump(0x2000, 0x10000 - 0x2000, icount) # dump RAM part of memory

        data = mem.getu32(m.pc)
        if data == 0:
            print(f'all zeroes at {m.pc:04x}, exiting ...')
            sys.exit()

        # Limit runs to a single tick so each time we execute exactly one instruction.
        m.ticks_to_stop = 1
        m.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--stopafter", help = "stop after N instructions",
                        type = int, default = 16380)
    parser.add_argument("-p", "--poi", help = "Point of interest (PC)",
                        type = int, default = 0x0d8a)
    parser.add_argument("-n", "--nodump", help = "Toggle hexdump", action='store_true')

    args = parser.parse_args()

    main(args)
