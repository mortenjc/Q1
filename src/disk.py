
# for now assume disk 1 only, drive 1 only, side 0 only

data = [ 0x9b,
         0x00, 0x00, # Record number
         ord('A'), ord('B'), ord('C'), ord('D'),
         ord('E'), ord('F'), ord('G'), ord('H'),
         0x01, 0x00, # Number of records
         0x0a, 0x00, # Record len
         0x00, 0x00, # R/T, Disk number
         0x00, 0x00, # first track
         0x00, 0x00, # last track
         0xab, 0xcd, # unused
         0x00, 0x00, # rec bef last
         0x01, 0x00, 0x70, 0x0c, 0x00, 0x01, 0x02, 0x03, # data
         0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b,
         0x00,       # cksum
         0x10        # end marker
         ]



# Possibilities according to "Q1 Lite system overview"
# Tracks  Bytes per track
#   35    4608
#   77    8316

class Disk:
    def __init__(self, disk, fs): #
        self.disk = disk
        self.tracks = fs.tracks
        self.bytes_per_track = fs.bpt
        self.data = fs.data
        self.current_track = 0
        self.current_byte = 0
        self.bytes_read = 0


    def step(self, direction):
        self.current_byte = 0 # assumption
        if direction: # UP
            msg = f'disk {self.disk}, step up 0x{direction:02x}'
            msg += f', track {self.current_track} -> {self.current_track + 1}'
            print(msg)
            self.current_track = (self.current_track + 1) % self.tracks
        else: # DOWN
            msg = f'disk {self.disk}, step down {direction:02x}'
            msg += f', track {self.current_track} -> {self.current_track - 1}'
            print(msg)
            if self.current_track == 0:
                return
            self.current_track -= 1


    def readbyte(self):
        track = self.current_track
        byte = self.current_byte
        assert 0 <= track < self.tracks
        assert 0 <= byte < self.bytes_per_track, byte
        self.current_byte = (self.current_byte + 1) % self.bytes_per_track
        self.bytes_read += 1
        return self.data[track][byte]


    def gettrackno(self):
        return self.current_track


    def isbusy(self):
        return True


statusbits = {
    "dbleside"   : 0x02,
    "track0"     : 0x10,
    "index"      : 0x20,
    "sdready"    : 0x40,
    "busy"       : 0x80
}

class Control:
    def __init__(self, diskno, fs):
        self.track0 = 0
        self.trackdir = 0
        self.write = 0
        self.disk = Disk(diskno, fs)


    def data_in(self) -> int:
        val = self.disk.readbyte()
        # print(f'disk {self.disk.disk}, track {self.disk.current_track}, ' + \
        #       f'byte {self.disk.current_byte}, val {val:02x}, count {self.disk.bytes_read}')
        return val


    def control1(self, val):
        if val == 0:
            self.disk.current_byte = 0
            return
        side = val >> 7
        drive = val & 0x7f
        assert drive in [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40], drive
        i = 1
        while True:
            if drive == 1:
                break
            drive /= 2
            i += 1
        assert side == 0
        assert drive == 1
        self.current_byte = 0 # ?


    def control2(self, val):
        stepdir = val & 0x40
        if val & 0x20: # Step
            self.disk.step(stepdir)
        if val & 0x80:
            self.write = 1


    def status(self):
        track = self.disk.current_track
        status = statusbits["sdready"]
        if self.disk.current_byte == 0:
            status += statusbits["index"]
        if self.disk.isbusy():
            status += statusbits["busy"]
        if track == 0:
            status += statusbits["track0"]
        #print(f'disk {self.disk.disk}, track {track}, CurrByte {self.disk.current_byte}, TotBytes {self.disk.bytes_read}, status {status:02x}')
        return status
