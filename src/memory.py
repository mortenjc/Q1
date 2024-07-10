


class Memory():

    roms = [
        ["roms/IC25.BIN", 0x0000],
        ["roms/IC26.BIN", 0x0400],
        ["roms/IC27.BIN", 0x0800],
        ["roms/IC28.BIN", 0x0C00]
        # ["roms/IC29.BIN", 0x1000],
        # ["roms/IC30.BIN", 0x1400],
        # ["roms/IC31.BIN", 0x1800],
        # ["roms/IC32.BIN", 0x1C00]
    ]

    funcs = {
       0x0000: "reset()",
       0x0038: "0038 interrupt ROM()",
       0x01e5: "01e5 interrupt2 ROM()",
       0x01eb: "01eb setup registers for copying and clearing",
       0x01f3: "01f3 copy (function calls) from 0x003f:0x0047 to 0x4080:",
       0x01f8: "01f8 clear RAM from 4089 to 40ff",
       0x02b1: "02b1 interrupt3 ROM()",
       0x0410: "0410 write 0x20 from 4100 to 417f",
       0x04a9: "04a9 unknown_io()",
       0x04d1: "04d1 wait_for_key_0x0e()",
       0x4083: "4083 interrupt RAM()",
       0x4086: "4086 wait_for_kbd_or_printer()"
    }

    # Named points of interest, for disassembly
    pois = {
        0x0000: 'reset vector',
        0x0003: 'TOSTR',
        0x0006: 'TODEC',
        0x0009: 'UPDIS',
        0x000C: 'MUL',
        0x000F: 'DIV',
        0x0012: 'BICHAR',
        0x0015: 'NHL',
        0x0018: 'START',
        0x001B: 'KFILE',
        0x001E: 'KEYIN',
        0x0021: 'GETDN',
        0x0024: 'NKEY',
        0x0027: 'DISPLAY',
        0x002A: 'PRINTER',
        0x002D: 'CARB',
        0x0030: 'STOP',
        0x0033: 'PROCH',
        0x0036: 'INTRET',
        0x0039: 'INDEX',
        0x003C: 'SHIFTY',
        0x043F: 'display ctrl (0x05) Reset, Unbuffer'
    }


    def __init__(self, m):
        self.m = m.memory
        self.verbose = False


    def hexdump(self, address, length, icount):
        nullpatt = "FF " * 16
        print(f"########### HEXDUMP 0x{address:x} - 0x{address+length:x} ####################################")
        print(f'icount {icount}')
        hexline = f"{address:04X} "
        char = ""
        count = 0
        prevempty = False
        for i in range(length):
            byte  = self.m[address + i]
            hexline += f"{byte:02X} "
            if byte >=32 and byte < 122:
                char += chr(byte)
            else:
                char += "."
            count += 1
            if count == 16:
                if hexline[5:] != nullpatt:
                    print(hexline, char)
                    prevempty = False
                else:
                    if prevempty == False:
                        print('....')
                        prevempty = True
                hexline = f"{address +i+1:04X} "
                char = ""
                count = 0
        print(f"########### HEXDUMP END #################################################")


    def set(self, start, end, val):
        assert end >= start
        assert val >= 0 and val <= 255

        for i in range(start, end + 1):
            self.m[i] = val
        if self.verbose:
            print(f'set {end - start + 1} bytes of memory to {val}')


    def writeu8(self, addr, val):
        assert val >=0 and val <= 255
        self.m[addr] = val


    def getu8(self, address: int) -> int:
        val = self.m[address]
        assert val >= 0 and val <= 255
        return val


    def getu16(self, address):
        return self.getu8(address) + (self.getu8(address+1) << 8)


    def getu32(self, address):
        lo = self.getu16(address)
        hi = self.getu16(address+2)
        return lo + (hi << 16)


    def loadfile(self, file, address):
            fh = open(file, 'rb')
            block = list(fh.read())
            assert len(block) + address < 65535
            for i in range(len(block)):
                self.m[address + i] = block[i]
            if self.verbose:
                print(f'loaded {len(block)} bytes from {file} at address {address}')
            fh.close()


    def loadroms(self, romlist):
        for file, addr in romlist:
            self.loadfile(file, addr)


    def loaddata(self, data, address):
        for i in range(len(data)):
            self.m[address+i] = data[i]


    def clear(self, val):
        for i in range(len(self.m)):
            self.m[i] = val


if __name__ == '__main__':

    class Standin():
        def __init__(self):
            self.memory = [0 for i in range(65536)]
            self.memory[0] = 0
            self.memory[1] = 1
            self.memory[2] = 2
            self.memory[3] = 3

    s = Standin()
    mem = Memory(s)

    assert mem.getu8(0) == 0
    assert mem.getu8(1) == 1
    assert mem.getu16(0) == 256
    assert mem.getu32(0) == mem.getu16(0) + mem.getu16(2)*65536
