
from enum import Enum

# for now assume disk 1 only, drive 1 only, side 0 only

class Control:
    def Status(Enum):
        doubleside = 0x02
        track0     = 0x10
        index      = 0x20
        sdready    = 0x40
        busy       = 0x80

    def __init__(self):
        self.track0 = 0
        self.pos = 0
        self.write = 0
        self.data = "AaBbCcDd"


    def control1(self, val):
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



    def status(self):
        return Status.sdready + Status.index + Status.track0
