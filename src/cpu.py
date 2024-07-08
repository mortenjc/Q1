#!/usr/bin/env python3

import z80, sys
import memory
import argparse

def isprintable(c):
    return c >= 0x20 and c <= 0x7D

class Cpu:
    MAX_INSTR_SIZE = 4


    def in_cb_func(self, val):
        reg = val >> 8
        ioaddr = val & 0xff
        print(f'in ({ioaddr}) callback (reg val {reg})')
        return 0

    def __init__(self):
        self.e = z80
        self.m = z80.Z80Machine()
        self.m.set_input_callback(self.in_cb_func)
        self.b = z80._Z80InstrBuilder()
        self.in_cbs = {}
        self.out_cbs = {}
        self.mem = memory.Memory(self.m)


    def reset(self):
        # Clear all memory to 0xff
        self.mem.set(0, 65535, 0xff)
        # Load ROMs to assumed addresses
        self.mem.loadroms(self.mem.roms)


    def step(self, ticks=1):
        self.m.ticks_to_stop = ticks
        self.m.run()

        data = self.mem.getu32(self.m.pc)
        if data == 0xffffffff:
            print(f'all ones at {self.m.pc:04x}, exiting ...')
            sys.exit()


    def getinst(self):
        instr = self.b.build_instr(self.m.pc, bytes(self.m.memory[self.m.pc:self.m.pc + Cpu.MAX_INSTR_SIZE]))
        instr_str = f"{instr}"
        # Get and verbalise the instruction bytes.
        instr_bytes = bytes(self.m.memory[instr.addr:instr.addr + instr.size])
        instr_bytes_str = ' '.join(f'{b:02X}' for b in instr_bytes)
        return instr_str, instr_bytes, instr_bytes_str


    def decodestr(self, inst, bytes):
        if isprintable(self.m.a):
            a_str = chr(self.m.a)
        else:
            a_str = '.'

        return f'{self.m.pc:04X} {bytes:12} ; {inst:15} | SP={self.m.sp:04X}, A={self.m.a:02X}({a_str}) BC={self.m.bc:04X}, DE={self.m.de:04X}, HL={self.m.hl:04X}'


# def myfunc(a):
#     func = a & 0xff
#     calldict[func]+=1
#     if func == 0x05:
#         print(f';in (05): printer status: no error')
#         return 0
#     elif func == 0x01:
#         if calldict[func] == 1:
#             print(f';in (01): read key 0x0F')
#             return 0x0f
#         else:
#             print(f';in (01): read key 0x0E')
#             return 0x0e
#     elif func == 0x0c:
#         print(f'unknown IO')
#         return 0
#     elif func == 0x1a:
#         print(';in (1A): unknown IO II')
#         return 0
#     elif func == 0x04:
#         print(f';in (04): display staus')
#         return 0
#     else:
#         print(f'unhandled in ({func})')
#         sys.exit()
