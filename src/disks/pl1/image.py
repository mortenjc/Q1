
import sys
sys.path.insert(0, '../..')

from disks.pl1 import t1, t2
import filesys


pl1fs = filesys.FileSys()

offset = 0
for i, lst in enumerate(t1.data):
    offset = pl1fs.rawrecord(1, offset, lst)

offset = 0
for i, lst in enumerate(t2.data):
    offset = pl1fs.rawrecord(2, offset, lst)


if __name__ == '__main__':
    track = filesys.Track()
    track.info(1, pl1fs.data[1], 30, 255)
    track.info(2, pl1fs.data[2], 30, 255)
