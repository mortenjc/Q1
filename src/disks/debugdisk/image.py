
import sys
sys.path.insert(0, '../..')

import disks.debugdisk.t0 as t0
import disks.debugdisk.t1 as t1
import disks.debugdisk.t2 as t2
import disks.debugdisk.t3 as t3
import filesys

##
ddfs = filesys.FileSys()
# Create INDEX track
offset = 0 # was 2189
for i, lst in enumerate(t0.data):
    offset = ddfs.rawrecord(0, offset, lst)

offset = 0
for i, lst in enumerate(t1.data):
    offset = ddfs.rawrecord(1, offset, lst)

offset = 0
for i, lst in enumerate(t2.data):
    offset = ddfs.rawrecord(2, offset, lst)

offset = 0
for i, lst in enumerate(t3.data):
    offset = ddfs.rawrecord(3, offset, lst)



if __name__ == '__main__':
    ddfs.datainfo(1, 30, 255)
    ddfs.datainfo(2, 30, 255)
    ddfs.datainfo(3, 30, 255)
    #s.data[1])
