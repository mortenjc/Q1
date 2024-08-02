
import disks.debugdisk.t0 as ddt0

class FileSys:

    def __init__(self, tracks=35, bytes_per_track=9000):
        self.tracks = tracks
        self.bpt = bytes_per_track
        self.data = [[0x00 for B in range(self.bpt)] for A in range(self.tracks)]


    def rawrecord(self, track, offset, data):
        if data[0] == 0x9b and data[3] >= 0x30:
            fn = ""
            for i in range(8):
                fn += chr(data[3+i])
            print(f'INDEX:  {fn}')

        l1 = len(data)
        d = self.data[track]
        cksum = sum(data[1:]) & 0xff
        data.append(cksum)
        data.append(0x10)
        for i, e in enumerate(data):
            d[offset + i] = e
        assert l1 + 2 == len(data)
        return offset + len(data)


    def idrecord(self, track, offset, sector):
        oldoff = offset
        d = self.data[track]
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


    def le16(self, value):
        hi = value >> 8
        lo = value & 0xff
        return [lo, hi]


    def datareci(self, offset, name, reclen):
        assert len(name) == 8
        rec = []
        d = self.data[0]
        o = offset

        rec.append(0x9b)
        rec += self.le16(0x0000)     # rec number, zero on index
        for i, c in enumerate(name): # filename
            rec.append(ord(c))
        rec += self.le16(0x0001) # number of records
        rec += self.le16(reclen) # record length
        rec.append(0x00 )        # R/T ??
        rec.append(0x00)         # disk, 0 on index
        rec += self.le16(0x0001) # first track
        rec += self.le16(0x0001) # last track
        rec += self.le16(0xabcd) # unused
        rec += self.le16(0x0001) # recno bef. last

        rec += self.le16(0x1100)
        rec += self.le16(0x3322)
        rec += self.le16(0x5544)
        rec += self.le16(0x7766)
        rec += self.le16(0x9988)
        rec += self.le16(0xbbaa)
        rec += self.le16(0xddcc)
        rec += self.le16(0xffee)

        cksum = sum(rec) & 0xff
        rec.append(cksum)
        rec.append(0x10)
        for i, ch in enumerate(rec):
            d[offset + i] = ch
        return offset + len(rec)



fs1 = FileSys()
fs1.idrecord(0, 2189, 0)
fs1.idrecord(0, 2193, 0)
fs1.datareci(2197, 'MJC     ', 16)
fs1.idrecord(0, 2240, 0)
fs1.idrecord(0, 2244, 0)
fs1.datareci(2248, 'IBM     ', 16)


##
ddfs = FileSys()
# Create INDEX track
offset = 2189
for i, lst in enumerate(ddt0.t0):
    #print(offset + i)
    offset = ddfs.rawrecord(0, offset, lst)

if __name__ == '__main__':
    print(ddfs.data[0])
