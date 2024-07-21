



INDEX FILE
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
