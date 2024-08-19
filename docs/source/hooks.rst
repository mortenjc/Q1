.. _python_modules:

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

display
^^^^^^^

The **display** module keeps track of the display buffer and essentially
only supports three operations: 1) reset cursor position to (0,0), 2) move
cursor right (and down if line width reached), 3) output a character at
current posision. On every operation, the current buffer is transmitted
via UDP to port 5005. This is used by the **q1curses** application to emulate
the display.

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

The **disk** can move (step) between tracks,read (but not yet write) data and
respond to status commands. The disk needs to be initialised with a
preformatted filesystem.


filesys
^^^^^^^

**filesys** provides funtions to create a filesystem. Either by loading
track files reconstructed by Mattis Lind using **loadtracks()**. The contents
of the tracks can be inspected by **trackinfo()** which parses the
records according to Figure 3 of ROS User's Manual (page 18).

Or by constructing tracks using id and data record functions using
**idrecord()**, **datarecord()** and **datareci()**.


q1curses
^^^^^^^^

Receives the display buffer via UDP and uses **curses** to output to
screen.
