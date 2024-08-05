
import sys
sys.path.insert(0, '../..')

from disks.fluxsamples import t0, t1, t2
import filesys


fluxfs = filesys.FileSys()
fluxfs.loadtracks([t0, t1, t2]) #


if __name__ == '__main__':
    #fluxfs.trackinfo(1, 82, 79)
    fluxfs.trackinfo(2, 82, 79)
