

File System
===========
(Mostly unconfirmed)
By tracing CPU instructions and doing annotated disassembly I have
made the following colclusions and assumptions.

The disk consists of 77 tracks (0 - 76), each track having 2468 bytes. I've
decided that the 'index' position is located at the first byte of each
track. I assume that when selecting a disk Track 0 is the first track.

The disk controller issues a 'step' and a 'step direction' command.
In the documentation (Q1 ASM IO addresess p. 80), Bit 5 is the step command
and Bit 6 the 'direction' where  '1' is UP and 0 (assumed) DOWN. However
I have had to reverse this logic. Perhaps I should have started at Track 76?

I assume that the byte offset within a track is increasing on every read and
also that it wraps around to 0 when reading past the last byte.

The Q1 system seems to skip the first **2190** bytes on **track 0**, before
trying to look for ID and Data records. Other offsets (not confirmed) seem
to be present for the other tracks.

2024 08 02

There seem to be way more bytes ona track, perhaps upwards of 8000 bytes.

A major source of information on disk formats was found here:

https://github.com/MattisLind/q1decode/



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
