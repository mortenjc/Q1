#!/usr/bin/env python3

import z80, sys
import memory
import argparse


def main(range):
    e = z80
    m = z80.Z80Machine()
    b = z80._Z80InstrBuilder()

    mem = memory.Memory(m)
    # Clear all memory to 0xff
    mem.set(0, 65535, 0xff)
    # Load ROMs to assumed addresses
    mem.loadroms(mem.roms)

    print()

    for start, end, text in range:
        #print(f'Range 0x{start:04x} - 0x{end:04x}\n<<<<< {text} >>>>>')
        print(f'<<<<< {text} >>>>>')
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

            if m.pc > end:
                #print('-------------------------------------')
                break




if __name__ == "__main__":

    def auto_int(x):
        return int(x, 0)

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auto", help = "disassemble known ranges", action='store_true')
    parser.add_argument("-s", "--start", help = "start at specified address",
                        type = auto_int, default = 0)
    parser.add_argument("-e", "--end", help = "end at specified address",
                        type = auto_int, default = 0x0500)

    args = parser.parse_args()

    # (mostly) validated ranges
    known_ranges = [
        [0x0000, 0x003e, 'jump tables'],
        [0x01e5, 0x01ea, 'set keyboard mode 2 (ASM IO page 10)'],
        [0x01eb, 0x01f2, 'prepare registers for copy and clearing'],
        [0x01f3, 0x01f7, 'copy jump tables from 003f:0047 to 4080:4088'],
        [0x01f8, 0x01fc, 'clear RAM from 4089 to 40ff'],
        [0x01fd, 0x0200, 'printer control - reset printer, raise ribbon'],
        [0x0201, 0x0218, 'printer status  - check result (FF?)'],
        [0x04D1, 0x054F, 'read key(s)?']
        # [0x0439, 0x0551, 'UPDIS() ?'],
        # [0x0553, 0x0590, 'UPDIS() ?'],
        # [0x0077, 0x0106, 'TOSTR() ?'],
        # [0x015B, 0x01AB, 'TOINT() ?'],
        # [0x0439, 0x047C, 'unknown function']
    ]

    if args.auto:
        main(known_ranges)
    else:
        main([[args.start, args.end, 'Custom']])
