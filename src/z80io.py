
import sys

#

def isprintable(c):
    return c >= 0x20 and c <= 0x7D


class IO:
    def __init__(self):
        self.incb = {}
        self.outcb = {}
        self.keyincount = 0
        self.displaystr = ""
        self.register_in_cb( 0x01, self.handle_key_in)
        #self.register_in_cb( 0x01, self.handle_key_in_string) # 'ABCD' + CR
        self.register_out_cb(0x01, self.handle_key_out)

        self.register_out_cb(0x03, self.handle_display_out)
        self.register_out_cb(0x04, self.handle_display_out_ctrl)
        self.register_in_cb( 0x04, self.handle_display_in)

        self.register_in_cb( 0x05, self.handle_printer_in)
        self.register_out_cb(0x07, self.handle_printer_out_7)

        self.register_out_cb(0x0a, self.handle_ciu_out_0a)
        self.register_out_cb(0x0b, self.handle_ciu_out_0b)
        self.register_in_cb( 0x0c, self.handle_ciu_in_0c)
        self.register_out_cb(0x0c, self.handle_ciu_out_0c)

        self.register_in_cb( 0x1a, self.handle_disk_in_1a)
        self.register_out_cb(0x1a, self.handle_disk_out_1a)
        self.register_out_cb(0x1b, self.handle_disk_out_1b)


    ### Functions for registering and handling IO

    def register_out_cb(self, outaddr: int, outfunc):
        self.outcb[outaddr] = outfunc

    def register_in_cb(self, inaddr: int, infunc):
        self.incb[inaddr] = infunc

    def handle_io_in(self, value) -> int:
        reg = value >> 8
        inaddr = value & 0xFF
        if inaddr in self.incb:
            return self.incb[inaddr]()
        else:
            print(f'IO - unregistered input address 0x{inaddr:02x}, exiting')
            sys.exit()

    def handle_io_out(self, outaddr, outval):
        if outaddr in self.outcb:
            self.outcb[outaddr](outval)
        else:
            print(f'IO - unregistered output address 0x{outaddr:02x} (0x{outval:02x})')
            #sys.exit()


    ### Specific functions

    ### Display

    def handle_display_in(self) -> int:
        print('IO - display status: 0')
        return 0


    def handle_display_out(self, val) -> str:
        if isprintable(val):
            print(f"IO - display out {val} '{chr(val)}'")
            self.displaystr += chr(val)
        else:
            print(f"IO - display out {val}")


    def handle_display_out_ctrl(self, val) -> str:
        if val == 0x05:
            desc = 'unblank, reset to (1,1)'
            self.displaystr += "\n-----\n"
        elif val == 0x08:
            desc = 'advance right (or new line)'
        else:
            desc = f'0x{val:02X}'
        print(f"IO - display control out - {desc}")


    ### Keyboard
    def handle_key_in_string(self) -> int:
        mystr = "ABCD"
        self.keyincount += 1
        retval = 0xd
        print(len(mystr), self.keyincount)
        if self.keyincount <= len(mystr):
            retval = ord(mystr[self.keyincount - 1])
            print(f'IO - key in (calls: {self.keyincount}): 0x{retval:02X}')
            return retval

        print(f'IO - key in return (calls: {self.keyincount}): 0x{retval:02X}')
        return retval


    def handle_key_in(self) -> int:
        self.keyincount += 1
        retval = 0
        if self.keyincount == 1:
            retval = 0x0F
        elif self.keyincount == 2:
            retval = 0x0E
        else:
            retval = 0x00
        print(f'IO - key in (calls: {self.keyincount}): 0x{retval:02X}')
        return retval


    def handle_key_out(self, val):
        if val == 0x04:
            desc = 'keyboard mode 2'
        else:
            desc = 'unknown'
        print(f'IO - key out: {desc}')


    ### Printer
    def handle_printer_in(self) -> int:
        print(f'IO - printer in (status) : 0 (no errors)')
        return 0


    def handle_printer_out_7(self, val):
        if val == 0xA0:
            desc = 'reset printer, raise ribbon'
        else:
            desc = 'unknown command'
        print(f'IO - printer out 7: {desc}')


    ### CIU ?
    def handle_ciu_out_0a(self, val):
        print(f'IO - CIU out (data out) (0x{val:02X})')


    def handle_ciu_out_0b(self, val):
        print(f'IO - CIU out (control 1) (0x{val:02X})')


    def handle_ciu_out_0c(self, val):
        if val == 0x81:
            desc = 'synchronous mode, master reset'
        else:
            desc = 'unspecified'
        print(f'IO - CIU out (control 2) {desc} (0x{val:02X})')


    def handle_ciu_in_0c(self):
        print('IO - CIU in (control 2): 0x00')
        return 0


    ### Disk control (from Q1 Assembler p. 52)
    def handle_disk_in_1a(self):
        print('IO - in (disk status): 0x00')
        return 0


    def handle_disk_out_1a(self, val):
        print(f'IO - disk control 1: NOP? (0x{val:02X})')


    def handle_disk_out_1b(self, val):
        print(f'IO - disk control 2: NOP? (0x{val:02X})')


if __name__ == '__main__':
    io = IO()
    # Display
    io.handle_io_out(0x03, 0xAA)
    assert io.handle_io_in(0x04) == 0
    io.handle_io_out(0x04, 0xAA)
    # Printer
    assert io.handle_io_in(0x05) == 0
    # Keyboard
    assert io.handle_io_in(0x01) == 0x0F
    assert io.handle_io_in(0x01) == 0x0E
    assert io.handle_io_in(0x01) == 0x00
    assert io.handle_io_in(0x01) == 0x00

    # Not sure
    assert io.handle_io_in(0x0C) == 0x00
    assert io.handle_io_in(0x1A) == 0x00
