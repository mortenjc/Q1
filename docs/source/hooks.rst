
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



Applications
============

The previous modules can be combined to achieve different functions

disassembly
^^^^^^^^^^^

Provides disassembler functionality of **programs** with annotations.

.. code-block:: console

  > python3 disassembly.py -a
  ...
  <<<<< print A, E times (entry 0x450) >>>>>
  044e 1d           ; dec e           |
  044f c8           ; ret z           |
  0450 d3 04        ; out (0x4), a    |
  0452 1d           ; dec e           |
  0453 c8           ; ret z           |
  0454 d3 04        ; out (0x4), a    |
  0456 18 f6        ; jr 0x44e        |
  <<<<< display() - string=HL, len=C >>>>>
  0458 f3           ; di              |
  0459 cd 39 04     ; call 0x439      |
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
