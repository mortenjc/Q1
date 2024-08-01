


class filesys:

    def __init__(self, tracks=35, bytes_per_track=4608):
        self.tracks = tracks
        self.bpt = bytes_per_track
        self.data = [[0x00 for B in range(self.bpt)] for A in range(self.tracks)]


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
        print(f'Data record at t{track}, b{offset}')
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


    def w16(self, track, offset, value):
        hi = value >> 8
        lo = value & 0xff
        self.data[track][offset + 0] = lo
        self.data[track][offset + 1] = hi


    def datareci(self, offset, name, reclen):
        assert len(name) == 8
        d = self.data[0]
        o = offset

        d[o] = 0x9b
        o += 1
        self.w16(0, o, 0x0000)        # rec number, zero on index
        for i, c in enumerate(name):  # filename
            d[o + 2 + i] = ord(c)
        self.w16(0, o + 0xa, 0x0001)  # number of records
        self.w16(0, o + 0xc, reclen)  # record length
        d[offset + 0xe] = 0x00        # R/T ??
        d[offset + 0xf] = 0x00        # disk, 0 on index
        self.w16(0, o + 0x10, 0x0001) # first track
        self.w16(0, o + 0x12, 0x0001) # last track
        self.w16(0, o + 0x14, 0xabcd) # unused
        self.w16(0, o + 0x16, 0x0001) # recno bef. last

        self.w16(0, o + 0x18, 0x1100)
        self.w16(0, o + 0x1a, 0x3322)
        self.w16(0, o + 0x1c, 0x5544)
        self.w16(0, o + 0x1e, 0x7766)
        self.w16(0, o + 0x20, 0x9988)
        self.w16(0, o + 0x22, 0xbbaa)
        self.w16(0, o + 0x24, 0xddcc)
        self.w16(0, o + 0x26, 0xffee)

        cksum = sum(d[offset:offset+41]) & 0xff
        d[o + 0x28] =  cksum
        d[o + 0x29] = 0x10
        d[o + 0x30] = 0x00
        return offset + 41



fs1 = filesys()
fs1.idrecord(0, 2189, 0, 0)
fs1.idrecord(0, 2193, 0, 0)
fs1.datareci(2197, 'MJC     ', 16)
fs1.idrecord(0, 2240, 0, 0)
fs1.idrecord(0, 2244, 0, 0)
fs1.datareci(2248, 'IBM     ', 16)
