


class Memory():

    funcs = {
       0x0038: "interrupt ROM()",
       0x01e5: "interrupt2 ROM()",
       0x01f3: "copy interrupt vectors to 4080",
       0x01f8: "clear RAM from 4089 to 40ff",
       0x02b1: "interrupt3 ROM()",
       0x0410: "write 0x20 from 4100 to 417f",
       0x04a9: "unknown_io()",
       0x4083: "interrupt RAM()",
       0x4086: "wait_for_kbd_or_printer()"
    }

    def __init__(self, m):
        self.m = m.memory


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
            print(f'loaded {len(block)} bytes from {file} at address {address}')
            fh.close()


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
