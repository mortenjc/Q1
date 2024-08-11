#!/usr/bin/env python3

"""Module providing a CPU abstraction"""

import sys
import z80
import memory
import ros as r
import z80io


class Cpu:
    MAX_INSTR_SIZE = 4

    def __init__(self, program):
        self.bt = [] # backtrace
        self.program = program
        self.e = z80
        self.m = z80.Z80Machine()
        self.b = z80.Z80InstrBuilder()
        self.mem = memory.Memory(self.m)
        self.ros = r.ROS(self.mem)
        self.fill = 0xfd
        self.halt = 0xfdfdfdfd


    def reset(self) -> None:
        # Set all memory to self.fill
        self.mem.clear(self.fill)
        # Load ROMs to assumed addresses
        self.m.pc = self.mem.loader(self.program)


    def step(self, ticks:int=1):
        m = self.m
        m.ticks_to_stop = ticks
        m.run()

        data = self.mem.getu32(m.pc)
        if data == self.halt:
            print(f'0x{self.halt:04x} at {m.pc:04x}, exiting ...')
            self.exit()


    def info(self, ros=True, dump=True, bt=True):
        if ros:
            self.ros.index()
            self.ros.file()
            self.ros.disk()
        if dump:
            self.mem.hexdump(0x2000, 0x10000 - 0x2000)
        if bt:
            for l in self.bt:
                print(l)

    def exit(self, ros=True, dump=True, bt=True):
        self.info(ros, dump, bt)
        print('exiting...')
        sys.exit()


    def getinst(self):
        try:
            instr = self.b.build_instr(self.m.pc,
                bytes(self.m.memory[self.m.pc:self.m.pc + Cpu.MAX_INSTR_SIZE]))
            instr_str = f"{instr}"
            # Get and verbalise the instruction bytes.
            instr_bytes = bytes(self.m.memory[instr.addr:instr.addr + instr.size])
            instr_bytes_str = ' '.join(f'{b:02x}' for b in instr_bytes)
            return instr_str, instr_bytes, instr_bytes_str
        except Exception as e:
            print('exception: build_instr() failed')
            pc = self.m.pc
            mem = self.mem
            b1 = mem.getu8(pc)
            b2 = mem.getu8(pc+1)
            b3 = mem.getu8(pc+2)
            b4 = mem.getu8(pc+3)
            print(f'{pc:04x} {b1:02x} {b2:02x} {b3:02x} {b4:02x}')
            print(f'{repr(e)}')
            self.exit()


    def getregs(self):
        m = self.m
        return f'pc={m.pc:04x}, sp={m.sp:04x}, a={m.a:02x}, bc={m.bc:04x}, de={m.de:04x}, hl={m.hl:04x}, ix={m.ix:04x}'


    def decodestr(self, inst: str, ibytes: []) -> str:
        if z80io.isprintable(self.m.a):
            a_str = f"'{chr(self.m.a)}'"
        else:
            a_str = '   '
        m = self.m
        l = f'{m.pc:04x} {ibytes:12} ; {inst:25} | sp={m.sp:04x}, ' + \
            f'a={m.a:02x}{a_str} bc={m.bc:04x}, de={m.de:04x}, hl={m.hl:04x}, ' + \
            f'ix={m.ix:04x}, iy={m.iy:04x}'
        self.bt.append(l)
        if len(self.bt) == 10:
            self.bt = self.bt[1:]
        return l
