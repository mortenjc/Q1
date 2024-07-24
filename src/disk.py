
import sys
from enum import Enum

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


class Disk:
    def __init__(self, disk, tracks=77, bpt=2468): # 2468 too small?
        self.disk = disk
        self.Tracks = tracks
        self.BytesPerTrack = bpt
        self.data = [[0x00 for B in range(self.BytesPerTrack)] for A in range(self.Tracks)]
        self.CurrentTrack = 0
        self.CurrentByte = 0
        self.BytesRead = 0

        self.idrecord(  2189, 17, 0)
        self.idrecord(  2193, 0, 0)
        self.datarecord(2197, 0, 25, 'MJC     ', data)
        self.idrecord(  2240, 0, 0)
        #self.idrecord(  2244, 0, 0)
        self.datarecord(2244, 0, 26, 'MJC     ', data)
        self.idrecord(  2287, 0, 0)
        self.idrecord(  2291, 0, 0)
        self.datarecord(2295, 0, 26, 'MJC     ', data)
        for i in range(100):
            self.data[0][2350+i] = 0x9e




    def idrecord(self, offset, track, sector):
        oldoff = offset
        d = self.data[track]
        d[offset] = 0x9e
        offset += 1
        d[offset] = track
        offset += 1
        d[offset] = sector
        offset += 1
        d[offset] = track + sector
        offset += 1
        d[offset] = 0x10
        offset += 1
        assert offset - oldoff == 5, offset - oldoff



    def datarecord(self, offset, track, recno, name, data):
        print(f'Disk {self.disk}: Data record at t{track}, b{offset}')
        o = offset
        d = self.data[track]
        assert len(name) == 8
        for i in range(len(data)):
            d[o] = data[i]
            o+=1
        for i in range(len(name)):
            d[offset + 3 + i] = ord(name[i])

        cksum = sum(d[offset:o-1])
        #print('cksum', cksum & 0xff)
        d[o - 2] = cksum & 0xff
        #print(d[offset:o])
        #print(offset, o, o - offset)
        return o




    def step(self, direction):
        print(f'disk {self.disk}, step {direction}, track {self.CurrentTrack}')
        self.CurrentByte = 0 # assumption
        if not direction: # DOWN
            if self.CurrentTrack == 76:
                return
            self.CurrentTrack += 1
        else: # UP
            if self.CurrentTrack == 0:
                return
            self.CurrentTrack -= 1


    def readbyte(self):
        track = self.CurrentTrack
        byte = self.CurrentByte
        #print(f'readbyte: disk {self.disk} track {self.CurrentTrack} byte {self.CurrentByte} value {self.data[track][byte]:02x}')
        assert 0 <= track < self.Tracks
        assert 0 <= byte < self.BytesPerTrack, byte
        if self.CurrentByte < self.BytesPerTrack - 1:
            self.CurrentByte += 1
        else:
            self.CurrentByte = 0
        self.BytesRead += 1
        return self.data[track][byte]


    def gettrackno(self):
        return self.CurrentTrack


    def isbusy(self):
        return True


doubleside = 0x02
track0     = 0x10
index      = 0x20
sdready    = 0x40
busy       = 0x80

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
            return
        side = val >> 7
        drive = (val & 0x7f)
        assert drive in [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40]
        i = 1
        while True:
            if drive == 1:
                break
            drive /= 2
            i += 1
        assert 1 <= drive <= 7
        assert 0 <= side <= 1
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
        status = sdready
        if self.disk.CurrentByte == 0:
            status += index
        if self.disk.isbusy():
            status += busy
        if track == 0:
            status += track
        # print(f'disk {self.disk.disk}, track {track}, CurrByte {self.disk.CurrentByte}, TotBytes {self.disk.BytesRead}, status {status:02x}')
        return status


if __name__ == "__main__":
    d = Disk(1)
    print(d.data)
