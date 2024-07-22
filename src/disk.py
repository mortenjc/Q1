
import sys
from enum import Enum

# for now assume disk 1 only, drive 1 only, side 0 only

class Disk:
    def __init__(self, disk, tracks=77, bpt=2468): #
        self.disk = disk
        self.Tracks = tracks
        self.BytesPerTrack = bpt
        self.data = [[0x00 for B in range(self.BytesPerTrack)] for A in range(self.Tracks)]
        self.CurrentTrack = 0
        self.CurrentByte = 0
        self.BytesRead = 0
        for track in range(77):
            for block in range(55):
                step = block * 26
                self.data[track][step + 0] = 0x9e # ID Record
                self.data[track][step + 1] = track
                self.data[track][step + 2] = block * 2 # sector
                self.data[track][step + 3] = 0x56 # cksum
                self.data[track][step + 4] = 10   #
                self.data[track][step + 5] = 0 # GAP
                self.data[track][step + 6] = 0 #
                self.data[track][step + 7] = 0 #
                self.data[track][step + 8] = 0 #
                self.data[track][step + 9] = 0 #
                self.data[track][step + 10] = 0 #

                self.data[track][step + 11] = 0x9b # Data Record
                self.data[track][step + 12] = track
                self.data[track][step + 13] = block * 2 + 1
                self.data[track][step + 14] = 0x56 # cksum
                self.data[track][step + 15] = 10

                self.data[track][step + 16] = 0x31
                self.data[track][step + 17] = 0x32
                self.data[track][step + 18] = 0x33
                self.data[track][step + 19] = 0x34

                self.data[track][step + 20] = 0 # GAP
                self.data[track][step + 21] = 0 #
                self.data[track][step + 22] = 0 #
                self.data[track][step + 23] = 0 #
                self.data[track][step + 24] = 0 #
                self.data[track][step + 25] = 0 #



    def step(self, direction):
        print(f'disk {self.disk}, step {direction}, track {self.CurrentTrack}')
        self.CurrentByte = 0
        if not direction: # DOWN
            if self.CurrentTrack == 77:
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
        assert 0 <= byte < self.BytesPerTrack
        if self.CurrentByte < self.BytesPerTrack:
            self.CurrentByte += 1
        if self.CurrentByte == self.BytesPerTrack: # wrap
            self.CurrentByte = 0
        self.BytesRead += 1
        return self.data[track][byte]


    def gettrackno(self):
        return self.CurrentTrack


    def isbusy(self):
        if self.CurrentByte == 0 or self.BytesRead > 2468:
            return True
        return False


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

    def control2(self, val):
        stepdir = val & 0x40
        if val & 0x20: # Step
            self.disk.step(stepdir)
        if val & 0x80:
            self.write = 1


    def status(self):
        track = self.disk.CurrentTrack
        status = sdready # + index
        if self.disk.isbusy():
            status += busy
        if track == 0:
            status += track
        #print(f'disk {self.disk.disk}, track {track}, CurrByte {self.disk.CurrentByte}, TotBytes {self.disk.BytesRead}, status {status:02x}')
        return status


if __name__ == "__main__":
    d = Disk(1)
    print(d.data)
