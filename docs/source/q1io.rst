
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
   * - 0x10 (IO)
     -
     - Data R+W
   * - 0x11 (IO)
     -
     - ctrl 1, status 1
   * - 0x12 (IO)
     -
     - ctrl 2, status 2
   * - 0x13 (O)
     -
     - ctrl 3
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


Display
-------

When reading the Display status, TBA reports **Bit 7** as busy.
However KIO has the following:

**Bit 6** = 0 for 12 line = 1 for 6 line
**Bit 5** = 1 for LITE; = 0 for LMC

Neither seem to be complete as the code for the JMC roms (add references)
at 0x2A0 seems to be testing **Bit 3** to select a 80 character width and
**Bit 4** to select 40 bytes:

        <<<<< Display width? >>>>>
        02A0 DB 04        ; in a, (0x4)     |
        02A2 CB 5F        ; bit 0x3, a      |
        02A4 3E 50        ; ld a, 0x50      |
        02A6 C0           ; ret nz          |
        02A7 DB 04        ; in a, (0x4)     |
        02A9 CB 67        ; bit 0x4, a      |
        02AB 3E 28        ; ld a, 0x28      |
        02AD C0           ; ret nz          |
        02AE C6 07        ; add a, 0x7      |
        02B0 C9           ; ret             |
