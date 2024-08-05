
Python modules
==============

The z80 emulator currently used is written by Ivan Kosarev.
https://github.com/kosarev/z80

In addition to this a few python modules have been written
to provide useful abstractions:


cpu
^^^^^^

The **cpu** module is initialised with a **program** that is to be loaded. the **reset()**
method clears the memory and loads the program.

The important method is **step()** which does one or more instruction executions.
It also detects a halt condition when the program counter points to
uninitialised memory.

In addition, **cpu** has methods for getting a human readable instruction from **getinstr()**
and to provided a dissasembler-like output with **decodestr()**.

Finally, the **exit()** method does a *hexdump* and prints the last 10 decoded instructions
before exiting the emulator.

memory
^^^^^^

The **memory** module taps into the memory object of the emulator.

The **clear()** method fills the memory with a user specified value. The **loader()** method
loads a **program** into memory. A **hexdump()** method prints out only lines that differ
from initial memory fill pattern. Thus the whole memory space can be specified, but normally only
a few handful of lines are displayed.

Finally, a number of *write* and *get* methods are provided: **getu8()**, **getu16()**, **getu32()**,
**writeu8()**, **writeu16()**.

z80io
^^^^^

The **z80io** module provides methods for registering input and output
handlers. These are triggered by the **in** and **out** assembler instructions.

kbd
^^^

The **kbd** module provides a **kbhit()** functionality that can be put in
the main loop of the emulation, capture keys and trigger keyboard events
with the correct codes.

programs
^^^^^^^^

the **program** module defines a loadable program. The program consists of
a list of files and snippets that can be loaded at specified addresses.

Programs can be annotated with points of interest (pois), function names (funcs)
and ranges (known_ranges). Finally, they also have a start address for
setting the initial value of the program counter.

.. code-block:: console

  loop = {
      "descr": "Program desription text",
      "start": 0x2000,
      "data": [
          ["file", "roms/SN615_SN580/IC25_2708.bin",  0x0000],
          ["snippet", [0x00, 0x00, 0x00], 0x2000], # nop
          ["snippet", [0x3C], 0x2003],             # inc a
          ["snippet", [0xC3, 0x00, 0x20], 0x2004]  # jp 2000h
      ],
      "funcs" : [],
      "pois" : [0x0000: 'reset START'],
  }


ros
^^^
The **ros** module provides mappings from addresses to variable names
as given in the "ROS User's Manual", pages 2 - 4. It also holds
functions to print the individual fields of the INDEX and LFILE
file descriptors.


disk
^^^^
The **disk** module provides a **Disk** class and a **Disk Control** class.
The **control** class is used by the **z80io** module to perform disk functions
due to the registered io callback functions.

The **disk** module holds the file system data, can move between tracks,
read (but not yet write) data and respond to status commands. It currently
comes with an attempt of an intitialised filesystem.


filesys
^^^^^^^



Applications
============

The previous modules can be combined to achieve different functions


disassembly
^^^^^^^^^^^

Provides disassembler functionality of **programs** with annotations.

.. code-block:: console

  > python3 disassembly.py -a
  ...
  <<<<< report() >>>>>
  0d8e c5           ; push bc         |
  0d8f f5           ; push af         |
  0d90 cd 6b 0d     ; call 0xd6b      | clrdk()
  0d93 21 ec 0d     ; ld hl, 0xdec    | CLEAR
  0d96 0e 01        ; ld c, 0x1       |
  0d98 cd 27 00     ; call 0x27       |
  0d9b f1           ; pop af          |
  0d9c fe 04        ; cp 0x4          |
  0d9e 28 33        ; jr z, 0xdd3     |
  0da0 fe 09        ; cp 0x9          |
  0da2 fa a7 0d     ; jp m, 0xda7     |
  0da5 3e 09        ; ld a, 0x9       |
  <<<<< print nth error message >>>>>
  0da7 21 ed 0d     ; ld hl, 0xded    | Start of error messages
  ...

emulator
^^^^^^^^

The **emulator** runs the program and displays the runtime status
of the program counter, registers, decoded instructions, etc.

.. code-block:: console

  > python3 emulator.py
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

For interactive sessions it is better to disable periodic hexdump and instruction decode.
This is done using the -d and -n option.


.. code-block:: console

  > python3 emulator.py -n -d -s -1
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
