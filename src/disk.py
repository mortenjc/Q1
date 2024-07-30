
#from enum import Enum
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
    def __init__(self, disk, tracks=35, bpt=4608): #
        self.disk = disk
        self.Tracks = tracks
        self.BytesPerTrack = bpt
        self.data = [[0x00 for B in range(self.BytesPerTrack)] for A in range(self.Tracks)]
        self.CurrentTrack = 0
        self.CurrentByte = 0
        self.BytesRead = 0

        if 1: # jdc rom addresses
            self.idrecord(  0, 2189, 0, 0)
            self.datarecord(0, 2193, 0, 'XXX     ', data)
            self.idrecord(  0, 2194, 0, 0)
            self.datarecord(0, 2198, 0, 'MJC     ', data)
            self.idrecord(  0, 2241, 0, 0)
            self.idrecord(  0, 2245, 0, 0)
            self.datarecord(0, 2249, 0, 'YYY     ', data)
            self.idrecord(  0, 2292, 0xff, 0x00)


    def idrecord(self, writetotrack, offset, track, sector):
        oldoff = offset
        d = self.data[writetotrack]
        d[offset] = 0x9e
        offset += 1
        d[offset] = track
        offset += 1
        d[offset] = sector
        offset += 1
        d[offset] = track + sector # cksum
        offset += 1
        d[offset] = 0x10
        offset += 1
        assert offset - oldoff == 5, offset - oldoff
        return offset


    def datarecord(self, track, offset, recno, name, data):
        print(f'Disk {self.disk}: Data record at t{track}, b{offset}')
        o = offset
        d = self.data[track]
        assert len(name) == 8
        for i in range(len(data)):
            d[o] = data[i]
            o+=1
        for i in range(len(name)):
            d[offset + 3 + i] = ord(name[i])

        d[1] = recno & 0xff
        d[2] = recno >> 8

        cksum = sum(d[offset:o-1])
        d[o - 2] = cksum & 0xff
        return o


    def step(self, direction):
        self.CurrentByte = 0 # assumption
        if direction: # UP
            msg = f'disk {self.disk}, step up 0x{direction:02x}'
            msg += f', track {self.CurrentTrack} -> {self.CurrentTrack + 1}'
            print(msg)
            if self.CurrentTrack == self.Tracks - 1:
                return
            self.CurrentTrack += 1
        else: # DOWN
            msg = f'disk {self.disk}, step down {direction:02x}'
            msg += ', track {self.CurrentTrack} -> {self.CurrentTrack - 1}'
            print(msg)
            if self.CurrentTrack == 0:
                return
            self.CurrentTrack -= 1


    def readbyte(self):
        track = self.CurrentTrack
        byte = self.CurrentByte
        assert 0 <= track < self.Tracks
        assert 0 <= byte < self.BytesPerTrack, byte
        self.CurrentByte = (self.CurrentByte + 1) % self.BytesPerTrack
        self.BytesRead += 1
        return self.data[track][byte]


    def gettrackno(self):
        return self.CurrentTrack


    def isbusy(self):
        return True



# dbleside   = 0x02
# track0     = 0x10
# index      = 0x20
# sdready    = 0x40
# busy       = 0x80

statusbits = {
"dbleside"   : 0x02,
"track0"     : 0x10,
"index"      : 0x20,
"sdready"    : 0x40,
"busy"       : 0x80
}

class Control:
    def __init__(self, diskno):
        self.track0 = 0
        self.trackdir = 0
        self.write = 0
        self.disk = Disk(diskno)


    def data_in(self) -> int:
        val = self.disk.readbyte()
        # print(f'disk {self.disk.disk}, track {self.disk.CurrentTrack}, ' + \
        #       f'byte {self.disk.CurrentByte}, val {val:02x}, count {self.disk.BytesRead}')
        return val


    def control1(self, val):
        if val == 0:
            self.disk.CurrentByte = 0
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
        self.CurrentByte = 0 # ?

    def control2(self, val):
        stepdir = val & 0x40
        if val & 0x20: # Step
            self.disk.step(stepdir)
        if val & 0x80:
            self.write = 1


    def status(self):
        track = self.disk.CurrentTrack
        status = statusbits["sdready"]
        if self.disk.CurrentByte == 0:
            status += statusbits["index"]
        if self.disk.isbusy():
            status += statusbits["busy"]
        if track == 0:
            status += statusbits["track0"]
        #print(f'disk {self.disk.disk}, track {track}, CurrByte {self.disk.CurrentByte}, TotBytes {self.disk.BytesRead}, status {status:02x}')
        return status


if __name__ == "__main__":
    testdisk = Disk(1)
    print(testdisk.data)
