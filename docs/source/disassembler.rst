Disassembler
============

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
