
2024 07 22
----------

In order to initialise the file system I fill out 55 records on each track
with information compatible with figure 2 on page 17 (same document):

Each record looks like this

|0x9e|Trk|Sect|Csum|0xa|x00 x00 x00 x00 x00 x00|0x9b|Trk|Sect|Csum|0xa|1234|x00 x00 x00 x00 x00 x00|

So far I have seen no definition of what a sector is. So I am assuming the above
record is two sectors, one starting with 0x9e (ID Record) and one starting with 0x9b
'(Data Record)'.

This clearly need more work, but it is a start.

2024 07 24
----------

The above data format was wrong. The end-of-record value is 0x10, not 0xa. Also the six consecutive
0x00 bytes are not actually returned by the controller.

Despite the picture on page 17, it seems that when reading a file desctiptor in a
data record (0x9b), the checksum comes AFTER the FD and User data:

|0x9b| FD data | User data | Csum | 0x10

Also, possibly due to other errors it looks like two sets of 0x9e blocks should come
before the 0x9b:

[0x9e ...] [0x9e ...] [0x9b ...]

Finally, there does not seem to be a 0x10 after the ID records

After messing with the file system (should probably implement a loader soon) I
at least get the OS to acknowledge that the disk I made was bad :-)

.. code-block:: console

  DISK OPEN
  DISK KEY
  DISK READ
  disk 1, step 0, track 0
  disk 1, step 0, track 1
  ...
  disk 1, step 0, track 28
  disk 1, step 0, track 29
  disk 1, step 0, track 30
  DISK (error) REPORT

  FORMAT ERR
   ON
  MJC



Index File
==========
Figure from ROS manual p. 17 gave a hint, but INDEX file does not
use the File Name field. The INDEX file descriptor resides in
the range 0x40a6 - 0x40b5.

.. list-table:: File Descriptor
   :header-rows: 1

   * - Address
     - Name
     - Description
   * - 0x40a6
     - Record Number
     -
   * - 0x40a8
     - Number of Records
     -
   * - 0x40aa
     - Record Length
     -
   * - 0x40ac
     - Records/Track
     -
   * - 0x40ad
     - Disk #
     - 0 for INDEX
   * - 0x40ae
     - First Track
     -
   * - 0x40b0
     - Last Track
     -
   * - 0x40b2
     - Unused
     -
   * - 0x40b4
     - Rec# bef. last op.
     -


LFILE
=====

Information about the file to be loaded (LFILE in ROS Manual)resides in
the address range 0x40d0 - 0x40e7.

.. list-table:: File Descriptor
   :header-rows: 1

   * - Address
     - Name
     - Description
   * - 0x40d0
     - Record Number
     -
   * - 0x40d2
     - File Name
     -
   * - 0x40da
     - Number of Records
     -
   * - 0x40dc
     - Record Length
     -
   * - 0x40de
     - Records/Track
     -
   * - 0x40df
     - Disk #
     -
   * - 0x40e0
     - First Track
     -
   * - 0x40e2
     - Last Track
     -
   * - 0x40e4
     - Unused
     -
   * - 0x40e6
     - Rec# bef. last op.
     -
