
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

.. list-table:: IO Addresses
   :header-rows: 1

   * - Address
     - KIO
     - TBA
   * - 0x00 (IO)
     - RTC
     - Timer
   * - 0x01 (IO)
     - Keyb.
     - Keyb.
   * - 0x03
     - Disp. data (O)
     - Disp. data + status (IO)
   * - 0x04
     - Disp. ctrl (IO)
     - Disp. ctrl (O)
   * - 0x05 (IO)
     - Prt. data + status
     - Prt. data + status
   * - 0x06 (O)
     - Prt. ctrl 1
     - Prt. ctrl 1
   * - 0x07 (O)
     - Prt. ctrl 2
     - Prt. ctrl 2
   * - 0x08 (IO)
     - Dotm. Print
     -
   * - 0x09 (IO)
     - Disk R+W
     -
   * - 0x0a (IO)
     - Disk ctrl 1 + status
     -
   * - 0x0b (O)
     - Disk ctrl 2
     -
   * - 0x19 (IO)
     -
     - Disk R+W
   * - 0x1a (IO)
     -
     - Disk ctrl 1 + status
   * - 0x1b (O)
     -
     - Disk ctrl 2
   * - 0x1c (O)
     -
     - Disk ctrl 3
