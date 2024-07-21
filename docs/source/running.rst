
Running the emulator
====================


Interactive Session
^^^^^^^^^^^^^^^^^^^

If you just want to interact with the Q1 via the keyboard you
should use the following invocation

.. code-block:: console

  > python3 emulator.py -n -d   # no instr. decode, no hexdump

Typed-in keys are passed to the Q1 system via fake interrupts.
Characters are echoed to the display, so you can see what you are doing,
but the implementation is not great. However it currently helps me in
my investigations.


The keyboard interaction is currently tailored to my MacBook Pro
keyboard. If you are using a different system you should make your own
bindings. In this case the printed values for non printable characters
are output during an interactive session.

On my MacBook Pro the following Q1 keys are implemented. Here,
they referenced by their variable names, not the names printed on
the keys (see emulator.py):

.. list-table:: ROMs
   :header-rows: 1

   * - Key Name
     - MacBook key
   * - GO
     - Option-g
   * - CORR
     - Backspace
   * - RETURN
     - Return (LF -> CR)
   * - CLEAR ENTRY
     - Option-c
   * - INSERT MODE
     - Option-m

In addition, I use Option-b to trigger hexdumps (much used) and Option-p
to print Z80 registers (rarely used).

Execution decode
^^^^^^^^^^^^^^^^

.. code-block:: console

  > python3 emulator.py -n   # instruction decode, no hexdump



Breakpoint
^^^^^^^^^^
You might want to halt the program and printout various information
when the Program Counter reaches a certain address. To do this:

.. code-block:: console

  > python3 emulator.py -b 0x1ff

This will do a hexdump of the RAM part of the memory, show the previous
10 instructions and dump information about INDEX and LFILE file descriptors.


Triggerpoint
^^^^^^^^^^^^
If you want detailed debug, but only starting from a certain Program Counter,
do This

.. code-block:: console

  > python3 emulator.py -n -d -b 0x1ff
