
# for now assume disk/drive 1 only, side 0 only


class Disk:
    def __init__(self, diskno, fs): #
        self.diskno = diskno
        self.tracks = fs.tracks
        self.bytes_per_track = fs.bpt
        self.data = fs.data
        self.marks = fs.marks
        self.current_track = 0
        self.current_byte = 0
        self.bytes_read = 0


    def step(self, direction):
        self.current_byte = 0 # assumption
        if direction: # UP
            msg = f'disk {self.diskno}, step up 0x{direction:02x}'
            msg += f', track {self.current_track} -> {self.current_track + 1}'
            print(msg)
            self.current_track = (self.current_track + 1) % self.tracks
        else: # DOWN
            msg = f'disk {self.diskno}, step down {direction:02x}'
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

    # Very unsure about the correct implementation
    def isbusy(self):
        # Idea 1 - always return true even when not on a mark. This approach
        # is slow but 'works' except currently files are not found during KEY
        # search
        return True

        # Idea 2 - only return True when on a mark, current_byte is only
        # icremented on reads. This one seems to get stuck permanently
        # if self.current_byte in self.marks[self.current_track]:
        #     return True
        # return False

        # Idea 3 - assume disk looks for the next mark and advances current_byte
        # always returns True. Only finds one case of good checksum
        while self.current_byte not in self.marks[self.current_track]:
            self.current_byte = (self.current_byte + 1) % self.bytes_per_track
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
        self.selected_drive = 0


    def data_in(self) -> int:
        val = self.disk.readbyte()
        # print(f'disk {self.disk.disk}, track {self.disk.current_track}, ' + \
        #       f'byte {self.disk.current_byte}, val {val:02x}, count {self.disk.bytes_read}')
        return val


    def control1(self, val):
        if val == 0:
            self.disk.current_byte = 0
            return
        #side = val >> 7
        drive = val #& 0x7f
        assert drive in [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80], f'val: 0x{val:02x}'
        i = 1
        while True:
            if drive == 1:
                break
            drive /= 2
            i += 1
        #assert side == 0
        self.selected_drive = i


    def control2(self, val):
        stepdir = val & 0x40
        if val & 0x20: # Step
            self.disk.step(stepdir)
        if val & 0x80:
            self.write = 1


    def status(self):
        if self.disk.diskno == 2:
            return 0 # Lite, for Magnus use 0x01
        assert self.disk.diskno == 1
        track = self.disk.current_track
        status = 0
        if self.selected_drive == 1:
            status = statusbits["sdready"]
        else:
            print(f'disk {self.disk.diskno} drive {self.selected_drive} not ready')
        if self.disk.current_byte == 0:
            status += statusbits["index"]
        if self.disk.isbusy():
            status += statusbits["busy"]
        if track == 0:
            status += statusbits["track0"]
        #print(f'disk {self.disk.disk}, track {track}, CurrByte {self.disk.current_byte}, TotBytes {self.disk.bytes_read}, status {status:02x}')
        return status
