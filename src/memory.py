


class Memory():


    def __init__(self, m):
        self.m = m


    def hexdump(self, address, length, icount):
        print(f"########### HEXDUMP 0x{address:x} - 0x{address+length:x} ####################################")
        print(f'icount {icount}')
        hexline = f"{address:04X} "
        char = ""
        count = 0
        prevempty = False
        for i in range(length):
            byte  = self.m.memory[address + i]
            hexline += f"{byte:02X} "
            if byte >=32 and byte < 122:
                char += chr(byte)
            else:
                char += "."
            count += 1
            if count == 16:
                if hexline[5:] != "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ":
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
            self.m.memory[i] = val
        print(f'set {end - start + 1} bytes of memory to {val}')


    def getu32(self, address):
        return (self.m.memory[address + 0] <<  0) + \
               (self.m.memory[address + 1] <<  8) + \
               (self.m.memory[address + 2] << 16) + \
               (self.m.memory[address + 3] << 24)


    def load(self, file, address):
            fh = open(file, 'rb')
            block = list(fh.read())
            assert len(block) + address < 65535
            for i in range(len(block)):
                self.m.memory[address + i] = block[i]
            print(f'loaded {len(block)} bytes from {file} at address {address}')
            fh.close()
