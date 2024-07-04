#!/usr/bin/env python3

import z80, sys
import memory
import argparse


def main(range):
    e = z80
    m = z80.Z80Machine()
    b = z80._Z80InstrBuilder()

    # Clear all memory to 0xff
    mem = memory.Memory(m)
    mem.set(0, 65535, 0xff)

    # Load ROMs to assumed addresses
    mem.loadfile("roms/IC25.BIN", 0x0000)
    mem.loadfile("roms/IC26.BIN", 0x0400)
    mem.loadfile("roms/IC27.BIN", 0x0800)
    mem.loadfile("roms/IC28.BIN", 0x0C00)
    mem.loadfile("roms/IC29.BIN", 0x1000)
    mem.loadfile("roms/IC30.BIN", 0x1400)
    mem.loadfile("roms/IC31.BIN", 0x1800)
    mem.loadfile("roms/IC32.BIN", 0x1C00)

    print()

    for start, end, text in range:
        print(f'Range 0x{start:04x} - 0x{end:04x}\n<<<<< {text} >>>>>')
        m.pc = start
        while True:
            # Decode the instruction.
            MAX_INSTR_SIZE = 4
            instr = b.build_instr(m.pc, bytes(m.memory[m.pc:m.pc + MAX_INSTR_SIZE]))
            instr_str = f"{instr}"
            # Get and verbalise the instruction bytes.
            instr_bytes = bytes(m.memory[instr.addr:instr.addr + instr.size])
            instr_bytes = ' '.join(f'{b:02X}' for b in instr_bytes)

            func_desc = ""
            if m.pc in mem.pois:
                func_desc = f'{mem.pois[m.pc]}'
            print(f'{m.pc:04X} {instr_bytes:12} ; {instr_str:15} | {func_desc}')

            m.pc += instr.size

            if m.pc >= end:
                print('----------------------------')
                break




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auto", help = "known ranges", action='store_true')
    parser.add_argument("-s", "--start", help = "start at specified address",
                        type = int, default = 0)
    parser.add_argument("-e", "--end", help = "end at specified address",
                        type = int, default = 0x2000)

    args = parser.parse_args()

    ranges = [
        [0x0000, 0x0035, 'jump tables'],
        [0x0439, 0x047C, 'unknown function']
    ]

    if args.auto:
        main(ranges)
    else:
        main([args.start, args.end, 'Custom'])
