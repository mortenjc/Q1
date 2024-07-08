

# Q1 Emulator project
An attempt at running Q1 code from ROMs. All information, including the
ROM images are taken from https://datamuseum.dk/wiki/Q1_Microlite

Documentation found at https://github.com/TheByteAttic/Q1

Please note that this repo is in the early phase and refactoring and
renaming is likely to happen often, hopefully to the better.

## prerequisites
The Q1 emulator uses a Z80 emulator from Kosraev: https://github.com/kosarev/z80

### Installation
Kosarev's Z80 emulator can be installed by

    > python3 setup.py install

If you get an error you might need to

    > pip install setuptools
    > pip install disttools

## Running
To run the emulator you have two options, use the disassembler or run the emulator. Igenerally need to
alternate between the two to achieve progress.

The python files are in the src directory

    > cd src

### Disassembler
Two modes exist:

Automatically disassemble some of the (few) currently known address
ranges. These will be annotated (see known_ranges in disassembly.py).

    > python3 disassembly.py -a
    ...
    <<<<< set keyboard mode 2 (ASM IO page 10) >>>>>
    01E5 ED 56        ; im 0x1          |
    01E7 3E 04        ; ld a, 0x4       |
    01E9 D3 01        ; out (0x1), a    |
    <<<<< prepare registers for copy and clearing >>>>>
    01EB 11 3F 00     ; ld de, 0x3f     |
    01EE 21 80 40     ; ld hl, 0x4080   |
    01F1 F9           ; ld sp, hl       |
    01F2 EB           ; ex de, hl       |
    ...

Manually specifying the start and end address for disassembly, for example:

    > python3 disassembly.py -s 0x01e5 -e 0x01ea
    <<<<< Custom >>>>>
    01E5 ED 56        ; im 0x1          |
    01E7 3E 04        ; ld a, 0x4       |
    01E9 D3 01        ; out (0x1), a    |

### Emulator
The emulator is generally started like this

    > python3 emulator.py
    ...
    ;01f8 clear RAM from 4089 to 40ff
    01F8 97           ; sub a           | SP=4080, A=00 BC=0000, DE=40C4, HL=0048
    01F9 12           ; ld (de), a      | SP=4080, A=00 BC=0000, DE=40C4, HL=0048
    '########### HEXDUMP 0x2000 - 0x10000 ####################################
    icount 256
    ....
    4080 C3 3F 00 C3 B1 02 C3 15 08 00 00 00 00 00 00 00  .?..............
    4090 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
    40A0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
    40B0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
    40C0 00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF  ................
    ....
    ''########### HEXDUMP END #################################################
    01FA 1C           ; inc e           | SP=4080, A=00 BC=0000, DE=40C4, HL=0048
    01FB 20 FB        ; jr nz, 0x1f8    | SP=4080, A=00 BC=0000, DE=40C5, HL=0048
    ...

The hexdump happens periodically and only prints lines that are modified. The
frequency can be controlled with **--dumpfreq**. To disable use **-nodump**.

If you don't care about the instruction decode you can use **--nodecode**.

The emulator stops when it encounters four bytes of uninitialised data (FF FF FF FF)
or when the maximum number of instructions have been emulated. This can be controlled
by **--stopafter**.


## Hardware emulation
The Z80 uses **in**
