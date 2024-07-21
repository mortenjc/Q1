


class ROS:

    def __init__(self, mem):
        self.m = mem

        self.addrs = {
            "0x4080" : "RA (jump to start of prg)",
            "0x4083" : "   (jump to interrupt processing)",
            "0x4086" : "   (wait for keyboard or printer)",
            "0x4089" : "PLC",
            "0x408a" : "PTC",
            "0x408b" : "POS",
            "0x408d" : "RIB",
            "0x408e" : "Unused",
            "0x408f" : "HEXX",
            "0x4090" : "INSF",
            "0x4091" : "FUNKEY",
            "0x4092" : "TOOK",
            "0x4093" : "CURSE",
            "0x4094" : "UNDER",
            "0x4095" : "KSIZ",
            "0x4096" : "OSEZ (# chars used for display)",
            "0x4098" : "ACTK",
            "0x4099" : "THERE (addr for disk transfer)",
            "0x409b" : "NRT   (disk record count)",
            "0x409c" : "SNRT  (# recs to be transfd)",
            "0x409d" : "ERC   (disk error count)",
            "0x409e" : "INDEX (curr. rec. # on index)",
            "0x40a0" : "DISK  (selected disk drive #)",
            "0x40a1" : "TRKS  (track # for drive 1)",
            "0x40a2" : "TRKS  (track # for drive 2)",
            "0x40a3" : "TRKS  (track # for drive 3)",
            "0x40a4" : "TRKS  (track # for drive 4)",
            "0x40a5" : "AD (access denined)",
            "0x40a6" : "Record Number",
            "0x40a8" : "Number of Records",
            "0x40aa" : "Record Length",
            "0x40ac" : "Records/Track",
            "0x40ad" : "Disk #",
            "0x40ae" : "First Track (LFILE)",
            "0x40b0" : "Last Track (LFILE)",
            "0x40b2" : "Unused (LFILE)",
            "0x40b4" : "Rec.# bef. last op (LFILE)",
            "0x40b6" : "PART1 (length to be transferred)",
            "0x40b8" : "PART2 unused length",

            "0x40d0" : "Record Number (LFILE)",
            "0x40d2" : "File Name (LFILE)",
            "0x40da" : "Number of Records (LFILE)",
            "0x40dc" : "Record Length (LFILE)",
            "0x40de" : "Records/Track (LFILE)",
            "0x40df" : "Disk # (LFILE)",
            "0x40e0" : "First Track (LFILE)",
            "0x40e2" : "Last Track (LFILE)",
            "0x40e4" : "Unused (LFILE)",
            "0x40e6" : "Rec.# bef. last op (LFILE)",
        }



    def index(self):
        m = self.m
        print(f'####   INDEX x40a6 - 40b5   ####')
        print(f'0x40a6/7 - Record Number      {m.getu16(0x40a6)}')
        print(f'0x40a8/9 - Number of Records  {m.getu16(0x40a8)}')
        print(f'0x40aa/b - Record Length      {m.getu16(0x40aa)} 0x{m.getu16(0x40aa):02x}')
        print(f'0x40ac   - Records/Track      {m.getu8(0x40ac)}')
        print(f'0x40ad   - Disk#              {m.getu8(0x40ad)}')
        print(f'0x40ae/f - First Track        {m.getu16(0x40ae)}')
        print(f'0x40b0/1 - Last Track         {m.getu16(0x40b0)}')
        print(f'0x40b2/3 - unused             {m.getu16(0x40b2)}')
        print(f'0x40b4/5 - Rec# bef. last op. {m.getu16(0x40b4)}')
        print()

    def disk(self):
        m = self.m
        print(f'#### DISK vars x4099 - 40a5   ####')
        print(f'0x4099/a - THERE (addr for disk transfer) 0x{m.getu16(0x4099):04x}')
        print(f'0x409b   - NRT   (disk record count)      {m.getu8(0x409b)}')
        print(f'0x409c   - SNRT  (# recs to be transfd)   {m.getu8(0x409c)}')
        print(f'0x409d   - ERC   disk error count         {m.getu8(0x409d)}')
        print(f'0x409e/f - INDEX curr. rec. # on index    {m.getu16(0x409e)}')
        print(f'0x40a1   - TRKS  track # for drive 1      {m.getu8(0x40a1)}')
        print(f'0x40a2   - TRKS  track # for drive 2      {m.getu8(0x40a2)}')
        print(f'0x40a3   - TRKS  track # for drive 3      {m.getu8(0x40a3)}')
        print(f'0x40a4   - TRKS  track # for drive 4      {m.getu8(0x40a4)}')
        print(f'0x40b6/7 - PART1 length to be transferred {m.getu16(0x40b6)}')
        print(f'0x40b8/9 - PART2 unused length            {m.getu16(0x40b8)}')
        print()



    def filename(self, addr):
        name = ''
        for i in range(8):
            name += chr(self.m.getu8(addr+i))
        return name

    def file(self):
        m = self.m
        print(f'####   LFILE x40d0 - 40e7   ####')
        print(f'0x40d0/1 - Record Number      {m.getu16(0x40d0)}')
        print(f'0x40d2   - File name          "{self.filename(0x40d2)}"')
        print(f'0x40da/b - Number of Records  {m.getu16(0x40da)}')
        print(f'0x40dc/d - Record Length      {m.getu16(0x40dc)} 0x{m.getu16(0x40dc):02x}')
        print(f'0x40de   - Records/Track      {m.getu8(0x40de)}')
        print(f'0x40df   - Disk#              {m.getu8(0x40df)}')
        print(f'0x40e0/1 - First Track        {m.getu16(0x40e0)}')
        print(f'0x40e2/3 - Last Track         {m.getu16(0x40e2)}')
        print(f'0x40e4/5 - unused             {m.getu16(0x40e4)}')
        print(f'0x40e6/7 - Rec# bef. last op. {m.getu16(0x40e6)}')
        print()
