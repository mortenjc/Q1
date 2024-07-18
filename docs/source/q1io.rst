
IO Addresses
============



The two main sources of information for IO is two versions of the
"The Q1 Assembler" document.

Karl's version (KIO) (only pages 64 to 80), dated 8/78.

https://www.peel.dk/Q1/pdf/Q1%20ASM%20IO%20addresses%20usage%20Q1%20Lite.pdf

From TheByteAttic(TBA) (whole document, marked preliminary), no date.

Pages 47 to 62 describes the IO addresses
https://github.com/TheByteAttic/Q1/blob/main/Original%20Documentation/Q1%20Assembler.pdf


Differences
-----------

The two document has some differences. For example the known addresses are

| Addresses  |  0x01  |  0x09 |
| ---------- | ------ | ----- |
| A          |  B     |  C    |

.. list-table:: Addresses

   :header-rows: 1

   * - Version
     - 0x00 (IO)
     - 0x01 (IO)
     - 0x03
     - 0x04
     - 0x05 (IO)
     - 0x06 (O)
     - 0x07 (O)
     - 0x08 (IO)
     - 0x09 (IO)
     - 0x0a (IO)
     - 0x0b (O)
     - 0x19 (IO)
     - 0x1a (IO)
     - 0x1b (O)
     - 0x1c (O)
   * - KIO
     - RTC
     - Keyb.
     - Disp. data (O)
     - Disp. ctrl (IO)
     - Prt. data + status
     - Prt. ctrl 1
     - Prt. ctrl 2
     - Dotm. Print
     - Disk R+W
     - Disk ctrl 1 + status
     - Disk ctrl 2
     - n/a
     - n/a
     - n/a
     - n/a
   * - TBA
     - Timer
     - Keyb.
     - Disp. data + status (IO)
     - Disp. ctrl (O)
     - Prt. data + status
     - Prt. ctrl 1
     - Prt. ctrl 2
     - n/a
     - n/a
     - n/a
     - n/a
     - Disk R+W
     - Disk ctrl 1 + status
     - Disk ctrl 2
     - Disk ctrl 3
