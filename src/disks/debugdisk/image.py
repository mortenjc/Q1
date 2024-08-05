
import sys
sys.path.insert(0, '../..')

from disks.debugdisk import t0, t1, t2, t3
import filesys


ddfs = filesys.FileSys()
ddfs.loadtracks([t0, t1, t2, t3])


if __name__ == '__main__':
    ddfs.trackinfo(1, 30, 255)
    ddfs.trackinfo(2, 30, 255)
    ddfs.trackinfo(3, 30, 255)
    #s.data[1])
