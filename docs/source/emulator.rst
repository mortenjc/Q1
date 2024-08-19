

Emulator
========

The **emulator** runs the program and displays the runtime status
of the program counter, registers, decoded instructions, etc.

.. figure:: images/emuarch.png
  :width: 800
  :align: center

  Q1 Emulator Architecture



.. code-block:: console

  > python3 emulator.py -d
  ; jump to START
  0000 c3 e5 01     ; jp 0x1e5        | SP=0000, A=00    BC=0000, DE=0000, HL=0000
  ; START()
  01e5 ed 56        ; im 0x1          | SP=0000, A=00    BC=0000, DE=0000, HL=0000
  01e7 3e 04        ; ld a, 0x4       | SP=0000, A=00    BC=0000, DE=0000, HL=0000
  01e9 d3 01        ; out (0x1), a    | SP=0000, A=04    BC=0000, DE=0000, HL=0000
  ; 01eb setup registers for copying and clearing
  01eb 11 3f 00     ; ld de, 0x3f     | SP=0000, A=04    BC=0000, DE=0000, HL=0000
  01ee 21 80 40     ; ld hl, 0x4080   | SP=0000, A=04    BC=0000, DE=003f, HL=0000
  01f1 f9           ; ld sp, hl       | SP=0000, A=04    BC=0000, DE=003f, HL=4080
  01f2 eb           ; ex de, hl       | SP=4080, A=04    BC=0000, DE=003f, HL=4080
  ; 01f3 copy (function calls) from 0x003f:0x0047 to 0x4080:
  01f3 01 09 00     ; ld bc, 0x9      | SP=4080, A=04    BC=0000, DE=4080, HL=003f

For interactive sessions it is better to disable periodic hexdump and instruction decode


.. code-block:: console

  > python3 emulator.py
  loading program: Combined Q1 image from IC25-IC32
  loaded 1024 bytes from roms/JDC/IC25.bin at address 0000h
  loaded 1024 bytes from roms/JDC/IC26.bin at address 0400h
  loaded 1024 bytes from roms/JDC/IC27.bin at address 0800h
  loaded 1024 bytes from roms/JDC/IC28.bin at address 0c00h
  loaded 1024 bytes from roms/JDC/IC29.bin at address 1000h
  loaded 1024 bytes from roms/JDC/IC30.bin at address 1400h
  loaded 1024 bytes from roms/JDC/IC31.bin at address 1800h
  loaded 1024 bytes from roms/JDC/IC32.bin at address 1c00h

  ... several blank lines ...

   Q1-Lite
   klar til brug


q1curses
^^^^^^^^

Receives the display buffer via UDP and uses **curses** to output to
screen.
