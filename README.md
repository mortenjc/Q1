

# Q1 Emulator project
An attempt at running Q1 code from ROMs. All information, including the
ROM images are taken from https://datamuseum.dk/wiki/Q1_Microlite

Documentation found at https://github.com/TheByteAttic/Q1

## prerequisites
The Q1 emulator uses a Z80 emulator from kosraev: https://github.com/kosarev/z80

## Installation
At this time I can not remember how I installed the project. More information
will come later.

## Running
To run the emulator

    > cd src
    > python3 single_stepping.py

### command line options

The output can be controlled by printing out a message at a program counter (PC)
of interest using --poi addr

Hexdummp is done periodically but but can be disabled by --nodump

The emulation is stopped after 16380 instructions but this can be changed by
--stopafter nnnn
