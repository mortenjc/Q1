"""Memory utilities used on top of Korarev's z80 emulator"""

class Memory():

    def __init__(self, m):
        self.m = m.memory
        self.verbose = True


    def print(self, s):
        if self.verbose:
            print(s)


    def clear(self, val: int):
        # Clear memory (set to val)
        for i, _ in enumerate(self.m):
            self.m[i] = val


    def loader(self, program : dict) -> int:
        # The main program loader
        print(f'loading program: {program["descr"]}')
        pc = program["start"]
        for datatype, source, addr in program["data"]:
            if datatype == "file":
                self._loadfile(source, addr)
            elif datatype == "snippet":
                self._loaddata(source, addr)
            else:
                print(f"Ignoring unknown data soure: {datatype}")
        return pc


    def hexdump(self, address, length):
        nullpatt = "fd " * 16
        self.print(f"########### HEXDUMP 0x{address:x} - 0x{address+length:x} ####################################")
        hexline = f"{address:04x} "
        char = ""
        count = 0
        prevempty = False
        for i in range(length):
            byte  = self.m[address + i]
            hexline += f"{byte:02x} "
            if 32 <= byte < 122:
                char += chr(byte)
            else:
                char += "."
            count += 1
            if count == 16:
                if hexline[5:] != nullpatt:
                    self.print(f'{hexline} {char}')
                    prevempty = False
                else:
                    if prevempty is False:
                        self.print('....')
                        prevempty = True
                hexline = f"{address +i+1:04x} "
                char = ""
                count = 0
        self.print("########### HEXDUMP END #################################################")


    def writeu8(self, addr: int, val: int):
        assert 0 <= val <= 255
        self.m[addr] = val

    def writeu16(self, addr: int, val: int):
        hi = val >> 8
        lo = val & 0xFF
        self.writeu8(addr  , lo)
        self.writeu8(addr+1, hi)


    def getu8(self, address: int) -> int:
        # Get byte from memory
        val = self.m[address]
        assert 0 <= val <= 255
        return val


    def getu16(self, address: int):
        # Get 2-byte word from memory
        return self.getu8(address) + (self.getu8(address+1) << 8)


    def getu32(self, address: int):
        # Get 4-byte word from memory
        lo = self.getu16(address)
        hi = self.getu16(address+2)
        return lo + (hi << 16)


    def _loadfile(self, file: str, address: int):
        # Helper code to load a file into a specidied address
        with open(file, 'rb') as fh:
            block = list(fh.read())
            assert len(block) + address < 65535
            for i, d in enumerate(block):
                self.m[address + i] = d
            print(f'loaded {len(block)} bytes from {file} at address {address:04x}h')


    def _loaddata(self, data: list, address: int):
        # Helper code to load a list of bytes into a specified address
        for i, d in enumerate(data):
            self.m[address+i] = d
        print(f'loaded {len(data)} bytes from list at address {address:04x}h')


if __name__ == '__main__':

    class Standin():
        def __init__(self):
            self.memory = [0 for i in range(65536)]
            self.memory[0] = 0
            self.memory[1] = 1
            self.memory[2] = 2
            self.memory[3] = 3

    standin = Standin()
    mem = Memory(standin)

    assert mem.getu8(0) == 0
    assert mem.getu8(1) == 1
    assert mem.getu16(0) == 256
    assert mem.getu32(0) == mem.getu16(0) + mem.getu16(2)*65536
