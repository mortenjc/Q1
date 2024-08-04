
Log book
========
Entries before July 22, 2024 have been reconstructed by git log history.

2024 07 03
----------

Initial commit

2024 07 06
----------

Capture input, boot prompt achieved.

2024 07 09
----------

Work on IO hooks

2024 07 10
----------

IO hooks for all input and output adddresses so far.

20924 07 12
-----------

Added a flexible program loader to support rom images and code snippets.


2024 07 13
----------

Added more ROM images from peel.dk

2024 07 18
----------

Keyboard handling by kbhit() and injected keyboard interrupt, several
line edit functions verifed (backspace, clear line, cursor.)

2024 07 19
----------

Fixed major bug in Stack Pointer adjustment during keyboard interrupt.

2024 07 21
----------

file descriptor investigations, annotations, ros module, match module, disk module



2024 07 22
----------

In order to initialise the file system I fill out 55 records on each track
with information compatible with figure 2 on page 17 (same document):

Each record looks like this

.. code-block:: console

    |0x9e|Trk|Sect|Csum|0xa|x00 x00 x00 x00 x00 x00|0x9b|Trk|Sect|Csum|0xa|1234|x00 x00 x00 x00 x00 x00|

So far I have seen no definition of what a sector is. So I am assuming the above
record is two sectors, one starting with 0x9e (ID Record) and one starting with 0x9b
'(Data Record)'.

This clearly need more work, but it is a start.

2024 07 24
----------

The above data format was wrong. The end-of-record value is 0x10, not 0xa. Also the six consecutive
0x00 bytes are not actually returned by the controller.

Despite the picture on page 17, it seems that when reading a file desctiptor in a
data record (0x9b), the checksum comes AFTER the FD and User data:

.. code-block:: console

  |0x9b| FD data (24 bytes) | User data | Csum | 0x10

Also, possibly due to other errors it looks like two sets of 0x9e blocks should come
before the 0x9b:

[0x9e ...] [0x9e ...] [0x9b ...]

Also, there does not seem to be a 0x10 after the ID records.

The filesystem can be initialised by adding ID and data blocks or even
manyally writing to certain locations:

.. code-block:: console

    disk.idrecord(  2189, 17, 0)
    disk.idrecord(  2193, 0, 0)
    disk.datarecord(2197, 0, 25, 'MJC     ', data)
    disk.idrecord(  2240, 0, 0)
    disk.datarecord(2244, 0, 26, 'MJC     ', data)
    disk.idrecord(  2287, 0, 0)
    disk.idrecord(  2291, 0, 0)
    disk.datarecord(2295, 0, 26, 'MJC     ', data)
    for i in range(100):
        disk.data[0][2350+i] = 0x9e

After messing with the file system as above (should probably implement a loader
soon), At least I get the OS to acknowledge that the disk I made was bad:

.. code-block:: console

  DISK OPEN
  DISK KEY
  DISK READ
  disk 1, step 0, track 0
  disk 1, step 0, track 1
  ...
  disk 1, step 0, track 28
  disk 1, step 0, track 29
  disk 1, step 0, track 30
  DISK (error) REPORT

  FORMAT ERR
   ON
  MJC

Only the string 'FORMAT ERR ...' is output by the Q1 Emulator. The rest is debugging
output based on IO calls and program counter values.

It would obviously help with more detailed knowledge about disk and file structures.

20.45

Disassembly from the emuklation (and bad disk format) reveals that this system
is expecting 35 tracks per disk, not 77 as previously assumed.


2024 07 27
----------

Still messing around with the filesystem and disk controller. Close but no cigar. Instead
try and work on something else.

Managed to locate the entry point for the pseudo machine code interpreter. This
is what PL/1 programs are compiled into.

Created a simple program to add two numbers on the stack. It consists of two
opcodes '0xa' for add and '0x1f' for return (Q1 Advanced PL/1 programmer's
Manual p. 3 and 4):

.. code-block:: python

  # PL/1 Interpretive Program Counter
  ["snippet", [0x00, 0x80],        0x40fe], # set IPC = x8000

  # Setup two numbers to be added, run PL/1 program
  ["snippet", [0x00],              0x6000], # nop (for trace)
  ["snippet", [0x21, 0x80, 0x40],  0x6001], # hl = 4080
  ["snippet", [0xf9],              0x6004], # SP = 4080
  ["snippet", [0x21, 0x10, 0x00],  0x6005], # hl = 0010
  ["snippet", [0xe5],              0x6008], # push hl
  ["snippet", [0x21, 0x20, 0x00],  0x6009], # hl = 0020
  ["snippet", [0xe5],              0x600c], # push hl
  ["snippet", [0xc3, 0x7c, 0x18],  0x600d], # run PL/1 program

  # PL/1 program
  ["snippet", [0x0a],              0x8000], # add two numbers
  ["snippet", [0x1f],              0x8001]  # return

The funtionality was verified by trace from the emulation:

.. code-block:: console

  6001 21 80 40     ; ld hl, 0x4080             | sp=0000, a=00    bc=0000, de=0000, hl=0000, ix=0000, iy=0000
  6004 f9           ; ld sp, hl                 | sp=0000, a=00    bc=0000, de=0000, hl=4080, ix=0000, iy=0000
  6005 21 10 00     ; ld hl, 0x10               | sp=4080, a=00    bc=0000, de=0000, hl=4080, ix=0000, iy=0000
  6008 e5           ; push hl                   | sp=4080, a=00    bc=0000, de=0000, hl=0010, ix=0000, iy=0000
  6009 21 20 00     ; ld hl, 0x20               | sp=407e, a=00    bc=0000, de=0000, hl=0010, ix=0000, iy=0000
  600c e5           ; push hl                   | sp=407e, a=00    bc=0000, de=0000, hl=0020, ix=0000, iy=0000
  600d c3 7c 18     ; jp 0x187c                 | sp=407c, a=00    bc=0000, de=0000, hl=0020, ix=0000, iy=0000
  187c 2a fe 40     ; ld hl, (0x40fe)           | sp=407c, a=00    bc=0000, de=0000, hl=0020, ix=0000, iy=0000
  187f 7e           ; ld a, (hl)                | sp=407c, a=00    bc=0000, de=0000, hl=8000, ix=0000, iy=0000
  1880 23           ; inc hl                    | sp=407c, a=0a    bc=0000, de=0000, hl=8000, ix=0000, iy=0000
  1881 87           ; add a, a                  | sp=407c, a=0a    bc=0000, de=0000, hl=8001, ix=0000, iy=0000
  1882 fa 95 18     ; jp m, 0x1895              | sp=407c, a=14    bc=0000, de=0000, hl=8001, ix=0000, iy=0000
  1885 da 95 18     ; jp c, 0x1895              | sp=407c, a=14    bc=0000, de=0000, hl=8001, ix=0000, iy=0000
  1888 22 fe 40     ; ld (0x40fe), hl           | sp=407c, a=14    bc=0000, de=0000, hl=8001, ix=0000, iy=0000
  188b c6 0c        ; add a, 0xc                | sp=407c, a=14    bc=0000, de=0000, hl=8001, ix=0000, iy=0000
  188d 6f           ; ld l, a                   | sp=407c, a=20' ' bc=0000, de=0000, hl=8001, ix=0000, iy=0000
  188e 26 18        ; ld h, 0x18                | sp=407c, a=20' ' bc=0000, de=0000, hl=8020, ix=0000, iy=0000
  1890 7e           ; ld a, (hl)                | sp=407c, a=20' ' bc=0000, de=0000, hl=1820, ix=0000, iy=0000
  1891 23           ; inc hl                    | sp=407c, a=a5    bc=0000, de=0000, hl=1820, ix=0000, iy=0000
  1892 66           ; ld h, (hl)                | sp=407c, a=a5    bc=0000, de=0000, hl=1821, ix=0000, iy=0000
  1893 6f           ; ld l, a                   | sp=407c, a=a5    bc=0000, de=0000, hl=1821, ix=0000, iy=0000
  1894 e9           ; jp (hl)                   | sp=407c, a=a5    bc=0000, de=0000, hl=18a5, ix=0000, iy=0000
  18a5 e1           ; pop hl                    | sp=407c, a=a5    bc=0000, de=0000, hl=18a5, ix=0000, iy=0000
  18a6 d1           ; pop de                    | sp=407e, a=a5    bc=0000, de=0000, hl=0020, ix=0000, iy=0000
  18a7 19           ; add hl, de                | sp=4080, a=a5    bc=0000, de=0010, hl=0020, ix=0000, iy=0000
  18a8 e5           ; push hl                   | sp=4080, a=a5    bc=0000, de=0010, hl=0030, ix=0000, iy=0000
  18a9 c3 7c 18     ; jp 0x187c                 | sp=407e, a=a5    bc=0000, de=0010, hl=0030, ix=0000, iy=0000
  187c 2a fe 40     ; ld hl, (0x40fe)           | sp=407e, a=a5    bc=0000, de=0010, hl=0030, ix=0000, iy=0000
  187f 7e           ; ld a, (hl)                | sp=407e, a=a5    bc=0000, de=0010, hl=8001, ix=0000, iy=0000
  1880 23           ; inc hl                    | sp=407e, a=1f    bc=0000, de=0010, hl=8001, ix=0000, iy=0000
  1881 87           ; add a, a                  | sp=407e, a=1f    bc=0000, de=0010, hl=8002, ix=0000, iy=0000
  1882 fa 95 18     ; jp m, 0x1895              | sp=407e, a=3e'>' bc=0000, de=0010, hl=8002, ix=0000, iy=0000
  1885 da 95 18     ; jp c, 0x1895              | sp=407e, a=3e'>' bc=0000, de=0010, hl=8002, ix=0000, iy=0000
  1888 22 fe 40     ; ld (0x40fe), hl           | sp=407e, a=3e'>' bc=0000, de=0010, hl=8002, ix=0000, iy=0000
  188b c6 0c        ; add a, 0xc                | sp=407e, a=3e'>' bc=0000, de=0010, hl=8002, ix=0000, iy=0000
  188d 6f           ; ld l, a                   | sp=407e, a=4a'J' bc=0000, de=0010, hl=8002, ix=0000, iy=0000
  188e 26 18        ; ld h, 0x18                | sp=407e, a=4a'J' bc=0000, de=0010, hl=804a, ix=0000, iy=0000
  1890 7e           ; ld a, (hl)                | sp=407e, a=4a'J' bc=0000, de=0010, hl=184a, ix=0000, iy=0000
  1891 23           ; inc hl                    | sp=407e, a=38'8' bc=0000, de=0010, hl=184a, ix=0000, iy=0000
  1892 66           ; ld h, (hl)                | sp=407e, a=38'8' bc=0000, de=0010, hl=184b, ix=0000, iy=0000
  1893 6f           ; ld l, a                   | sp=407e, a=38'8' bc=0000, de=0010, hl=194b, ix=0000, iy=0000
  1894 e9           ; jp (hl)                   | sp=407e, a=38'8' bc=0000, de=0010, hl=1938, ix=0000, iy=0000
  1938 c9           ; ret                       | sp=407e, a=38'8' bc=0000, de=0010, hl=1938, ix=0000, iy=0000


First we put two numbers 0x0010 and 0x0020 on the stack, then call the pseudocode
interpreter (pc 0x6001 - 0x600f). The 'add' pseudocode instruction is picked up at 0x187f, causing
the add istructions at 0x18a5 - 0x 18a7, placing the correct result (0x0030) on the stack
at 0x18a8.

Then at 0x1875 the 'return from subroutine'  pseudocode instruction is retrieved,
causing the return instruction at 0x1938.


2024 07 28
----------

Testing more pseudocode instructions: multiply, divide and binary to string.

.. code-block:: python

  psmcb2ch = {
      "descr": "Q1 pseudo machine code program (bin to char)",
      "start": 0x6000,
      "stop" : 0x1938,
      "data": [
              ["file", "roms/JDC/full.bin", 0x0000],
              # PL/1 Interpretive Program Counter
              ["snippet", [0x00, 0x80],        0x40fe], # set IPC = x8000
              # Setup two numbers to be added, run PL/1 program
              ["snippet", [0x00],              0x6000], # nop (for trace)
              ["snippet", [0x21, 0x80, 0x40],  0x6001], # hl = 0x4080
              ["snippet", [0xf9],              0x6004], # SP = 0x4080
              ["snippet", [0x21, 0xab, 0xcd],  0x6005], # hl = 0xabcd, unused
              ["snippet", [0xe5],              0x6008], # push hl
              ["snippet", [0x21, 0xff, 0x7f],  0x6009], # hl = 0x7fff
              ["snippet", [0xe5],              0x600c], # push hl
              ["snippet", [0xc3, 0x7c, 0x18],  0x600d], # run program
              # 'PL/1' program
              ["snippet", [0x19],              0x8000], # divide
              ["snippet", [0x1f],              0x8001]  # return
      ],
      "funcs" : [],
      "pois" : []
  }


Here 0x7fff is converted into ascii 32767 as verified from the hexdump:

.. code-block:: console

  ########### HEXDUMP 0x2000 - 0x10000 ####################################
  ....
  4070 03 00 44 00 9b 06 04 00 2e 42 05 00 2e 42 ab cd  ..D......B...B..
  ....
  40f0 fd fd fd fd fd fd fd fd fd fd fd fd fd fd 02 80  ................
  ....
  4220 fd fd fd fd fd fd fd fd fd fd fd fd fd fd 33 32  ..............32
  4230 37 36 37 fd fd fd fd fd fd fd fd fd fd fd fd fd  767.............
  ....
  6000 00 21 80 40 f9 21 ab cd e5 21 ff 7f e5 c3 7c 18  .!.@.!...!......
  ....
  8000 19 1f fd fd fd fd fd fd fd fd fd fd fd fd fd fd  ................
  ....
  ########### HEXDUMP END #################################################


2024 07 30
----------

Mostly address and address range annotations. Some **pylint** related
changes.


2024 08 02
----------

Found real Q1 disk images (from flux samples) here:
https://github.com/MattisLind/q1decode/blob/main/Q1DISKS/README.md

This clarified the sector numbering. converted testdiskette C_S0T00.000 into
a python structure which is loaded when creating the filesystem. There are 23
file on the disk, including the special INDEX file.

.. code-block:: console

  > python3 emulator.py
  INDEX:  INDEX
  INDEX:  SCR
  INDEX:  DALIGN
  INDEX:  PRINT
  INDEX:  RTCTEST
  INDEX:  CONV
  INDEX:  PTEST
  INDEX:  DANKB
  INDEX:  DISPTEST
  INDEX:  SWEDKB
  INDEX:  GERMKB
  INDEX:  SELKB
  INDEX:  DINDEX
  INDEX:  COPY
  INDEX:  ALTER
  INDEX:  MTEST
  INDEX:  DISK
  INDEX:  CTEST
  INDEX:  BDTEST
  INDEX:  SEL
  INDEX:  VERIFY
  INDEX:  SUM
  INDEX:  FRENKB

There are still some issues with accessing the files. For example if I type in
'SCR' the emulator enters an infinite loop searching for iD records on Track 0.

On track 0 all data records have size 40 bytes.

(0x9e, track, sector, cksum, 0x10, 0x9b, 40 bytes, cksum, 0x10)

On the other tracks records are 255 bytes:

(0x9e, track, sector, cksum, 0x10, 0x9b, 255 bytes, cksum, 0x10)


2024 08 04
----------

Still a bit confused about the size of the disk. I've seen code
for skipping 2189 bytes (reading them but not examining them) before
looking for markers. So far I had assumed that something else was
on the disk. Now I am not so sure. Perhaps this allows the disk to
spin up before addressing the data?

Added several disk **images** and a utility to load data recovered from the
fluxsamples provided by Mattis Lind.

For example.

.. code-block:: console

  src/disks/fluxsamples> python3 image.py
  ...
  nonz 0x52: load  78 bytes into address 0x4547
  41 2e 20 20 20 20 20 20 20 20 20 20 20 20 20 20  A.
  20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
  20 20 20 20 20 20 20 cb 10 9e 01 02 03 10 9b 20         ........
  20 20 20 20 20 20 20 44 41 54 45 2d 57 52 49 54         DATE-WRIT
  54 45 4e 2e 20 20 20 20 20 20 20 20 20 20        TEN.

  nonz 0x20: load  57 bytes into address 0x3120
  38 34 2d 30 32 2d 30 36 2e 20 20 20 20 20 20 20  84-02-06.
  20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
  20 20 20 20 20 20 20 20 20 20 20 20 ac 10 9e 01              ....
  03 04 10 9b 20 20 20 20 20                       ....

  nonz 0x20: load  65 bytes into address 0x2020
  55 54 48 4f 52 2e 20 20 20 20 20 20 20 20 20 20  UTHOR.
  20 20 20 20 20 20 20 20 4f 4c 4c 45 2e 20 20 20          OLLE.
  20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
  20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20
  ...
