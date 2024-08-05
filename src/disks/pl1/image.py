
import sys
sys.path.insert(0, '../..')

from disks.pl1 import t1
import filesys


pl1fs = filesys.FileSys()

offset = 0
for i, lst in enumerate(t1.data):
    offset = pl1fs.rawrecord(1, offset, lst)


if __name__ == '__main__':
    pl1fs.trackinfo(1, 30, 255)
