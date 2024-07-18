
Emulator Hooks and Helpers
==========================

The z80 emulator currently used is written by Ivan Kosarev.
https://github.com/kosarev/z80

In addition to this a few python modules have been written
to provide useful abstractions:


cpu
^^^^^^

The cpu module is initialised with a *program* that is to be loaded. the *reset*
method clears the memory and loads the program.

The important method is *step()* which does one or more instruction executions.
It also detects a halt condition when the program counter points to
uninitialised memory.

In addition, cpu has methods for getting a human readable instruction from *getinstr*
and to provided a dissasembler-like output with *decodestr*.

Finally, the *exit* method does a *hexdump* and prints the last 10 decoded instructions
before esiting the emulator.

memory
^^^^^^

The memory abstraction taps into the memory object of the emulator.

The *clear* method fills the memory with a user specified value. The *loader* method
loads a 'program' into memory. A *hexdump* method prints out only lines that differ
from initialised memory so the whole memory space can be specified but normally only
a few handful of lines are displayed.

Finally, a number of write and get methods are provided: *getu8*, *getu16*, *getu32*,
*writeu8*, *writeu16*.

z8io
^^^^

kbd
^^^

programs
^^^^^^^^

These have then been combined to achieve different functions

disassembly.py
^^^^^^^^^^^^^^

emulator.py
^^^^^^^^^^^
