#!/usr/bin/env python3

import z80, sys
import memory, z80io
import argparse

class Cpu:
    MAX_INSTR_SIZE = 4

    def __init__(self, program):
        self.program = program
        self.e = z80
        self.m = z80.Z80Machine()
        self.b = z80._Z80InstrBuilder()
        self.in_cbs = {}
        self.out_cbs = {}
        self.mem = memory.Memory(self.m)
        self.fill = 0xff
        self.halt = 0xffffffff


    def reset(self):
        # Set all memory to self.fill
        self.mem.clear(self.fill)
        # Load ROMs to assumed addresses
        self.m.pc = self.mem.loader(self.program)


    def step(self, ticks:int =1):
        self.m.ticks_to_stop = ticks
        self.m.run()

        data = self.mem.getu32(self.m.pc)
        if data == self.halt:
            print(f'0x{self.halt:04x} at {self.m.pc:04x}, exiting ...')
            sys.exit()


    def getinst(self):
        instr = self.b.build_instr(self.m.pc, bytes(self.m.memory[self.m.pc:self.m.pc + Cpu.MAX_INSTR_SIZE]))
        instr_str = f"{instr}"
        # Get and verbalise the instruction bytes.
        instr_bytes = bytes(self.m.memory[instr.addr:instr.addr + instr.size])
        instr_bytes_str = ' '.join(f'{b:02X}' for b in instr_bytes)
        return instr_str, instr_bytes, instr_bytes_str


    def decodestr(self, inst: str, bytes: []) -> str:
        if z80io.isprintable(self.m.a):
            a_str = f"'{chr(self.m.a)}'"
        else:
            a_str = '   '
        return f'{self.m.pc:04X} {bytes:12} ; {inst:15} | SP={self.m.sp:04X}, A={self.m.a:02X}{a_str} BC={self.m.bc:04X}, DE={self.m.de:04X}, HL={self.m.hl:04X}'
