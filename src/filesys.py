

class FileSys:

    # Possibilities according to "Q1 Lite system overview"
    # Tracks  Bytes per track
    #   35    4608
    #   77    8316
    def __init__(self, tracks=77, bytes_per_track=8316):
        self.tracks = tracks
        self.bpt = bytes_per_track
        self.data = [[0x00 for B in range(self.bpt)] for A in range(self.tracks)]


    def rawrecord(self, track, offset, data):
        if track == 0 and data[0] == 0x9b and data[3] >= 0x30:
            fn = ""
            for i in range(8):
                fn += chr(data[3+i])
            print(f'INDEX Record:  {fn}')

        d = self.data[track]
        cksum = sum(data[1:]) & 0xff
        for i, e in enumerate(data):
            d[offset + i] = e
        d[offset + i + 1] = cksum
        d[offset + i + 2] = 0x10
        return offset + len(data) + 2


    #
    def loadtracks(self, track_list): # assume contiguous, starting with t0
        for track, trackdata in enumerate(track_list):
            offset = 0
            for lst in trackdata.data:
                offset = self.rawrecord(track, offset, lst)


    def idrecord(self, track, offset, sector):
        d = self.data[track]
        d[offset+0] = 0x9e
        d[offset+1] = track
        d[offset+2] = sector
        d[offset+3] = (track + sector) & 0xff # cksum
        d[offset+4] = 0x10
        return offset + 5


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


    def trackinfo(self, track, records, record_size):
        d = self.data[track]
        for record in range(records):
            overhead = 8
            firstline = False
            i = 0
            offset = record * (record_size + overhead)
            assert d[offset + i] == 0x9e, f'{i=}, {d[offset + i]=}'
            i += 5
            assert d[offset + i] == 0x9b
            i += 1
            while 255 - i  >= 5:
                block_separator = d[offset + i]
                if block_separator == 0:
                    break
                if not firstline:
                    firstline = True
                    print(f'\nTrack {track}, Record {record}')

                i += 1
                addr = d[offset + i] + (d[offset + i + 1] << 8)
                i += 2
                bytecount = d[offset + i]
                i += 1
                print(f'separator 0x{block_separator:02x}: load {bytecount:3} bytes into address 0x{addr:04x}')
                brk = 0
                s0 = f'{addr:04x}'
                s1 = ''
                s2 = ''
                for j in range(bytecount):
                    val = d[offset + i]
                    i += 1
                    s1 += f'{val:02x} '
                    if 32 <= val <= 127:
                        s2 += chr(val)
                    else:
                        s2 += '.'
                    brk += 1
                    if brk == 16:
                        brk = 0
                        s0 = f'{addr:04x}'
                        print(s0, s1, s2)
                        addr += 16
                        s1 = ''
                        s2 = ''
                s0 = f'{addr:04x}'
                print(f'{s0} {s1:48} {s2}')
                print()



fs1 = FileSys()
fs1.idrecord(0, 2189, 0)
fs1.idrecord(0, 2193, 0)
fs1.datareci(2197, 'MJC     ', 16)
fs1.idrecord(0, 2240, 0)
fs1.idrecord(0, 2244, 0)
fs1.datareci(2248, 'IBM     ', 16)
