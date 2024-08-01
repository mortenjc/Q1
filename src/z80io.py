"""Module to provide IO hooks for the Q1 Lite"""

import disk

#

def isprintable(c):
    """True if character is printable ASCII"""
    return 0x20 <= c <= 0x7D


class IO:
    def __init__(self, m, fs):
        self.disk1 = disk.Control(1, fs)
        self.disk2 = disk.Control(2, fs)
        self.m = m
        self.incb = {}
        self.outcb = {}
        self.keyincount = 0
        self.keyin = 0
        self.displaystr = ""
        self.diskdata = 0x00
        self.diskstatus = 0x00
        self.go = 0
        self.verbose = False
        self.register_in_cb( 0x01, self.handle_key_in)
        self.register_out_cb(0x01, self.handle_key_out)

        self.register_out_cb(0x03, self.handle_display_out)
        self.register_out_cb(0x04, self.handle_display_out_ctrl)
        self.register_in_cb( 0x04, self.handle_display_in)

        self.register_in_cb( 0x05, self.handle_printer_in)
        self.register_out_cb(0x07, self.handle_printer_out_7)

        # Maybe these are really disk IO ?
        self.register_in_cb( 0x09, self.handle_disk_in_09)
        self.register_in_cb( 0x0a, self.handle_disk_in_0a)
        self.register_out_cb(0x09, self.handle_disk_out_09)
        self.register_out_cb(0x0a, self.handle_disk_out_0a)
        self.register_out_cb(0x0b, self.handle_disk_out_0b)
        # possibly not disk?
        self.register_in_cb(0x0c, self.handle_disk_in_0c)

        self.register_in_cb( 0x19, self.handle_disk_in_19)
        self.register_in_cb( 0x1a, self.handle_disk_in_1a)
        self.register_out_cb(0x1a, self.handle_disk_out_1a)
        self.register_out_cb(0x1b, self.handle_disk_out_1b)


    def print(self, s):
        if self.verbose:
            print(s)

    ### Functions for registering and handling IO

    def register_out_cb(self, outaddr: int, outfunc):
        self.outcb[outaddr] = outfunc

    def register_in_cb(self, inaddr: int, infunc):
        self.incb[inaddr] = infunc

    def handle_io_in(self, value) -> int:
        #reg = value >> 8
        inaddr = value & 0xFF
        if inaddr in self.incb:
            return self.incb[inaddr]()

        #print(f'IO - unregistered input address 0x{inaddr:02x} at pc {self.m.pc:04x}, exiting')
        #print()
        return 0
        #sys.exit()

    def handle_io_out(self, outaddr, outval):
        outaddr = outaddr & 0xff
        #print(f'handle_io_out({outaddr:02x},{outval:02x}({chr(outval)}))')
        if outaddr in self.outcb:
            self.outcb[outaddr](outval)
        else:
            self.print(f'IO - unregistered output address 0x{outaddr:02x} (0x{outval:02x})')
            #sys.exit()


    ### Specific functions

    ### Display

    def handle_display_in(self) -> int:
        self.print('IO - display status: 32 + 16 (Lite, 40 char)')
        return 32 + 16


    def handle_display_out(self, val) -> str:
        if isprintable(val):
            #self.print(f"IO out - display {val} '{chr(val)}'")
            self.displaystr += chr(val)
        else:
            pass #self.print(f"IO out - display (non printable){val}")


    def handle_display_out_ctrl(self, val) -> str:
        if val == 0x05:
            desc = 'unblank, reset to (1,1)'
            #self.displaystr += "\n"

            if len(self.displaystr) > 1:
                print(self.displaystr)
            self.displaystr = ""
        elif val == 0x08:
            desc = 'advance right (or new line)'
        else:
            desc = f'0x{val:02}'
        self.print(f"IO out - display control - {desc}")


    ### Keyboard
    def handle_key_in(self) -> int:
        retval = self.keyin
        self.keyin = 0
        if self.go:
            retval = 0x0e
            self.go = 0
        self.print(f'IO in  - key : 0x{retval:02x}')
        return retval


    # First version with magic values 0x0F and 0x0E
    # def handle_key_in(self) -> int:
    #     self.keyincount += 1
    #     retval = 0
    #     if self.keyincount == 1:
    #         retval = 0x0F
    #     elif self.keyincount == 2:
    #         retval = 0x0E
    #     else:
    #         retval = 0x00
    #     self.print(f'IO in  - key (calls: {self.keyincount}): 0x{retval:02x}')
    #     return retval


    def handle_key_out(self, val):
        if val == 0x04:
            desc = 'keyboard mode 2'
        else:
            desc = 'unknown'
        self.print(f'IO out - key - {desc}')


    ### Printer
    def handle_printer_in(self) -> int:
        self.print('IO in  - printer status -  0 (no errors)')
        return 0


    def handle_printer_out_7(self, val):
        if val == 0xA0:
            desc = 'reset printer, raise ribbon'
        else:
            desc = 'unknown command'
        self.print(f'IO out - printer control - {desc}')


    ### Disk 1? Data and Control
    ### From "Q1 ASM IO addresses usage Q1 Lite" p. 77 - 80
    def handle_disk_out_0a(self, val):
        if val != 0:
            self.print(f'IO out - disk1 (control 1 ) - (0x{val:02x})')
        self.disk1.control1(val)

    def handle_disk_out_0b(self, val):
        if val != 0:
            self.print(f'IO out - disk1 (control 2 ) - (0x{val:02x})')
        self.disk1.control2(val)


    def handle_disk_out_09(self, val):
        self.print(f'IO out - disk1 (data) - (0x{val:02x})')


    def handle_disk_in_0a(self):
        retval = self.disk1.status()
        t = self.disk1.disk.current_track
        b = self.disk1.disk.current_byte
        self.print(f'IO in  - disk1 (0xa) (status): 0x{retval:02x}, t{t}, b{b}')
        return retval

    def handle_disk_in_09(self):
        t = self.disk1.disk.current_track
        b = self.disk1.disk.current_byte
        retval = self.disk1.data_in()
        print(f'IO in  - disk1 (0x9) (data): 0x{retval:02x}, t{t}, b{b}')
        return retval

    # possibly not disk, could be rs232
    def handle_disk_in_0c(self):
        self.print(f'IO in  - disk1 ???????????? - (0x00)')
        return 0


    ### Disk 2 Data and Control
    ### From "Q1 Assembler" p. 52 - 54
    def handle_disk_in_19(self):
        retval =self.disk2.data_in()
        self.print(f'IO in  - disk2 (data): {retval}')
        return retval

    def handle_disk_in_1a(self):
        retval = self.disk2.status()
        self.print(f'IO in  - disk2 (status): {retval}')
        return retval


    def handle_disk_out_1a(self, val):
        if val != 0:
            self.print(f'IO out - disk2 (control 1 ) - (0x{val:02x})')
        self.disk2.control1(val)


    def handle_disk_out_1b(self, val):
        if val != 0:
            self.print(f'IO out - disk2 (control 2 ) - (0x{val:02x})')
        self.disk2.control2(val)
