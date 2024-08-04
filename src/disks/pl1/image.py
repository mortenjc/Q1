
import sys
sys.path.insert(0, '../..')

#import disks.pl1.t0 as t0
import disks.pl1.t1 as t1

import filesys

##
pl1fs = filesys.FileSys()
# Create INDEX track
# offset = 0 # was 2189
# for i, lst in enumerate(t0.data):
#     offset = ddfs.rawrecord(0, offset, lst)

offset = 0
for i, lst in enumerate(t1.data):
    offset = pl1fs.rawrecord(1, offset, lst)

# offset = 0
# for i, lst in enumerate(t2.data):
#     offset = ddfs.rawrecord(2, offset, lst)
#
# offset = 0
# for i, lst in enumerate(t3.data):
#     offset = ddfs.rawrecord(3, offset, lst)



if __name__ == '__main__':
    pl1fs.datainfo(1, 30, 255)
