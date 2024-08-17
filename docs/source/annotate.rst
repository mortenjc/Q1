
Annotated disassembly
=====================

From **disassembly.py -a** on 2024 08 17

.. code-block:: console

  loading program: Combined Q1 image from IC25-IC32
  loaded 1024 bytes from roms/JDC/IC25.bin at address 0000h
  loaded 1024 bytes from roms/JDC/IC26.bin at address 0400h
  loaded 1024 bytes from roms/JDC/IC27.bin at address 0800h
  loaded 1024 bytes from roms/JDC/IC28.bin at address 0c00h
  loaded 1024 bytes from roms/JDC/IC29.bin at address 1000h
  loaded 1024 bytes from roms/JDC/IC30.bin at address 1400h
  loaded 1024 bytes from roms/JDC/IC31.bin at address 1800h
  loaded 1024 bytes from roms/JDC/IC32.bin at address 1c00h

  ;jump tables
  0000 c3 e5 01     ; jp 0x1e5             | reset START
  0003 c3 77 00     ; jp 0x77              | TOSTR
  0006 c3 5b 01     ; jp 0x15b             | TODEC
  0009 c3 53 05     ; jp 0x553             | UPDIS
  000c c3 42 06     ; jp 0x642             | MUL
  000f c3 52 06     ; jp 0x652             | DIV
  0012 c3 8a 06     ; jp 0x68a             | BICHAR
  0015 c3 7f 06     ; jp 0x67f             | NHL
  0018 c3 0f 02     ; jp 0x20f             | START
  001b c3 da 03     ; jp 0x3da             | KFILE
  001e c3 7d 04     ; jp 0x47d             | KEYIN
  0021 c3 b4 06     ; jp 0x6b4             | GETDN
  0024 c3 0b 04     ; jp 0x40b             | NKEY
  0027 c3 58 04     ; jp 0x458             | DISPLAY
  002a c3 8f 03     ; jp 0x38f             | PRINTER
  002d c3 e8 06     ; jp 0x6e8             | CARB
  0030 c3 cb 04     ; jp 0x4cb             | STOP
  0033 c3 e6 04     ; jp 0x4e6             | PROCH
  0036 18 14        ; jr 0x4c              | INTRET
  0038 18 18        ; jr 0x52              |
  003a 14           ; inc d                |
  003b 00           ; nop                  |
  003c c3 67 07     ; jp 0x767             | SHIFTY

  ;Return Address (copied to 4080)
  003f c3 3f 00     ; jp 0x3f              |

  ;JP to interrupt routine (copied to 4083)
  0042 c3 b1 02     ; jp 0x2b1             |

  ;JP to wait-for-keyboard-or-printer
  0045 c3 15 08     ; jp 0x815             |

  ;interrupt38 chain
  0052 c3 de 01     ; jp 0x1de             |

  ;interrupt routine()
  01de f5           ; push af              |
  01df c5           ; push bc              |
  01e0 d5           ; push de              |
  01e1 e5           ; push hl              |
  01e2 c3 83 40     ; jp 0x4083            |

  ;start()
  01e5 ed 56        ; im 0x1               |
  01e7 3e 04        ; ld a, 0x4            | set keyboard mode 2 (ASM IO page 73)
  01e9 d3 01        ; out (0x1), a         |
  01eb 11 3f 00     ; ld de, 0x3f          | prepare registers for copy and clearing
  01ee 21 80 40     ; ld hl, 0x4080        |
  01f1 f9           ; ld sp, hl            |
  01f2 eb           ; ex de, hl            |
  01f3 01 09 00     ; ld bc, 0x9           |
  01f6 ed b0        ; ldir                 | copy jump tables from 003f:0047 to 4080:4088
  01f8 97           ; sub a                |
  01f9 12           ; ld (de), a           |
  01fa 1c           ; inc e                |
  01fb 20 fb        ; jr nz, 0x1f8         | clear RAM from 4089 to 40ff
  01fd 3e a0        ; ld a, 0xa0           | printer control - reset printer, raise ribbon
  01ff d3 07        ; out (0x7), a         |
  0201 db 05        ; in a, (0x5)          | printer status  - check result (0 is good)
  0203 b7           ; or a                 |
  0204 20 06        ; jr nz, 0x20c         |
  0206 21 fd 07     ; ld hl, 0x7fd         |
  0209 22 84 40     ; ld (0x4084), hl      |
  020c cd 10 04     ; call 0x410           | clear keyboard buffer, update display

  ;Main program loop
  020f 21 80 40     ; ld hl, 0x4080        | reset stack pointer to x4080
  0212 f9           ; ld sp, hl            |
  0213 cd 15 08     ; call 0x815           | CLRDK
  0216 3a 8e 40     ; ld a, (0x408e)       | get a = Unused
  0219 0f           ; rrca                 |
  021a 38 15        ; jr c, 0x231          |
  021c 21 89 40     ; ld hl, 0x4089        |
  021f 7e           ; ld a, (hl)           | a = PLC (lsb of addr of last char loaded to printer buffer)
  0220 23           ; inc hl               |
  0221 96           ; sub (hl)             | ensure there are no buffered chars to print???
  0222 20 ef        ; jr nz, 0x213         |
  0224 db 0c        ; in a, (0xc)          | UNKNOWN INPUT from 0xc
  0226 cb 77        ; bit 0x6, a           | check bit 6 - unknown
  0228 20 07        ; jr nz, 0x231         |
  022a 07           ; rlca                 |
  022b 38 e6        ; jr c, 0x213          |
  022d 3e 81        ; ld a, 0x81           |
  022f d3 0c        ; out (0xc), a         | UNKNOWN OUTPUT to 0xc
  0231 cd b3 04     ; call 0x4b3           | clear display
  0234 db 1a        ; in a, (0x1a)         | Get status for disk 2
  0236 b7           ; or a                 |
  0237 28 0b        ; jr z, 0x244          | disk status == 0 -> Q1-Lite
  0239 e6 08        ; and 0x8              | else if bit 3 (0x8) clear -> Q1-Magnus
  023b 20 07        ; jr nz, 0x244         |
  023d 21 5e 00     ; ld hl, 0x5e          | HL -> " Q1-Magnus klar til brug"
  0240 0e 18        ; ld c, 0x18           |
  0242 18 05        ; jr 0x249             |
  0244 21 55 00     ; ld hl, 0x55          | HL -> " Q1-Lite"
  0247 0e 16        ; ld c, 0x16           |
  0249 cd a0 02     ; call 0x2a0           | get display width
  024c 91           ; sub c                |
  024d cb 3f        ; srl a                |
  024f 47           ; ld b, a              |
  0250 c5           ; push bc              |
  0251 e5           ; push hl              |
  0252 cd 93 02     ; call 0x293           | ???
  0255 e1           ; pop hl               |
  0256 0e 0a        ; ld c, 0xa            |
  0258 cd 58 04     ; call 0x458           | print " Q1-Magnus/Lite"
  025b 21 68 00     ; ld hl, 0x68          |
  025e 0e 0e        ; ld c, 0xe            |
  0260 cd 58 04     ; call 0x458           | print " Klar til brug"
  0263 c1           ; pop bc               |
  0264 db 04        ; in a, (0x4)          | get display status
  0266 e6 18        ; and 0x18             | check if 40 or 80 bytes
  0268 20 01        ; jr nz, 0x26b         |
  026a 04           ; inc b                |
  026b cd 93 02     ; call 0x293           |
  026e 21 8e 40     ; ld hl, 0x408e        |
  0271 cb 8e        ; res 0x1, (hl)        |
  0273 cd da 03     ; call 0x3da           | get keyboard input (returns when command is entered)
  0276 cd b3 04     ; call 0x4b3           | clear display

  ;load and run program
  0279 21 0f 02     ; ld hl, 0x20f         | set return to Main loop
  027c 22 81 40     ; ld (0x4081), hl      |
  027f cd 0f 08     ; call 0x80f           | LOADER
  0282 21 8e 40     ; ld hl, 0x408e        | USE OF FIELD REPORTED AS UNUSED
  0285 cb ce        ; set 0x1, (hl)        |
  0287 ca 80 40     ; jp z, 0x4080         | jump to loaded program start???
  028a cd 18 08     ; call 0x818           | REPORT
  028d cd 10 04     ; call 0x410           | clear keyboard buffer, update display
  0290 c3 0f 02     ; jp 0x20f             | back to Main loop

  ;print "Q1 Lite/Magnus ..."
  0293 21 55 00     ; ld hl, 0x55          | String "Q1 Lite"
  0296 c5           ; push bc              |
  0297 0e 01        ; ld c, 0x1            |
  0299 cd 58 04     ; call 0x458           | display(SPC)
  029c c1           ; pop bc               |
  029d 10 f4        ; djnz 0x293           |
  029f c9           ; ret                  |

  ;Display width?
  02a0 db 04        ; in a, (0x4)          |
  02a2 cb 5f        ; bit 0x3, a           |
  02a4 3e 50        ; ld a, 0x50           | 80 characters
  02a6 c0           ; ret nz               |
  02a7 db 04        ; in a, (0x4)          |
  02a9 cb 67        ; bit 0x4, a           |
  02ab 3e 28        ; ld a, 0x28           | 40 characters
  02ad c0           ; ret nz               |
  02ae c6 07        ; add a, 0x7           |
  02b0 c9           ; ret                  |

  ;interrupt processing routine()
  02b1 cd d8 04     ; call 0x4d8           |
  02b4 db 05        ; in a, (0x5)          |
  02b6 b7           ; or a                 |
  02b7 fa 62 03     ; jp m, 0x362          |
  02ba 01 00 00     ; ld bc, 0x0           |
  02bd 51           ; ld d, c              |
  02be 59           ; ld e, c              |
  02bf 3a 8d 40     ; ld a, (0x408d)       | get a = RIB
  02c2 b7           ; or a                 |
  02c3 28 02        ; jr z, 0x2c7          |
  02c5 1e 0a        ; ld e, 0xa            |
  02c7 21 89 40     ; ld hl, 0x4089        |
  02ca 7e           ; ld a, (hl)           |
  02cb 23           ; inc hl               |
  02cc 96           ; sub (hl)             |
  02cd 28 5d        ; jr z, 0x32c          |
  02cf 6e           ; ld l, (hl)           |
  02d0 26 41        ; ld h, 0x41           |
  02d2 2c           ; inc l                |
  02d3 7d           ; ld a, l              |
  02d4 f6 80        ; or 0x80              |
  02d6 6f           ; ld l, a              |
  02d7 32 8a 40     ; ld (0x408a), a       | set PTC = a
  02da 7e           ; ld a, (hl)           |
  02db 62           ; ld h, d              |
  02dc 6b           ; ld l, e              |
  02dd 3c           ; inc a                |
  02de fe 20        ; cp 0x20              |
  02e0 28 4a        ; jr z, 0x32c          |
  02e2 3d           ; dec a                |
  02e3 fe 20        ; cp 0x20              |
  02e5 38 06        ; jr c, 0x2ed          |
  02e7 20 43        ; jr nz, 0x32c         |
  02e9 21 0a 00     ; ld hl, 0xa           |
  02ec 19           ; add hl, de           |
  02ed fe 08        ; cp 0x8               |
  02ef 20 04        ; jr nz, 0x2f5         |
  02f1 21 f6 ff     ; ld hl, 0xfff6        |
  02f4 19           ; add hl, de           |
  02f5 fe 0d        ; cp 0xd               |
  02f7 20 08        ; jr nz, 0x301         |
  02f9 2a 8b 40     ; ld hl, (0x408b)      | get hl = POS
  02fc f5           ; push af              |
  02fd cd 7f 06     ; call 0x67f           |
  0300 f1           ; pop af               |
  0301 eb           ; ex de, hl            |
  0302 69           ; ld l, c              |
  0303 60           ; ld h, b              |
  0304 fe 02        ; cp 0x2               |
  0306 20 02        ; jr nz, 0x30a         |
  0308 13           ; inc de               |
  0309 13           ; inc de               |
  030a fe 06        ; cp 0x6               |
  030c 20 01        ; jr nz, 0x30f         |
  030e 13           ; inc de               |
  030f fe 0d        ; cp 0xd               |
  0311 28 02        ; jr z, 0x315          |
  0313 fe 0a        ; cp 0xa               |
  0315 20 04        ; jr nz, 0x31b         |
  0317 21 08 00     ; ld hl, 0x8           |
  031a 09           ; add hl, bc           |
  031b fe 01        ; cp 0x1               |
  031d 20 04        ; jr nz, 0x323         |
  031f 2b           ; dec hl               |
  0320 2b           ; dec hl               |
  0321 2b           ; dec hl               |
  0322 2b           ; dec hl               |
  0323 fe 03        ; cp 0x3               |
  0325 20 01        ; jr nz, 0x328         |
  0327 23           ; inc hl               |
  0328 44           ; ld b, h              |
  0329 4d           ; ld c, l              |
  032a 18 9b        ; jr 0x2c7             |
  032c 32 8d 40     ; ld (0x408d), a       | set RIB = a
  032f f5           ; push af              |
  0330 c5           ; push bc              |
  0331 7a           ; ld a, d              |
  0332 b3           ; or e                 |
  0333 28 22        ; jr z, 0x357          |
  0335 2a 8b 40     ; ld hl, (0x408b)      | get hl = POS
  0338 19           ; add hl, de           |
  0339 22 8b 40     ; ld (0x408b), hl      | set POS = hl
  033c 0e 20        ; ld c, 0x20           |
  033e 30 08        ; jr nc, 0x348         |
  0340 0e 24        ; ld c, 0x24           |
  0342 eb           ; ex de, hl            |
  0343 cd 7f 06     ; call 0x67f           |
  0346 eb           ; ex de, hl            |
  0347 b7           ; or a                 |
  0348 7a           ; ld a, d              |
  0349 1f           ; rra                  |
  034a 57           ; ld d, a              |
  034b 7b           ; ld a, e              |
  034c 1f           ; rra                  |
  034d 5f           ; ld e, a              |
  034e 1f           ; rra                  |
  034f 1f           ; rra                  |
  0350 e6 40        ; and 0x40             |
  0352 b1           ; or c                 |
  0353 4f           ; ld c, a              |
  0354 cd 6b 03     ; call 0x36b           |
  0357 d1           ; pop de               |
  0358 0e 28        ; ld c, 0x28           |
  035a cd 68 03     ; call 0x368           |
  035d f1           ; pop af               |
  035e 28 02        ; jr z, 0x362          |
  0360 d3 05        ; out (0x5), a         |
  0362 e1           ; pop hl               |
  0363 d1           ; pop de               |
  0364 c1           ; pop bc               |
  0365 f1           ; pop af               |
  0366 fb           ; ei                   |
  0367 c9           ; ret                  |

  ;unknown
  0368 7b           ; ld a, e              |
  0369 b2           ; or d                 |
  036a c8           ; ret z                |
  036b 62           ; ld h, d              |
  036c 6b           ; ld l, e              |
  036d 14           ; inc d                |
  036e 15           ; dec d                |
  036f f2 79 03     ; jp p, 0x379          |
  0372 0c           ; inc c                |
  0373 0c           ; inc c                |
  0374 0c           ; inc c                |
  0375 0c           ; inc c                |
  0376 cd 7f 06     ; call 0x67f           |
  0379 7c           ; ld a, h              |
  037a b1           ; or c                 |
  037b d3 07        ; out (0x7), a         | move printer carriage
  037d 7d           ; ld a, l              |
  037e d3 06        ; out (0x6), a         |
  0380 c9           ; ret                  |

  ;text string - CLR, PRINTER FAULT
  0381 0d           ; dec c                |
  0382 50           ; ld d, b              |
  0383 52           ; ld d, d              |
  0384 49           ; ld c, c              |
  0385 4e           ; ld c, (hl)           |
  0386 54           ; ld d, h              |
  0387 45           ; ld b, l              |
  0388 52           ; ld d, d              |
  0389 20 46        ; jr nz, 0x3d1         |
  038b 41           ; ld b, c              |
  038c 55           ; ld d, l              |
  038d 4c           ; ld c, h              |
  038e 54           ; ld d, h              |

  ;check printer status
  038f 0c           ; inc c                |
  0390 0d           ; dec c                |
  0391 c8           ; ret z                |
  0392 db 05        ; in a, (0x5)          |
  0394 cb 6f        ; bit 0x5, a           | test for out of ribbon
  0396 28 10        ; jr z, 0x3a8          |
  0398 d9           ; exx                  |
  0399 0e 0e        ; ld c, 0xe            |
  039b 21 81 03     ; ld hl, 0x381         |
  039e cd 58 04     ; call 0x458           | display PRINTER FAULT
  03a1 cd cb 04     ; call 0x4cb           |
  03a4 cd b3 04     ; call 0x4b3           |
  03a7 d9           ; exx                  |
  03a8 7e           ; ld a, (hl)           |
  03a9 b7           ; or a                 |
  03aa 28 1e        ; jr z, 0x3ca          |
  03ac e5           ; push hl              |
  03ad 21 8a 40     ; ld hl, 0x408a        |
  03b0 7e           ; ld a, (hl)           |
  03b1 2b           ; dec hl               |
  03b2 96           ; sub (hl)             |
  03b3 e6 7f        ; and 0x7f             |
  03b5 3d           ; dec a                |
  03b6 28 15        ; jr z, 0x3cd          |
  03b8 7e           ; ld a, (hl)           |
  03b9 3c           ; inc a                |
  03ba f6 80        ; or 0x80              |
  03bc e1           ; pop hl               |
  03bd 5f           ; ld e, a              |
  03be 16 41        ; ld d, 0x41           |
  03c0 7e           ; ld a, (hl)           |
  03c1 12           ; ld (de), a           |
  03c2 7b           ; ld a, e              |
  03c3 32 89 40     ; ld (0x4089), a       | set PLC = a
  03c6 23           ; inc hl               |
  03c7 0d           ; dec c                |
  03c8 20 c8        ; jr nz, 0x392         |
  03ca f3           ; di                   |
  03cb ff           ; rst 0x38             |

  ;unknown
  03cd c5           ; push bc              |
  03ce cd 86 40     ; call 0x4086          |
  03d1 c1           ; pop bc               |
  03d2 e1           ; pop hl               |
  03d3 f3           ; di                   |
  03d4 ff           ; rst 0x38             |

  ;unknown
  03d5 18 b8        ; jr 0x38f             | check printer status
  03d7 cd 10 04     ; call 0x410           | clear keyboard buffer, update display
  03da cd a9 04     ; call 0x4a9           | get keyboard input, result in a
  03dd 3a 92 40     ; ld a, (0x4092)       | get a = TOOK
  03e0 6f           ; ld l, a              |
  03e1 26 41        ; ld h, 0x41           |
  03e3 0e 00        ; ld c, 0x0            |
  03e5 7e           ; ld a, (hl)           |
  03e6 2c           ; inc l                |
  03e7 fa d7 03     ; jp m, 0x3d7          |
  03ea fe 20        ; cp 0x20              | ignore leading spaces (0x20)
  03ec 28 f7        ; jr z, 0x3e5          |
  03ee 7d           ; ld a, l              |
  03ef 3d           ; dec a                |
  03f0 32 92 40     ; ld (0x4092), a       | set TOOK = a
  03f3 06 08        ; ld b, 0x8            |
  03f5 0c           ; inc c                |
  03f6 7e           ; ld a, (hl)           |
  03f7 23           ; inc hl               |
  03f8 fe 30        ; cp 0x30              |
  03fa 05           ; dec b                |
  03fb 28 02        ; jr z, 0x3ff          |
  03fd 30 f6        ; jr nc, 0x3f5         |
  03ff 21 da 40     ; ld hl, 0x40da        |
  0402 06 08        ; ld b, 0x8            |
  0404 2b           ; dec hl               |
  0405 36 20        ; ld (hl), 0x20        |
  0407 10 fb        ; djnz 0x404           |
  0409 18 72        ; jr 0x47d             |

  ;clear keyboard buffer, update display
  0410 21 00 41     ; ld hl, 0x4100        |
  0413 f3           ; di                   |
  0414 36 00        ; ld (hl), 0x0         |
  0416 2c           ; inc l                |
  0417 3e 20        ; ld a, 0x20           |
  0419 77           ; ld (hl), a           |
  041a 2c           ; inc l                |
  041b f2 19 04     ; jp p, 0x419          |
  041e 32 94 40     ; ld (0x4094), a       | set UNDER = a
  0421 cd 53 05     ; call 0x553           | update display
  0424 97           ; sub a                | a = 0
  0425 32 92 40     ; ld (0x4092), a       | set TOOK = a
  0428 32 95 40     ; ld (0x4095), a       | set KSIZ = a
  042b 32 93 40     ; ld (0x4093), a       | set CURSE = a
  042e 32 98 40     ; ld (0x4098), a       | set ACTK = a
  0431 32 8f 40     ; ld (0x408f), a       | set HEXX = a
  0434 32 90 40     ; ld (0x4090), a       | set INSF = a
  0437 ff           ; rst 0x38             |
  0438 c9           ; ret                  |

  ;XXX
  0439 ed 5b 96 40  ; ld de, (0x4096)      | get de = OSEZ (# chars used for display)
  043d 3e 05        ; ld a, 0x5            |
  043f d3 04        ; out (0x4), a         | display ctrl (0x05) Reset, Unbuffer
  0441 3e 08        ; ld a, 0x8            |
  0443 1c           ; inc e                |
  0444 cd 4e 04     ; call 0x44e           |
  0447 15           ; dec d                |
  0448 f8           ; ret m                |
  0449 cd 50 04     ; call 0x450           |
  044c 18 f9        ; jr 0x447             |

  ;print A, E times (entry 0x450)
  044e 1d           ; dec e                |
  044f c8           ; ret z                |
  0450 d3 04        ; out (0x4), a         |
  0452 1d           ; dec e                |
  0453 c8           ; ret z                |
  0454 d3 04        ; out (0x4), a         |
  0456 18 f6        ; jr 0x44e             |

  ;display() - string=HL, len=C
  0458 f3           ; di                   |
  0459 cd 39 04     ; call 0x439           |
  045c ed 5b 96 40  ; ld de, (0x4096)      | get de = OSEZ (# chars used for display)
  0460 0c           ; inc c                |
  0461 0d           ; dec c                |
  0462 28 10        ; jr z, 0x474          |
  0464 7e           ; ld a, (hl)           |
  0465 23           ; inc hl               |
  0466 b7           ; or a                 |
  0467 28 0b        ; jr z, 0x474          |
  0469 d3 03        ; out (0x3), a         |
  046b 13           ; inc de               |
  046c fe 0d        ; cp 0xd               |
  046e cc b3 04     ; call z, 0x4b3        |
  0471 0d           ; dec c                |
  0472 20 f0        ; jr nz, 0x464         |
  0474 eb           ; ex de, hl            |
  0475 22 96 40     ; ld (0x4096), hl      | set OSEZ (# chars used for display) = hl
  0478 cd 56 05     ; call 0x556           |
  047b fb           ; ei                   |
  047c c9           ; ret                  |

  ;unkown
  047d e5           ; push hl              |
  047e cd a9 04     ; call 0x4a9           |
  0481 d1           ; pop de               |
  0482 21 92 40     ; ld hl, 0x4092        |
  0485 6e           ; ld l, (hl)           |
  0486 26 41        ; ld h, 0x41           |
  0488 3a 95 40     ; ld a, (0x4095)       | get a = KSIZ
  048b 47           ; ld b, a              |
  048c 0c           ; inc c                |
  048d 78           ; ld a, b              |
  048e bd           ; cp l                 |
  048f 28 0e        ; jr z, 0x49f          |
  0491 0d           ; dec c                |
  0492 28 06        ; jr z, 0x49a          |
  0494 7e           ; ld a, (hl)           |
  0495 12           ; ld (de), a           |
  0496 23           ; inc hl               |
  0497 13           ; inc de               |
  0498 18 f3        ; jr 0x48d             |
  049a 7d           ; ld a, l              |
  049b 32 92 40     ; ld (0x4092), a       | set TOOK = a
  049e c9           ; ret                  |
  049f 0d           ; dec c                |
  04a0 ca 10 04     ; jp z, 0x410          |
  04a3 3e 20        ; ld a, 0x20           |
  04a5 12           ; ld (de), a           |
  04a6 13           ; inc de               |
  04a7 18 f6        ; jr 0x49f             |

  ;wait for keyboard
  04a9 3a 98 40     ; ld a, (0x4098)       | get a = ACTK
  04ac b7           ; or a                 |
  04ad c0           ; ret nz               |
  04ae cd 86 40     ; call 0x4086          |
  04b1 18 f6        ; jr 0x4a9             |

  ;clear display?
  04b3 11 00 04     ; ld de, 0x400         |
  04b6 3e 20        ; ld a, 0x20           |
  04b8 d3 03        ; out (0x3), a         |
  04ba d3 03        ; out (0x3), a         |
  04bc 1d           ; dec e                |
  04bd 20 f9        ; jr nz, 0x4b8         |
  04bf 15           ; dec d                |
  04c0 20 f6        ; jr nz, 0x4b8         |
  04c2 ed 53 96 40  ; ld (0x4096), de      | set OSEZ (# chars used for display) = de
  04c6 3e 05        ; ld a, 0x5            |
  04c8 d3 04        ; out (0x4), a         |
  04ca c9           ; ret                  |

  ;disable interrupt, get key?, enable interrupt
  04cb f3           ; di                   |
  04cc cd d1 04     ; call 0x4d1           |
  04cf fb           ; ei                   |
  04d0 c9           ; ret                  |

  ;STOP, wait for key GO (0xe)
  04d1 db 01        ; in a, (0x1)          |
  04d3 fe 0e        ; cp 0xe               | key: GO
  04d5 20 fa        ; jr nz, 0x4d1         |
  04d7 c9           ; ret                  |

  ;read_key()
  04d8 db 01        ; in a, (0x1)          |
  04da b7           ; or a                 |
  04db c8           ; ret z                |
  04dc fe 0f        ; cp 0xf               | key: STOP
  04de 28 f1        ; jr z, 0x4d1          |
  04e0 21 98 40     ; ld hl, 0x4098        |
  04e3 34           ; inc (hl)             |
  04e4 35           ; dec (hl)             |
  04e5 c0           ; ret nz               |
  04e6 21 93 40     ; ld hl, 0x4093        |
  04e9 11 94 40     ; ld de, 0x4094        |
  04ec 46           ; ld b, (hl)           |
  04ed 48           ; ld c, b              |
  04ee fe 9a        ; cp 0x9a              |
  04f0 ca 99 05     ; jp z, 0x599          |
  04f3 fe 9e        ; cp 0x9e              |
  04f5 ca a8 05     ; jp z, 0x5a8          |
  04f8 30 42        ; jr nc, 0x53c         |
  04fa fe 84        ; cp 0x84              |
  04fc 30 4a        ; jr nc, 0x548         |
  04fe fe 1b        ; cp 0x1b              | key: CLEAR ENTRY
  0500 ca 10 04     ; jp z, 0x410          |
  0503 fe 1e        ; cp 0x1e              | key: INSERT MODE
  0505 ca d4 05     ; jp z, 0x5d4          |
  0508 fe 1d        ; cp 0x1d              | key: DEL CHAR
  050a ca f6 05     ; jp z, 0x5f6          |
  050d fe 10        ; cp 0x10              | key: REV TAB
  050f ca e9 05     ; jp z, 0x5e9          |
  0512 fe 09        ; cp 0x9               | key: TAB
  0514 ca da 05     ; jp z, 0x5da          |
  0517 fe 1a        ; cp 0x1a              | key: 0x1a undocumented
  0519 ca ce 05     ; jp z, 0x5ce          |
  051c fe 04        ; cp 0x4               | key: CORR
  051e 20 09        ; jr nz, 0x529         |
  0520 1a           ; ld a, (de)           |
  0521 0d           ; dec c                |
  0522 f2 83 05     ; jp p, 0x583          |
  0525 0c           ; inc c                |
  0526 c3 83 05     ; jp 0x583             |
  0529 38 11        ; jr c, 0x53c          |
  052b fe 1c        ; cp 0x1c              | key: CHAR ADV
  052d 20 03        ; jr nz, 0x532         |
  052f 1a           ; ld a, (de)           |
  0530 18 4c        ; jr 0x57e             |
  0532 30 08        ; jr nc, 0x53c         |
  0534 fe 0b        ; cp 0xb               | key: CLEAR ENTRY
  0536 30 10        ; jr nc, 0x548         |
  0538 fe 08        ; cp 0x8               | key: 0x08 undocumented
  053a 38 0c        ; jr c, 0x548          |
  053c e6 7f        ; and 0x7f             |
  053e fe 03        ; cp 0x3               | key: TAB SET
  0540 20 21        ; jr nz, 0x563         |
  0542 cd b5 05     ; call 0x5b5           |
  0545 b6           ; or (hl)              |
  0546 77           ; ld (hl), a           |
  0547 c9           ; ret                  |

  ;unknown
  0548 32 98 40     ; ld (0x4098), a       | set ACTK = a
  054b 32 91 40     ; ld (0x4091), a       | set FUNKEY = a
  054e 1a           ; ld a, (de)           |
  054f 6e           ; ld l, (hl)           |
  0550 26 41        ; ld h, 0x41           |
  0552 77           ; ld (hl), a           |

  ;updis() - called after printing line?
  0553 cd 39 04     ; call 0x439           |
  0556 21 00 41     ; ld hl, 0x4100        |
  0559 3a 95 40     ; ld a, (0x4095)       | get a = KSIZ
  055c 47           ; ld b, a              |
  055d 04           ; inc b                |
  055e 0e 03        ; ld c, 0x3            |
  0560 ed           ; db 0xed              | z80 otir instruction - B bytes from HL to port C
  0561 b3           ; or e                 |
  0562 c9           ; ret                  |

  ;handle tab clear (clears tab bit in hl?)
  0563 fe 02        ; cp 0x2               | key: TAB CLR
  0565 20 07        ; jr nz, 0x56e         |
  0567 cd b5 05     ; call 0x5b5           |
  056a 2f           ; cpl                  |
  056b a6           ; and (hl)             |
  056c 77           ; ld (hl), a           |
  056d c9           ; ret                  |

  ;unknown HEXX function?
  056e 21 8f 40     ; ld hl, 0x408f        | HEXX
  0571 34           ; inc (hl)             |
  0572 35           ; dec (hl)             |
  0573 c2 07 06     ; jp nz, 0x607         |
  0576 21 90 40     ; ld hl, 0x4090        | INSF
  0579 34           ; inc (hl)             |
  057a 35           ; dec (hl)             |
  057b c4 2b 06     ; call nz, 0x62b       |
  057e 0c           ; inc c                |
  057f f2 83 05     ; jp p, 0x583          |
  0582 0d           ; dec c                |
  0583 26 41        ; ld h, 0x41           |
  0585 68           ; ld l, b              |
  0586 77           ; ld (hl), a           |
  0587 69           ; ld l, c              |

  ;update cursor position and current size of line
  0588 7e           ; ld a, (hl)           |
  0589 36 00        ; ld (hl), 0x0         |
  058b 12           ; ld (de), a           |
  058c 21 93 40     ; ld hl, 0x4093        | CURSE (cursor position)
  058f 71           ; ld (hl), c           |
  0590 23           ; inc hl               |
  0591 23           ; inc hl               |
  0592 7e           ; ld a, (hl)           |
  0593 b9           ; cp c                 |
  0594 30 bd        ; jr nc, 0x553         |
  0596 71           ; ld (hl), c           |
  0597 18 ba        ; jr 0x553             | update display

  ;unknown (on key 0x9a?)
  0599 cd a0 02     ; call 0x2a0           |
  059c ed 44        ; neg                  |
  059e 81           ; add a, c             |
  059f 4f           ; ld c, a              |
  05a0 1a           ; ld a, (de)           |
  05a1 f2 83 05     ; jp p, 0x583          |
  05a4 0e 00        ; ld c, 0x0            |
  05a6 18 db        ; jr 0x583             |

  ;get tab position bit??
  05b5 79           ; ld a, c              |
  05b6 e6 f8        ; and 0xf8             |
  05b8 0f           ; rrca                 |
  05b9 0f           ; rrca                 |
  05ba 0f           ; rrca                 |
  05bb c6 c0        ; add a, 0xc0          | hl = tab positions
  05bd 26 40        ; ld h, 0x40           |
  05bf 6f           ; ld l, a              |
  05c0 79           ; ld a, c              |
  05c1 e6 07        ; and 0x7              |
  05c3 d5           ; push de              |
  05c4 57           ; ld d, a              |
  05c5 3e 80        ; ld a, 0x80           |
  05c7 15           ; dec d                |
  05c8 07           ; rlca                 |
  05c9 f2 c7 05     ; jp p, 0x5c7          |
  05cc d1           ; pop de               |
  05cd c9           ; ret                  |

  ;something with HEX last key
  05ce 3e 81        ; ld a, 0x81           |
  05d0 32 8f 40     ; ld (0x408f), a       | set HEXX = a
  05d3 c9           ; ret                  |

  ;Toggle INSERT mode (on key 0x1e)
  05d4 21 90 40     ; ld hl, 0x4090        | hl = INSF
  05d7 ae           ; xor (hl)             |
  05d8 77           ; ld (hl), a           |
  05d9 c9           ; ret                  |

  ;tab()
  05da 0c           ; inc c                |
  05db 1a           ; ld a, (de)           |
  05dc fa 82 05     ; jp m, 0x582          |
  05df cd b5 05     ; call 0x5b5           |
  05e2 a6           ; and (hl)             |
  05e3 28 f5        ; jr z, 0x5da          |
  05e5 1a           ; ld a, (de)           |
  05e6 c3 83 05     ; jp 0x583             |

  ;unknown
  05e7 83           ; add a, e             |
  05e8 05           ; dec b                |

  ;rev_tab()
  05e9 0d           ; dec c                |
  05ea 1a           ; ld a, (de)           |
  05eb fa 25 05     ; jp m, 0x525          |
  05ee cd b5 05     ; call 0x5b5           |
  05f1 a6           ; and (hl)             |
  05f2 28 f5        ; jr z, 0x5e9          |
  05f4 18 ef        ; jr 0x5e5             |

  ;del_char()
  05f6 21 7f 41     ; ld hl, 0x417f        |
  05f9 0e 20        ; ld c, 0x20           |
  05fb 7d           ; ld a, l              |
  05fc b8           ; cp b                 |
  05fd 7e           ; ld a, (hl)           |
  05fe 71           ; ld (hl), c           |
  05ff 48           ; ld c, b              |
  0600 ca 88 05     ; jp z, 0x588          | done - update cursor position and current size of line
  0603 2d           ; dec l                |
  0604 4f           ; ld c, a              |
  0605 18 f4        ; jr 0x5fb             |

  ;hexx_input()?
  0607 f6 20        ; or 0x20              |
  0609 d6 30        ; sub 0x30             |
  060b fe 10        ; cp 0x10              |
  060d 38 02        ; jr c, 0x611          |
  060f d6 27        ; sub 0x27             |
  0611 35           ; dec (hl)             |
  0612 34           ; inc (hl)             |
  0613 f2 1d 06     ; jp p, 0x61d          |
  0616 c6 10        ; add a, 0x10          |
  0618 77           ; ld (hl), a           |
  0619 1a           ; ld a, (de)           |
  061a c3 83 05     ; jp 0x583             |
  061d 4f           ; ld c, a              |
  061e 7e           ; ld a, (hl)           |
  061f 07           ; rlca                 |
  0620 07           ; rlca                 |
  0621 07           ; rlca                 |
  0622 07           ; rlca                 |
  0623 3d           ; dec a                |
  0624 b1           ; or c                 |
  0625 36 00        ; ld (hl), 0x0         |
  0627 48           ; ld c, b              |
  0628 c3 76 05     ; jp 0x576             |

  ;UNEXPLORED
  062b 26 41        ; ld h, 0x41           |
  062d 68           ; ld l, b              |
  062e 2c           ; inc l                |
  062f f8           ; ret m                |
  0630 f5           ; push af              |
  0631 1a           ; ld a, (de)           |
  0632 4e           ; ld c, (hl)           |
  0633 77           ; ld (hl), a           |
  0634 79           ; ld a, c              |
  0635 2c           ; inc l                |
  0636 f2 32 06     ; jp p, 0x632          |
  0639 48           ; ld c, b              |
  063a f1           ; pop af               |
  063b 21 95 40     ; ld hl, 0x4095        |
  063e 34           ; inc (hl)             |
  063f f0           ; ret p                |
  0640 35           ; dec (hl)             |
  0641 c9           ; ret                  |

  ;multiply() = de * bc
  0642 3e 10        ; ld a, 0x10           |
  0644 21 00 00     ; ld hl, 0x0           |
  0647 29           ; add hl, hl           |
  0648 eb           ; ex de, hl            |
  0649 29           ; add hl, hl           |
  064a eb           ; ex de, hl            |
  064b 30 01        ; jr nc, 0x64e         |
  064d 09           ; add hl, bc           |
  064e 3d           ; dec a                |
  064f 20 f6        ; jr nz, 0x647         |
  0651 c9           ; ret                  |

  ;divide() = hl / de
  0652 7a           ; ld a, d              |
  0653 ac           ; xor h                |
  0654 f5           ; push af              |
  0655 aa           ; xor d                |
  0656 fc 7f 06     ; call m, 0x67f        |
  0659 29           ; add hl, hl           |
  065a eb           ; ex de, hl            |
  065b 24           ; inc h                |
  065c 25           ; dec h                |
  065d f4 7f 06     ; call p, 0x67f        |
  0660 44           ; ld b, h              |
  0661 4d           ; ld c, l              |
  0662 21 00 00     ; ld hl, 0x0           |
  0665 3e 0f        ; ld a, 0xf            |
  0667 29           ; add hl, hl           |
  0668 eb           ; ex de, hl            |
  0669 29           ; add hl, hl           |
  066a eb           ; ex de, hl            |
  066b 30 01        ; jr nc, 0x66e         |
  066d 23           ; inc hl               |
  066e e5           ; push hl              |
  066f 09           ; add hl, bc           |
  0670 30 15        ; jr nc, 0x687         |
  0672 13           ; inc de               |
  0673 33           ; inc sp               |
  0674 33           ; inc sp               |
  0675 3d           ; dec a                |
  0676 20 ef        ; jr nz, 0x667         |
  0678 f1           ; pop af               |
  0679 f0           ; ret p                |
  067a eb           ; ex de, hl            |
  067b cd 7f 06     ; call 0x67f           |
  067e eb           ; ex de, hl            |
  067f 7c           ; ld a, h              |
  0680 2f           ; cpl                  |
  0681 67           ; ld h, a              |
  0682 7d           ; ld a, l              |
  0683 2f           ; cpl                  |
  0684 6f           ; ld l, a              |
  0685 23           ; inc hl               |
  0686 c9           ; ret                  |
  0687 e1           ; pop hl               |
  0688 18 eb        ; jr 0x675             |

  ;bin_to_string()
  068a 01 00 00     ; ld bc, 0x0           |
  068d 24           ; inc h                |
  068e 25           ; dec h                |
  068f f5           ; push af              |
  0690 fc 7f 06     ; call m, 0x67f        |
  0693 d5           ; push de              |
  0694 c5           ; push bc              |
  0695 11 0a 00     ; ld de, 0xa           |
  0698 cd 52 06     ; call 0x652           | call divide() hl/10
  069b 7d           ; ld a, l              |
  069c c6 30        ; add a, 0x30          |
  069e c1           ; pop bc               |
  069f 0c           ; inc c                |
  06a0 e1           ; pop hl               |
  06a1 77           ; ld (hl), a           |
  06a2 2b           ; dec hl               |
  06a3 eb           ; ex de, hl            |
  06a4 7c           ; ld a, h              |
  06a5 b5           ; or l                 |
  06a6 20 eb        ; jr nz, 0x693         |
  06a8 13           ; inc de               |
  06a9 f1           ; pop af               |
  06aa f0           ; ret p                |
  06ab 0c           ; inc c                |
  06ac 3e 2d        ; ld a, 0x2d           |
  06ae 1b           ; dec de               |
  06af 12           ; ld (de), a           |
  06b0 c9           ; ret                  |

  ;UNEXPLORED
  06b1 cd 10 04     ; call 0x410           |
  06b4 cd a9 04     ; call 0x4a9           |
  06b7 21 92 40     ; ld hl, 0x4092        |
  06ba 6e           ; ld l, (hl)           |
  06bb 26 41        ; ld h, 0x41           |
  06bd 3a 95 40     ; ld a, (0x4095)       | get a = KSIZ
  06c0 95           ; sub l                |
  06c1 4f           ; ld c, a              |
  06c2 47           ; ld b, a              |
  06c3 28 ec        ; jr z, 0x6b1          |
  06c5 0c           ; inc c                |
  06c6 cd c2 01     ; call 0x1c2           |
  06c9 28 e6        ; jr z, 0x6b1          |
  06cb 30 f9        ; jr nc, 0x6c6         |
  06cd cd c2 01     ; call 0x1c2           |
  06d0 28 06        ; jr z, 0x6d8          |
  06d2 38 f9        ; jr c, 0x6cd          |
  06d4 fe 15        ; cp 0x15              |
  06d6 28 f5        ; jr z, 0x6cd          |
  06d8 d1           ; pop de               |
  06d9 78           ; ld a, b              |
  06da 91           ; sub c                |
  06db 4f           ; ld c, a              |
  06dc 21 40 42     ; ld hl, 0x4240        |
  06df e5           ; push hl              |
  06e0 c5           ; push bc              |
  06e1 d5           ; push de              |
  06e2 cd 7d 04     ; call 0x47d           |
  06e5 c3 5b 01     ; jp 0x15b             |
  06e8 11 00 00     ; ld de, 0x0           |
  06eb 0c           ; inc c                |
  06ec 0d           ; dec c                |
  06ed c8           ; ret z                |
  06ee 7e           ; ld a, (hl)           |
  06ef e6 7f        ; and 0x7f             |
  06f1 23           ; inc hl               |
  06f2 d6 30        ; sub 0x30             |
  06f4 38 2d        ; jr c, 0x723          |
  06f6 fe 0a        ; cp 0xa               |
  06f8 30 f2        ; jr nc, 0x6ec         |
  06fa 2b           ; dec hl               |
  06fb e5           ; push hl              |
  06fc 62           ; ld h, d              |
  06fd 6b           ; ld l, e              |
  06fe 29           ; add hl, hl           |
  06ff 38 0d        ; jr c, 0x70e          |
  0701 29           ; add hl, hl           |
  0702 38 0a        ; jr c, 0x70e          |
  0704 19           ; add hl, de           |
  0705 38 07        ; jr c, 0x70e          |
  0707 29           ; add hl, hl           |
  0708 38 04        ; jr c, 0x70e          |
  070a 5f           ; ld e, a              |
  070b 16 00        ; ld d, 0x0            |
  070d 19           ; add hl, de           |
  070e eb           ; ex de, hl            |
  070f e1           ; pop hl               |
  0710 d8           ; ret c                |
  0711 0d           ; dec c                |
  0712 c8           ; ret z                |
  0713 23           ; inc hl               |
  0714 7e           ; ld a, (hl)           |
  0715 f6 80        ; or 0x80              |
  0717 d6 30        ; sub 0x30             |
  0719 f0           ; ret p                |
  071a e6 7f        ; and 0x7f             |
  071c fe 0a        ; cp 0xa               |
  071e 38 db        ; jr c, 0x6fb          |
  0720 14           ; inc d                |
  0721 15           ; dec d                |
  0722 c9           ; ret                  |
  0723 d6 fe        ; sub 0xfe             |
  0725 c8           ; ret z                |
  0726 3c           ; inc a                |
  0727 20 c3        ; jr nz, 0x6ec         |
  0729 cd ec 06     ; call 0x6ec           |
  072c d8           ; ret c                |
  072d eb           ; ex de, hl            |
  072e cd 7f 06     ; call 0x67f           |
  0731 bf           ; cp a                 |
  0732 eb           ; ex de, hl            |
  0733 c9           ; ret                  |

  ;UNEXPLORED
  0734 e5           ; push hl              |
  0735 0c           ; inc c                |
  0736 04           ; inc b                |
  0737 2b           ; dec hl               |
  0738 23           ; inc hl               |
  0739 0d           ; dec c                |
  073a 28 26        ; jr z, 0x762          |
  073c 7e           ; ld a, (hl)           |
  073d b7           ; or a                 |
  073e 28 22        ; jr z, 0x762          |
  0740 e5           ; push hl              |
  0741 d5           ; push de              |
  0742 c5           ; push bc              |
  0743 0c           ; inc c                |
  0744 05           ; dec b                |
  0745 28 11        ; jr z, 0x758          |
  0747 1a           ; ld a, (de)           |
  0748 b7           ; or a                 |
  0749 28 0d        ; jr z, 0x758          |
  074b 0d           ; dec c                |
  074c 28 05        ; jr z, 0x753          |
  074e 13           ; inc de               |
  074f be           ; cp (hl)              |
  0750 23           ; inc hl               |
  0751 28 f1        ; jr z, 0x744          |
  0753 c1           ; pop bc               |
  0754 d1           ; pop de               |
  0755 e1           ; pop hl               |
  0756 18 e0        ; jr 0x738             |
  0758 f1           ; pop af               |
  0759 f1           ; pop af               |
  075a d1           ; pop de               |
  075b e1           ; pop hl               |
  075c cd 7f 06     ; call 0x67f           |
  075f 19           ; add hl, de           |
  0760 23           ; inc hl               |
  0761 c9           ; ret                  |
  0762 f1           ; pop af               |
  0763 21 00 00     ; ld hl, 0x0           |
  0766 c9           ; ret                  |

  ;called from x003c (nibbl rotation?)
  0767 c5           ; push bc              |
  0768 06 10        ; ld b, 0x10           |
  076a 21 00 42     ; ld hl, 0x4200        |
  076d af           ; xor a                |
  076e ed 6f        ; rld                  |
  0770 23           ; inc hl               |
  0771 10 fb        ; djnz 0x76e           |
  0773 c1           ; pop bc               |
  0774 c9           ; ret                  |

  ;UNEXPLORED
  0775 cd d8 04     ; call 0x4d8           | call getkey?
  0778 21 89 40     ; ld hl, 0x4089        |
  077b 7e           ; ld a, (hl)           |
  077c 23           ; inc hl               |
  077d be           ; cp (hl)              |
  077e 28 3c        ; jr z, 0x7bc          |
  0780 db 0c        ; in a, (0xc)          | unknown input (0xc undocumented, rs232?)
  0782 cb 77        ; bit 0x6, a           |
  0784 28 06        ; jr z, 0x78c          |
  0786 3e c0        ; ld a, 0xc0           |
  0788 d3 0c        ; out (0xc), a         |
  078a 18 30        ; jr 0x7bc             |
  078c e6 80        ; and 0x80             |
  078e 20 2c        ; jr nz, 0x7bc         |
  0790 21 89 40     ; ld hl, 0x4089        |
  0793 7e           ; ld a, (hl)           |
  0794 23           ; inc hl               |
  0795 96           ; sub (hl)             |
  0796 28 24        ; jr z, 0x7bc          |
  0798 6e           ; ld l, (hl)           |
  0799 26 41        ; ld h, 0x41           |
  079b 2c           ; inc l                |
  079c 7d           ; ld a, l              |
  079d f6 80        ; or 0x80              |
  079f 32 8a 40     ; ld (0x408a), a       | set PTC = a
  07a2 6f           ; ld l, a              |
  07a3 7e           ; ld a, (hl)           |
  07a4 fe 0d        ; cp 0xd               |
  07a6 20 04        ; jr nz, 0x7ac         |
  07a8 3e 0a        ; ld a, 0xa            |
  07aa 18 06        ; jr 0x7b2             |
  07ac fe 0a        ; cp 0xa               |
  07ae 20 02        ; jr nz, 0x7b2         |
  07b0 3e 0d        ; ld a, 0xd            |
  07b2 fe 7f        ; cp 0x7f              |
  07b4 20 02        ; jr nz, 0x7b8         |
  07b6 3e 7e        ; ld a, 0x7e           |
  07b8 e6 7f        ; and 0x7f             |
  07ba d3 0c        ; out (0xc), a         |
  07bc c3 36 00     ; jp 0x36              |
  07bf 41           ; ld b, c              |
  07c0 7e           ; ld a, (hl)           |
  07c1 12           ; ld (de), a           |
  07c2 7b           ; ld a, e              |
  07c3 32 89 40     ; ld (0x4089), a       | set PLC = a
  07c6 23           ; inc hl               |
  07c7 0d           ; dec c                |
  07c8 20 c8        ; jr nz, 0x792         |
  07ca f3           ; di                   |
  07cb ff           ; rst 0x38             |
  07cc c9           ; ret                  |
  07cd c5           ; push bc              |
  07ce cd 86 40     ; call 0x4086          |
  07d1 c1           ; pop bc               |
  07d2 e1           ; pop hl               |
  07d3 f3           ; di                   |
  07d4 ff           ; rst 0x38             |
  07d5 18 b8        ; jr 0x78f             |
  07d7 cd 10 04     ; call 0x410           |
  07da cd a9 04     ; call 0x4a9           |
  07dd 3a 92 40     ; ld a, (0x4092)       | get a = TOOK
  07e0 6f           ; ld l, a              |
  07e1 26 41        ; ld h, 0x41           |
  07e3 0e 00        ; ld c, 0x0            |
  07e5 7e           ; ld a, (hl)           |
  07e6 2c           ; inc l                |
  07e7 fa d7 03     ; jp m, 0x3d7          |
  07ea fe 20        ; cp 0x20              |
  07ec 28 f7        ; jr z, 0x7e5          |
  07ee 7d           ; ld a, l              |
  07ef 3d           ; dec a                |
  07f0 32 92 40     ; ld (0x4092), a       | set TOOK = a
  07f3 06 08        ; ld b, 0x8            |
  07f5 0c           ; inc c                |
  07f6 7e           ; ld a, (hl)           |
  07f7 23           ; inc hl               |
  07f8 fe 30        ; cp 0x30              |
  07fa 05           ; dec b                |
  07fb 28 02        ; jr z, 0x7ff          |
  07fd c3 75 07     ; jp 0x775             |

  ;READ vec
  0800 c3 8e 08     ; jp 0x88e             |

  ;WRITE vec
  0803 c3 4a 09     ; jp 0x94a             |

  ;REWRITE vec
  0806 c3 75 09     ; jp 0x975             |

  ;KEY[SEARCH] vec
  0809 c3 4f 0e     ; jp 0xe4f             |

  ;OPEN vec
  080c c3 30 08     ; jp 0x830             |

  ;LOADER vec
  080f c3 1e 0d     ; jp 0xd1e             | jump to loader()

  ;CLOSE vec
  0812 c3 e0 0c     ; jp 0xce0             |

  ;CLRDK vec
  0815 c3 6b 0d     ; jp 0xd6b             |

  ;REPORT vec
  0818 c3 8e 0d     ; jp 0xd8e             |

  ;unknown jump vectors
  081b c3 ab 0b     ; jp 0xbab             |
  081e c3 34 0c     ; jp 0xc34             |
  0821 c3 36 09     ; jp 0x936             |
  0824 c3 45 09     ; jp 0x945             |
  0827 c3 3b 0b     ; jp 0xb3b             |
  082a c3 5a 0b     ; jp 0xb5a             |
  082d c3 67 0b     ; jp 0xb67             |

  ;open()
  0830 97           ; sub a                |
  0831 32 ad 40     ; ld (0x40ad), a       | set Disk # = a
  0834 3e 80        ; ld a, 0x80           |
  0836 32 13 42     ; ld (0x4213), a       |
  0839 e5           ; push hl              |
  083a 3a a5 40     ; ld a, (0x40a5)       | get a = AD (access denined)
  083d 2f           ; cpl                  | a = bit mask of allowed drives
  083e 47           ; ld b, a              |
  083f 21 13 42     ; ld hl, 0x4213        |
  0842 7e           ; ld a, (hl)           |
  0843 07           ; rlca                 | get next potential disk
  0844 77           ; ld (hl), a           |
  0845 21 ad 40     ; ld hl, 0x40ad        | get disk# from index file
  0848 34           ; inc (hl)             |
  0849 a0           ; and b                | is disk available?
  084a e1           ; pop hl               |
  084b 28 2f        ; jr z, 0x87c          |
  084d e5           ; push hl              |
  084e 11 02 00     ; ld de, 0x2           |
  0851 01 9f 40     ; ld bc, 0x409f        | Current record number on index?
  0854 cd e1 0f     ; call 0xfe1           | setup FD for INDEX (rpt, #records, record size)
  0857 02           ; ld (bc), a           |
  0858 0b           ; dec bc               |
  0859 02           ; ld (bc), a           |
  085a 3e 08        ; ld a, 0x8            |
  085c 23           ; inc hl               |
  085d 23           ; inc hl               |
  085e cd 09 08     ; call 0x809           | call KEY[SEARCH]
  0861 e1           ; pop hl               |
  0862 20 18        ; jr nz, 0x87c         |
  0864 11 18 00     ; ld de, 0x18          |
  0867 3e 01        ; ld a, 0x1            |
  0869 cd 00 08     ; call 0x800           | call READ
  086c 21 ad 40     ; ld hl, 0x40ad        | get disk# from index file
  086f 46           ; ld b, (hl)           |
  0870 2a 99 40     ; ld hl, (0x4099)      | get hl = THERE (addr for disk transfer)
  0873 11 0f 00     ; ld de, 0xf           |
  0876 19           ; add hl, de           |
  0877 70           ; ld (hl), b           |
  0878 01 df 0d     ; ld bc, 0xddf         |
  087b c9           ; ret                  |
  087c e5           ; push hl              |
  087d 21 13 42     ; ld hl, 0x4213        |
  0880 7e           ; ld a, (hl)           |
  0881 fe 80        ; cp 0x80              |
  0883 fa 3a 08     ; jp m, 0x83a          |
  0886 3e 04        ; ld a, 0x4            |
  0888 b7           ; or a                 |
  0889 e1           ; pop hl               |
  088a 01 df 0d     ; ld bc, 0xddf         |
  088d c9           ; ret                  |

  ;read()
  088e cd b8 0f     ; call 0xfb8           |
  0891 c3 00 10     ; jp 0x1000            |
  0894 cd f0 0a     ; call 0xaf0           |
  0897 c0           ; ret nz               |
  0898 21 9d 40     ; ld hl, 0x409d        |
  089b 36 20        ; ld (hl), 0x20        |
  089d cd 5a 0b     ; call 0xb5a           |
  08a0 cd d3 0a     ; call 0xad3           |
  08a3 cd 3b 0b     ; call 0xb3b           |
  08a6 1e ff        ; ld e, 0xff           |
  08a8 cd 67 0b     ; call 0xb67           |
  08ab ca 36 09     ; jp z, 0x936          |
  08ae cd 8d 0c     ; call 0xc8d           |
  08b1 c2 36 09     ; jp nz, 0x936         |
  08b4 3a b8 40     ; ld a, (0x40b8)       | get a = PART2 unused length
  08b7 3c           ; inc a                |
  08b8 47           ; ld b, a              |
  08b9 0e 19        ; ld c, 0x19           |
  08bb d9           ; exx                  |
  08bc 2a b6 40     ; ld hl, (0x40b6)      | get hl = PART1 (length to be transferred)
  08bf 7c           ; ld a, h              |
  08c0 1f           ; rra                  |
  08c1 7d           ; ld a, l              |
  08c2 1f           ; rra                  |
  08c3 47           ; ld b, a              |
  08c4 21 ee 08     ; ld hl, 0x8ee         |
  08c7 30 04        ; jr nc, 0x8cd         |
  08c9 21 f4 08     ; ld hl, 0x8f4         |
  08cc 04           ; inc b                |
  08cd e5           ; push hl              |
  08ce 2a a2 40     ; ld hl, (0x40a2)      | get hl = TRKS  (track # for drive 2)
  08d1 2b           ; dec hl               |
  08d2 56           ; ld d, (hl)           |
  08d3 db 1a        ; in a, (0x1a)         |
  08d5 0e 1a        ; ld c, 0x1a           |
  08d7 ed 78        ; in a, (c)            |
  08d9 f2 d7 08     ; jp p, 0x8d7          |
  08dc 0d           ; dec c                |
  08dd db 19        ; in a, (0x19)         | read byte from disk 2
  08df fe 9b        ; cp 0x9b              | is Data record?
  08e1 c8           ; ret z                |
  08e2 e1           ; pop hl               |
  08e3 21 9d 40     ; ld hl, 0x409d        |
  08e6 3e 02        ; ld a, 0x2            |
  08e8 35           ; dec (hl)             |
  08e9 28 4b        ; jr z, 0x936          |
  08eb 18 b9        ; jr 0x8a6             |
  08ed 23           ; inc hl               |
  08ee ed 58        ; in e, (c)            | read byte from disk 2
  08f0 72           ; ld (hl), d           |
  08f1 23           ; inc hl               |
  08f2 73           ; ld (hl), e           |
  08f3 83           ; add a, e             |
  08f4 ed 50        ; in d, (c)            | read byte from disk 2
  08f6 82           ; add a, d             |
  08f7 05           ; dec b                |
  08f8 20 f3        ; jr nz, 0x8ed         |
  08fa d9           ; exx                  |
  08fb ed 68        ; in l, (c)            |
  08fd 85           ; add a, l             |
  08fe 05           ; dec b                |
  08ff 20 fa        ; jr nz, 0x8fb         |
  0901 95           ; sub l                |
  0902 bd           ; cp l                 |
  0903 db 19        ; in a, (0x19)         | read byte from disk 2
  0905 20 dc        ; jr nz, 0x8e3         |
  0907 d9           ; exx                  |
  0908 23           ; inc hl               |
  0909 72           ; ld (hl), d           |
  090a fe 10        ; cp 0x10              |
  090c 20 d5        ; jr nz, 0x8e3         |
  090e 07           ; rlca                 |
  090f 32 9d 40     ; ld (0x409d), a       | set ERC   (disk error count) = a
  0912 2a a2 40     ; ld hl, (0x40a2)      | get hl = TRKS  (track # for drive 2)
  0915 eb           ; ex de, hl            |
  0916 2a 20 42     ; ld hl, (0x4220)      |
  0919 19           ; add hl, de           |
  091a 22 a2 40     ; ld (0x40a2), hl      | set TRKS  (track # for drive 2) = hl
  091d d9           ; exx                  |
  091e dd 34 00     ; inc (ix + 0x0)       |
  0921 20 03        ; jr nz, 0x926         |
  0923 dd 34 01     ; inc (ix + 0x1)       |
  0926 3e 20        ; ld a, 0x20           |
  0928 32 9d 40     ; ld (0x409d), a       | set ERC   (disk error count) = a
  092b 97           ; sub a                |
  092c 21 9c 40     ; ld hl, 0x409c        |
  092f 1c           ; inc e                |
  0930 35           ; dec (hl)             |
  0931 c2 a8 08     ; jp nz, 0x8a8         |
  0934 18 0f        ; jr 0x945             |
  0936 dd 34 00     ; inc (ix + 0x0)       | increment Record Number (LO)
  0939 20 03        ; jr nz, 0x93e         |
  093b dd 34 01     ; inc (ix + 0x1)       | increment Record Number (HI)
  093e 21 9c 40     ; ld hl, 0x409c        |
  0941 35           ; dec (hl)             |
  0942 20 f2        ; jr nz, 0x936         |
  0944 b7           ; or a                 |
  0945 fb           ; ei                   |
  0946 dd e5        ; push ix              |
  0948 c1           ; pop bc               |
  0949 c9           ; ret                  |

  ;write jump()
  094a cd b8 0f     ; call 0xfb8           |
  094d c3 03 10     ; jp 0x1003            |
  0950 cd f0 0a     ; call 0xaf0           |
  0953 c0           ; ret nz               |
  0954 cd 5a 0b     ; call 0xb5a           |
  0957 cd d3 0a     ; call 0xad3           |
  095a dd 5e 0e     ; ld e, (ix + 0xe)     |
  095d 16 00        ; ld d, 0x0            |
  095f dd 7e 10     ; ld a, (ix + 0x10)    |
  0962 dd 96 12     ; sub (ix + 0x12)      |
  0965 21 00 00     ; ld hl, 0x0           |
  0968 3d           ; dec a                |
  0969 19           ; add hl, de           |
  096a 3c           ; inc a                |
  096b 20 fc        ; jr nz, 0x969         |
  096d dd 75 0a     ; ld (ix + 0xa), l     |
  0970 dd 74 0b     ; ld (ix + 0xb), h     |
  0973 18 0d        ; jr 0x982             |

  ;rewrite()
  0975 cd b8 0f     ; call 0xfb8           |
  0978 c3 06 10     ; jp 0x1006            |
  097b cd f0 0a     ; call 0xaf0           |
  097e c0           ; ret nz               |
  097f cd d3 0a     ; call 0xad3           |
  0982 21 9d 40     ; ld hl, 0x409d        |
  0985 36 20        ; ld (hl), 0x20        |
  0987 dd 7e 13     ; ld a, (ix + 0x13)    |
  098a b7           ; or a                 |
  098b 3e 07        ; ld a, 0x7            |
  098d fa 36 09     ; jp m, 0x936          |
  0990 21 29 42     ; ld hl, 0x4229        |
  0993 77           ; ld (hl), a           |
  0994 21 22 42     ; ld hl, 0x4222        |
  0997 36 00        ; ld (hl), 0x0         |
  0999 22 24 42     ; ld (0x4224), hl      |
  099c cd 3b 0b     ; call 0xb3b           |
  099f 1e ff        ; ld e, 0xff           |
  09a1 cd 67 0b     ; call 0xb67           |
  09a4 28 57        ; jr z, 0x9fd          |
  09a6 cd 8d 0c     ; call 0xc8d           |
  09a9 20 8b        ; jr nz, 0x936         |
  09ab db 19        ; in a, (0x19)         |
  09ad 3e 80        ; ld a, 0x80           |
  09af d3 1b        ; out (0x1b), a        |
  09b1 d9           ; exx                  |
  09b2 2a b6 40     ; ld hl, (0x40b6)      | get hl = PART1 (length to be transferred)
  09b5 db 19        ; in a, (0x19)         |
  09b7 eb           ; ex de, hl            |
  09b8 2a a2 40     ; ld hl, (0x40a2)      | get hl = TRKS  (track # for drive 2)
  09bb db 19        ; in a, (0x19)         |
  09bd 1b           ; dec de               |
  09be 7a           ; ld a, d              |
  09bf 13           ; inc de               |
  09c0 0f           ; rrca                 |
  09c1 db 19        ; in a, (0x19)         |
  09c3 3a b8 40     ; ld a, (0x40b8)       | get a = PART2 unused length
  09c6 57           ; ld d, a              |
  09c7 db 19        ; in a, (0x19)         |
  09c9 14           ; inc d                |
  09ca 01 19 00     ; ld bc, 0x19          |
  09cd db 19        ; in a, (0x19)         |
  09cf 3e 9b        ; ld a, 0x9b           |
  09d1 d3 19        ; out (0x19), a        |
  09d3 d2 c8 0a     ; jp nc, 0xac8         |
  09d6 86           ; add a, (hl)          |
  09d7 ed a3        ; outi                 |
  09d9 20 fb        ; jr nz, 0x9d6         |
  09db 43           ; ld b, e              |
  09dc 86           ; add a, (hl)          |
  09dd ed a3        ; outi                 |
  09df 20 fb        ; jr nz, 0x9dc         |
  09e1 15           ; dec d                |
  09e2 28 05        ; jr z, 0x9e9          |
  09e4 ed 41        ; out (c), b           |
  09e6 15           ; dec d                |
  09e7 20 fb        ; jr nz, 0x9e4         |
  09e9 d3 19        ; out (0x19), a        |
  09eb 2a 24 42     ; ld hl, (0x4224)      |
  09ee 16 10        ; ld d, 0x10           |
  09f0 ed 51        ; out (c), d           |
  09f2 86           ; add a, (hl)          |
  09f3 77           ; ld (hl), a           |
  09f4 af           ; xor a                |
  09f5 d3 19        ; out (0x19), a        |
  09f7 00           ; nop                  |
  09f8 00           ; nop                  |
  09f9 d3 19        ; out (0x19), a        |
  09fb d3 1b        ; out (0x1b), a        |
  09fd 2a a2 40     ; ld hl, (0x40a2)      | get hl = TRKS  (track # for drive 2)
  0a00 eb           ; ex de, hl            |
  0a01 2a 20 42     ; ld hl, (0x4220)      |
  0a04 19           ; add hl, de           |
  0a05 22 a2 40     ; ld (0x40a2), hl      | set TRKS  (track # for drive 2) = hl
  0a08 d9           ; exx                  |
  0a09 1c           ; inc e                |
  0a0a dd 34 00     ; inc (ix + 0x0)       |
  0a0d 20 03        ; jr nz, 0xa12         |
  0a0f dd 34 01     ; inc (ix + 0x1)       |
  0a12 21 9b 40     ; ld hl, 0x409b        |
  0a15 35           ; dec (hl)             |
  0a16 20 89        ; jr nz, 0x9a1         |
  0a18 23           ; inc hl               |
  0a19 7e           ; ld a, (hl)           |
  0a1a ed 44        ; neg                  |
  0a1c dd 86 00     ; add a, (ix + 0x0)    |
  0a1f dd 77 00     ; ld (ix + 0x0), a     |
  0a22 38 03        ; jr c, 0xa27          |
  0a24 dd 35 01     ; dec (ix + 0x1)       |
  0a27 1e ff        ; ld e, 0xff           |
  0a29 3e 23        ; ld a, 0x23           |
  0a2b 32 24 42     ; ld (0x4224), a       |
  0a2e cd 67 0b     ; call 0xb67           |
  0a31 ca 36 09     ; jp z, 0x936          |
  0a34 cd 8d 0c     ; call 0xc8d           |
  0a37 c2 36 09     ; jp nz, 0x936         |
  0a3a db 19        ; in a, (0x19)         |
  0a3c dd 6e 0c     ; ld l, (ix + 0xc)     |
  0a3f dd 66 0d     ; ld h, (ix + 0xd)     |
  0a42 2c           ; inc l                |
  0a43 25           ; dec h                |
  0a44 28 03        ; jr z, 0xa49          |
  0a46 2d           ; dec l                |
  0a47 26 01        ; ld h, 0x1            |
  0a49 01 19 00     ; ld bc, 0x19          |
  0a4c db 1a        ; in a, (0x1a)         |
  0a4e db 1a        ; in a, (0x1a)         |
  0a50 b7           ; or a                 |
  0a51 f2 4e 0a     ; jp p, 0xa4e          |
  0a54 db 19        ; in a, (0x19)         |
  0a56 80           ; add a, b             |
  0a57 ed 40        ; in b, (c)            |
  0a59 2d           ; dec l                |
  0a5a 20 fa        ; jr nz, 0xa56         |
  0a5c 80           ; add a, b             |
  0a5d ed 40        ; in b, (c)            |
  0a5f 25           ; dec h                |
  0a60 20 fa        ; jr nz, 0xa5c         |
  0a62 b8           ; cp b                 |
  0a63 db 19        ; in a, (0x19)         |
  0a65 20 49        ; jr nz, 0xab0         |
  0a67 fe 10        ; cp 0x10              |
  0a69 20 45        ; jr nz, 0xab0         |
  0a6b 3a 22 42     ; ld a, (0x4222)       |
  0a6e 90           ; sub b                |
  0a6f 32 22 42     ; ld (0x4222), a       |
  0a72 21 9d 40     ; ld hl, 0x409d        |
  0a75 36 14        ; ld (hl), 0x14        |
  0a77 2a 20 42     ; ld hl, (0x4220)      |
  0a7a 44           ; ld b, h              |
  0a7b 4d           ; ld c, l              |
  0a7c 2a 99 40     ; ld hl, (0x4099)      | get hl = THERE (addr for disk transfer)
  0a7f 09           ; add hl, bc           |
  0a80 22 99 40     ; ld (0x4099), hl      | set THERE (addr for disk transfer) = hl
  0a83 1c           ; inc e                |
  0a84 dd 34 00     ; inc (ix + 0x0)       |
  0a87 20 03        ; jr nz, 0xa8c         |
  0a89 dd 34 01     ; inc (ix + 0x1)       |
  0a8c 21 9c 40     ; ld hl, 0x409c        |
  0a8f 35           ; dec (hl)             |
  0a90 20 9c        ; jr nz, 0xa2e         |
  0a92 3a 22 42     ; ld a, (0x4222)       |
  0a95 b7           ; or a                 |
  0a96 ca 45 09     ; jp z, 0x945          |
  0a99 21 29 42     ; ld hl, 0x4229        |
  0a9c 35           ; dec (hl)             |
  0a9d 3e 03        ; ld a, 0x3            |
  0a9f 28 15        ; jr z, 0xab6          |
  0aa1 2a 26 42     ; ld hl, (0x4226)      |
  0aa4 22 99 40     ; ld (0x4099), hl      | set THERE (addr for disk transfer) = hl
  0aa7 3a 28 42     ; ld a, (0x4228)       |
  0aaa 32 9c 40     ; ld (0x409c), a       | set SNRT  (# recs to be transfd) = a
  0aad c3 94 09     ; jp 0x994             |
  0ab0 3e 03        ; ld a, 0x3            |
  0ab2 21 9d 40     ; ld hl, 0x409d        |
  0ab5 35           ; dec (hl)             |
  0ab6 ca 36 09     ; jp z, 0x936          |
  0ab9 2a 99 40     ; ld hl, (0x4099)      | get hl = THERE (addr for disk transfer)
  0abc 22 a2 40     ; ld (0x40a2), hl      | set TRKS  (track # for drive 2) = hl
  0abf 3a 9c 40     ; ld a, (0x409c)       | get a = SNRT  (# recs to be transfd)
  0ac2 32 9b 40     ; ld (0x409b), a       | set NRT   (disk record count) = a
  0ac5 c3 9f 09     ; jp 0x99f             |
  0ac8 86           ; add a, (hl)          |
  0ac9 ed a3        ; outi                 |
  0acb 43           ; ld b, e              |
  0acc 05           ; dec b                |
  0acd 86           ; add a, (hl)          |
  0ace ed a3        ; outi                 |
  0ad0 c3 dc 09     ; jp 0x9dc             |
  0ad3 dd 4e 0c     ; ld c, (ix + 0xc)     |
  0ad6 dd 46 0d     ; ld b, (ix + 0xd)     |
  0ad9 7b           ; ld a, e              |
  0ada 2f           ; cpl                  |
  0adb 6f           ; ld l, a              |
  0adc 7a           ; ld a, d              |
  0add 2f           ; cpl                  |
  0ade 67           ; ld h, a              |
  0adf 09           ; add hl, bc           |
  0ae0 23           ; inc hl               |
  0ae1 38 05        ; jr c, 0xae8          |
  0ae3 50           ; ld d, b              |
  0ae4 59           ; ld e, c              |
  0ae5 21 00 00     ; ld hl, 0x0           |
  0ae8 22 b8 40     ; ld (0x40b8), hl      | set PART2 unused length = hl
  0aeb eb           ; ex de, hl            |
  0aec 22 b6 40     ; ld (0x40b6), hl      | set PART1 (length to be transferred) = hl
  0aef c9           ; ret                  |
  0af0 22 99 40     ; ld (0x4099), hl      | set THERE (addr for disk transfer) = hl
  0af3 32 9c 40     ; ld (0x409c), a       | set SNRT  (# recs to be transfd) = a
  0af6 6b           ; ld l, e              |
  0af7 62           ; ld h, d              |
  0af8 22 20 42     ; ld (0x4220), hl      |
  0afb dd 6e 0f     ; ld l, (ix + 0xf)     |
  0afe 3a a0 40     ; ld a, (0x40a0)       | get a = DISK  (selected disk drive #)
  0b01 bd           ; cp l                 |
  0b02 28 28        ; jr z, 0xb2c          |
  0b04 3e 80        ; ld a, 0x80           |
  0b06 65           ; ld h, l              |
  0b07 07           ; rlca                 |
  0b08 2d           ; dec l                |
  0b09 20 fc        ; jr nz, 0xb07         |
  0b0b 6c           ; ld l, h              |
  0b0c 67           ; ld h, a              |
  0b0d d3 1a        ; out (0x1a), a        |
  0b0f 97           ; sub a                |
  0b10 d3 0a        ; out (0xa), a         |
  0b12 db 1a        ; in a, (0x1a)         |
  0b14 0f           ; rrca                 |
  0b15 38 e4        ; jr c, 0xafb          |
  0b17 7c           ; ld a, h              |
  0b18 d3 1a        ; out (0x1a), a        |
  0b1a 7d           ; ld a, l              |
  0b1b 32 a0 40     ; ld (0x40a0), a       | set DISK  (selected disk drive #) = a
  0b1e 3e ff        ; ld a, 0xff           |
  0b20 32 a1 40     ; ld (0x40a1), a       | set TRKS  (track # for drive 1) = a
  0b23 2e 94        ; ld l, 0x94           |
  0b25 06 05        ; ld b, 0x5            |
  0b27 cd 2c 0c     ; call 0xc2c           |
  0b2a 10 fb        ; djnz 0xb27           |
  0b2c db 1a        ; in a, (0x1a)         |
  0b2e e6 40        ; and 0x40             |
  0b30 28 02        ; jr z, 0xb34          |
  0b32 97           ; sub a                |
  0b33 c9           ; ret                  |
  0b34 3e 05        ; ld a, 0x5            |
  0b36 dd e5        ; push ix              |
  0b38 c1           ; pop bc               |
  0b39 b7           ; or a                 |
  0b3a c9           ; ret                  |

  ;UNEXPLORED
  0b3b dd 7e 16     ; ld a, (ix + 0x16)    |
  0b3e dd 77 00     ; ld (ix + 0x0), a     |
  0b41 dd 7e 17     ; ld a, (ix + 0x17)    |
  0b44 dd 77 01     ; ld (ix + 0x1), a     |
  0b47 2a 99 40     ; ld hl, (0x4099)      | get hl = THERE (addr for disk transfer)
  0b4a 22 a2 40     ; ld (0x40a2), hl      | set TRKS  (track # for drive 2) = hl
  0b4d 22 26 42     ; ld (0x4226), hl      |
  0b50 3a 9c 40     ; ld a, (0x409c)       | get a = SNRT  (# recs to be transfd)
  0b53 32 9b 40     ; ld (0x409b), a       | set NRT   (disk record count) = a
  0b56 32 28 42     ; ld (0x4228), a       |
  0b59 c9           ; ret                  |
  0b5a dd 7e 00     ; ld a, (ix + 0x0)     |
  0b5d dd 77 16     ; ld (ix + 0x16), a    |
  0b60 dd 7e 01     ; ld a, (ix + 0x1)     |
  0b63 dd 77 17     ; ld (ix + 0x17), a    |
  0b66 c9           ; ret                  |
  0b67 dd 7e 01     ; ld a, (ix + 0x1)     |
  0b6a dd be 0b     ; cp (ix + 0xb)        |
  0b6d 20 06        ; jr nz, 0xb75         |
  0b6f dd 7e 00     ; ld a, (ix + 0x0)     |
  0b72 dd be 0a     ; cp (ix + 0xa)        |
  0b75 d8           ; ret c                |
  0b76 97           ; sub a                |
  0b77 3e 06        ; ld a, 0x6            |
  0b79 c9           ; ret                  |
  0b7a 0e 1a        ; ld c, 0x1a           |
  0b7c 21 10 27     ; ld hl, 0x2710        |
  0b7f f3           ; di                   |
  0b80 ed 78        ; in a, (c)            |
  0b82 ed 78        ; in a, (c)            |
  0b84 fa 95 0b     ; jp m, 0xb95          |
  0b87 2d           ; dec l                |
  0b88 20 f8        ; jr nz, 0xb82         |
  0b8a ed 78        ; in a, (c)            |
  0b8c fa 95 0b     ; jp m, 0xb95          |
  0b8f 25           ; dec h                |
  0b90 20 f0        ; jr nz, 0xb82         |
  0b92 fb           ; ei                   |
  0b93 3c           ; inc a                |
  0b94 c9           ; ret                  |
  0b95 db 19        ; in a, (0x19)         |
  0b97 fe 9e        ; cp 0x9e              |
  0b99 20 e5        ; jr nz, 0xb80         |
  0b9b 0d           ; dec c                |
  0b9c ed 40        ; in b, (c)            |
  0b9e ed 48        ; in c, (c)            |
  0ba0 db 19        ; in a, (0x19)         |
  0ba2 90           ; sub b                |
  0ba3 91           ; sub c                |
  0ba4 20 da        ; jr nz, 0xb80         |
  0ba6 fb           ; ei                   |
  0ba7 21 a1 40     ; ld hl, 0x40a1        |
  0baa 70           ; ld (hl), b           |
  0bab 21 a1 40     ; ld hl, 0x40a1        |
  0bae 3a a0 40     ; ld a, (0x40a0)       | get a = DISK  (selected disk drive #)
  0bb1 3c           ; inc a                |
  0bb2 e6 fe        ; and 0xfe             |
  0bb4 fe 06        ; cp 0x6               |
  0bb6 28 0b        ; jr z, 0xbc3          |
  0bb8 3a 1b 10     ; ld a, (0x101b)       |
  0bbb fe c3        ; cp 0xc3              |
  0bbd ca 1b 10     ; jp z, 0x101b         |
  0bc0 c3 00 00     ; jp 0x0               |
  0bc3 7e           ; ld a, (hl)           |
  0bc4 72           ; ld (hl), d           |
  0bc5 fe fe        ; cp 0xfe              |
  0bc7 d0           ; ret nc               |
  0bc8 47           ; ld b, a              |
  0bc9 21 00 4d     ; ld hl, 0x4d00        |
  0bcc bc           ; cp h                 |
  0bcd 38 06        ; jr c, 0xbd5          |
  0bcf ed 44        ; neg                  |
  0bd1 c6 99        ; add a, 0x99          |
  0bd3 47           ; ld b, a              |
  0bd4 2c           ; inc l                |
  0bd5 7a           ; ld a, d              |
  0bd6 bc           ; cp h                 |
  0bd7 38 07        ; jr c, 0xbe0          |
  0bd9 ed 44        ; neg                  |
  0bdb c6 99        ; add a, 0x99          |
  0bdd 57           ; ld d, a              |
  0bde cb fd        ; set 0x7, l           |
  0be0 7d           ; ld a, l              |
  0be1 b7           ; or a                 |
  0be2 28 18        ; jr z, 0xbfc          |
  0be4 fe 81        ; cp 0x81              |
  0be6 28 14        ; jr z, 0xbfc          |
  0be8 3a a0 40     ; ld a, (0x40a0)       | get a = DISK  (selected disk drive #)
  0beb 67           ; ld h, a              |
  0bec 3e 80        ; ld a, 0x80           |
  0bee 07           ; rlca                 |
  0bef 25           ; dec h                |
  0bf0 20 fc        ; jr nz, 0xbee         |
  0bf2 cb 85        ; res 0x0, l           |
  0bf4 b5           ; or l                 |
  0bf5 d3 1a        ; out (0x1a), a        |
  0bf7 2e 02        ; ld l, 0x2            |
  0bf9 cd 2c 0c     ; call 0xc2c           |
  0bfc 78           ; ld a, b              |
  0bfd 92           ; sub d                |
  0bfe 47           ; ld b, a              |
  0bff c8           ; ret z                |
  0c00 0e 00        ; ld c, 0x0            |
  0c02 30 05        ; jr nc, 0xc09         |
  0c04 0e 40        ; ld c, 0x40           |
  0c06 ed 44        ; neg                  |
  0c08 47           ; ld b, a              |
  0c09 79           ; ld a, c              |
  0c0a b7           ; or a                 |
  0c0b 20 09        ; jr nz, 0xc16         |
  0c0d db 1a        ; in a, (0x1a)         |
  0c0f e6 10        ; and 0x10             |
  0c11 28 03        ; jr z, 0xc16          |
  0c13 01 40 03     ; ld bc, 0x340         |
  0c16 3e 20        ; ld a, 0x20           |
  0c18 b1           ; or c                 |
  0c19 d3 1b        ; out (0x1b), a        |
  0c1b 79           ; ld a, c              |
  0c1c d3 1b        ; out (0x1b), a        |
  0c1e 2e d5        ; ld l, 0xd5           |
  0c20 cd 2c 0c     ; call 0xc2c           |
  0c23 cd 2c 0c     ; call 0xc2c           |
  0c26 05           ; dec b                |
  0c27 20 e0        ; jr nz, 0xc09         |
  0c29 2e 9d        ; ld l, 0x9d           |
  0c2b 04           ; inc b                |
  0c2c db 19        ; in a, (0x19)         |
  0c2e 2d           ; dec l                |
  0c2f db 19        ; in a, (0x19)         |
  0c31 c8           ; ret z                |
  0c32 18 f8        ; jr 0xc2c             |
  0c34 21 9d 40     ; ld hl, 0x409d        |
  0c37 36 0a        ; ld (hl), 0xa         |
  0c39 fb           ; ei                   |
  0c3a dd 6e 00     ; ld l, (ix + 0x0)     |
  0c3d dd 66 01     ; ld h, (ix + 0x1)     |
  0c40 dd 7e 0e     ; ld a, (ix + 0xe)     |
  0c43 dd 46 10     ; ld b, (ix + 0x10)    |
  0c46 05           ; dec b                |
  0c47 2f           ; cpl                  |
  0c48 3c           ; inc a                |
  0c49 5f           ; ld e, a              |
  0c4a 16 ff        ; ld d, 0xff           |
  0c4c 78           ; ld a, b              |
  0c4d 19           ; add hl, de           |
  0c4e 3c           ; inc a                |
  0c4f 38 fc        ; jr c, 0xc4d          |
  0c51 57           ; ld d, a              |
  0c52 7d           ; ld a, l              |
  0c53 93           ; sub e                |
  0c54 5f           ; ld e, a              |
  0c55 cd 7a 0b     ; call 0xb7a           |
  0c58 21 a1 40     ; ld hl, 0x40a1        |
  0c5b 56           ; ld d, (hl)           |
  0c5c 28 2f        ; jr z, 0xc8d          |
  0c5e 2e 9d        ; ld l, 0x9d           |
  0c60 cd 2c 0c     ; call 0xc2c           |
  0c63 21 00 80     ; ld hl, 0x8000        |
  0c66 0e 1a        ; ld c, 0x1a           |
  0c68 2d           ; dec l                |
  0c69 28 0b        ; jr z, 0xc76          |
  0c6b ed 40        ; in b, (c)            |
  0c6d f2 68 0c     ; jp p, 0xc68          |
  0c70 db 19        ; in a, (0x19)         |
  0c72 d6 9b        ; sub 0x9b             |
  0c74 28 17        ; jr z, 0xc8d          |
  0c76 25           ; dec h                |
  0c77 20 ef        ; jr nz, 0xc68         |
  0c79 21 9d 40     ; ld hl, 0x409d        |
  0c7c 35           ; dec (hl)             |
  0c7d 01 00 01     ; ld bc, 0x100         |
  0c80 28 3a        ; jr z, 0xcbc          |
  0c82 db 1a        ; in a, (0x1a)         |
  0c84 e6 10        ; and 0x10             |
  0c86 20 34        ; jr nz, 0xcbc         |
  0c88 cd 09 0c     ; call 0xc09           |
  0c8b 18 d1        ; jr 0xc5e             |
  0c8d 7b           ; ld a, e              |
  0c8e dd 6e 0e     ; ld l, (ix + 0xe)     |
  0c91 bd           ; cp l                 |
  0c92 30 a5        ; jr nc, 0xc39         |
  0c94 21 00 08     ; ld hl, 0x800         |
  0c97 0e 1a        ; ld c, 0x1a           |
  0c99 f3           ; di                   |
  0c9a db 1a        ; in a, (0x1a)         |
  0c9c ed 78        ; in a, (c)            |
  0c9e f2 9c 0c     ; jp p, 0xc9c          |
  0ca1 db 19        ; in a, (0x19)         |
  0ca3 fe 9e        ; cp 0x9e              |
  0ca5 20 0f        ; jr nz, 0xcb6         |
  0ca7 db 19        ; in a, (0x19)         |
  0ca9 ba           ; cp d                 |
  0caa 20 14        ; jr nz, 0xcc0         |
  0cac db 19        ; in a, (0x19)         |
  0cae bb           ; cp e                 |
  0caf 20 05        ; jr nz, 0xcb6         |
  0cb1 db 19        ; in a, (0x19)         |
  0cb3 93           ; sub e                |
  0cb4 92           ; sub d                |
  0cb5 c8           ; ret z                |
  0cb6 fb           ; ei                   |
  0cb7 2b           ; dec hl               |
  0cb8 7d           ; ld a, l              |
  0cb9 b4           ; or h                 |
  0cba 20 dd        ; jr nz, 0xc99         |
  0cbc 3e 01        ; ld a, 0x1            |
  0cbe b7           ; or a                 |
  0cbf c9           ; ret                  |
  0cc0 4f           ; ld c, a              |
  0cc1 db 19        ; in a, (0x19)         |
  0cc3 47           ; ld b, a              |
  0cc4 db 19        ; in a, (0x19)         |
  0cc6 91           ; sub c                |
  0cc7 90           ; sub b                |
  0cc8 41           ; ld b, c              |
  0cc9 0e 1a        ; ld c, 0x1a           |
  0ccb 20 cc        ; jr nz, 0xc99         |
  0ccd db 19        ; in a, (0x19)         |
  0ccf fe 10        ; cp 0x10              |
  0cd1 20 c6        ; jr nz, 0xc99         |
  0cd3 78           ; ld a, b              |
  0cd4 32 a1 40     ; ld (0x40a1), a       | set TRKS  (track # for drive 1) = a
  0cd7 21 9d 40     ; ld hl, 0x409d        |
  0cda 35           ; dec (hl)             |
  0cdb 28 df        ; jr z, 0xcbc          |
  0cdd c3 39 0c     ; jp 0xc39             |
  0ce0 01 0a 00     ; ld bc, 0xa           |
  0ce3 54           ; ld d, h              |
  0ce4 5d           ; ld e, l              |
  0ce5 09           ; add hl, bc           |
  0ce6 eb           ; ex de, hl            |
  0ce7 7e           ; ld a, (hl)           |
  0ce8 36 00        ; ld (hl), 0x0         |
  0cea 12           ; ld (de), a           |
  0ceb 23           ; inc hl               |
  0cec 13           ; inc de               |
  0ced 7e           ; ld a, (hl)           |
  0cee 36 00        ; ld (hl), 0x0         |
  0cf0 12           ; ld (de), a           |
  0cf1 13           ; inc de               |
  0cf2 13           ; inc de               |
  0cf3 13           ; inc de               |
  0cf4 13           ; inc de               |
  0cf5 1a           ; ld a, (de)           |
  0cf6 32 ad 40     ; ld (0x40ad), a       | set Disk # = a
  0cf9 cd e1 0f     ; call 0xfe1           |
  0cfc 12           ; ld (de), a           |
  0cfd 11 02 00     ; ld de, 0x2           |
  0d00 01 9e 40     ; ld bc, 0x409e        |
  0d03 02           ; ld (bc), a           |
  0d04 03           ; inc bc               |
  0d05 02           ; ld (bc), a           |
  0d06 0b           ; dec bc               |
  0d07 3e 08        ; ld a, 0x8            |
  0d09 e5           ; push hl              |
  0d0a 23           ; inc hl               |
  0d0b cd 09 08     ; call 0x809           |
  0d0e e1           ; pop hl               |
  0d0f 20 09        ; jr nz, 0xd1a         |
  0d11 2b           ; dec hl               |
  0d12 3e 01        ; ld a, 0x1            |
  0d14 11 14 00     ; ld de, 0x14          |
  0d17 cc 03 08     ; call z, 0x803        |
  0d1a 01 df 0d     ; ld bc, 0xddf         |
  0d1d c9           ; ret                  |

  ;loader()
  0d1e 21 d0 40     ; ld hl, 0x40d0        | loader() - hl = FD for loaded file
  0d21 cd 30 08     ; call 0x830           | call OPEN
  0d24 c0           ; ret nz               |
  0d25 3a da 40     ; ld a, (0x40da)       | get a = Number of Records (LFILE)
  0d28 4f           ; ld c, a              |
  0d29 06 01        ; ld b, 0x1            |
  0d2b 78           ; ld a, b              |
  0d2c b9           ; cp c                 |
  0d2d 30 34        ; jr nc, 0xd63         |
  0d2f 21 d0 40     ; ld hl, 0x40d0        | hl = Record #
  0d32 70           ; ld (hl), b           |
  0d33 04           ; inc b                |
  0d34 04           ; inc b                |
  0d35 11 ff 00     ; ld de, 0xff          |
  0d38 c5           ; push bc              |
  0d39 01 d0 40     ; ld bc, 0x40d0        |
  0d3c 21 00 42     ; ld hl, 0x4200        |
  0d3f 3e 01        ; ld a, 0x1            | Read 1 record
  0d41 cd 00 08     ; call 0x800           | call READ
  0d44 e1           ; pop hl               |
  0d45 c0           ; ret nz               |
  0d46 e5           ; push hl              |
  0d47 21 ff 42     ; ld hl, 0x42ff        |
  0d4a 77           ; ld (hl), a           |
  0d4b 2c           ; inc l                |
  0d4c c1           ; pop bc               |
  0d4d 7e           ; ld a, (hl)           |
  0d4e b7           ; or a                 |
  0d4f 28 da        ; jr z, 0xd2b          |
  0d51 c5           ; push bc              |
  0d52 23           ; inc hl               |
  0d53 5e           ; ld e, (hl)           |
  0d54 23           ; inc hl               |
  0d55 56           ; ld d, (hl)           |
  0d56 23           ; inc hl               |
  0d57 4e           ; ld c, (hl)           |
  0d58 0c           ; inc c                |
  0d59 0d           ; dec c                |
  0d5a 23           ; inc hl               |
  0d5b 28 ef        ; jr z, 0xd4c          |
  0d5d 06 00        ; ld b, 0x0            |
  0d5f ed b0        ; ldir                 |
  0d61 18 e9        ; jr 0xd4c             |
  0d63 3e 01        ; ld a, 0x1            |
  0d65 a0           ; and b                |
  0d66 c8           ; ret z                |
  0d67 06 00        ; ld b, 0x0            |
  0d69 18 c0        ; jr 0xd2b             |

  ;clrdk()
  0d6b 21 8b 0d     ; ld hl, 0xd8b         |
  0d6e 11 fa 13     ; ld de, 0x13fa        |
  0d71 06 03        ; ld b, 0x3            |
  0d73 1a           ; ld a, (de)           |
  0d74 be           ; cp (hl)              | check if "IWS" version
  0d75 20 07        ; jr nz, 0xd7e         |
  0d77 23           ; inc hl               |
  0d78 13           ; inc de               |
  0d79 10 f8        ; djnz 0xd73           |
  0d7b cd 15 10     ; call 0x1015          | call IWS specific code

  ;deselect all disks()
  0d7e 97           ; sub a                |
  0d7f 32 a0 40     ; ld (0x40a0), a       | set DISK  (selected disk drive #) = a
  0d82 d3 1b        ; out (0x1b), a        |
  0d84 d3 0b        ; out (0xb), a         |
  0d86 d3 1a        ; out (0x1a), a        |
  0d88 d3 0a        ; out (0xa), a         |
  0d8a c9           ; ret                  |

  ;text string? - IWS
  0d8b 49           ; ld c, c              |
  0d8c 57           ; ld d, a              |
  0d8d 53           ; ld d, e              |

  ;report()
  0d8e c5           ; push bc              |
  0d8f f5           ; push af              |
  0d90 cd 6b 0d     ; call 0xd6b           | clrdk()
  0d93 21 ec 0d     ; ld hl, 0xdec         |
  0d96 0e 01        ; ld c, 0x1            |
  0d98 cd 27 00     ; call 0x27            | print "CR?"
  0d9b f1           ; pop af               |
  0d9c fe 04        ; cp 0x4               | 0x4 = Key not found
  0d9e 28 33        ; jr z, 0xdd3          |
  0da0 fe 09        ; cp 0x9               |
  0da2 fa a7 0d     ; jp m, 0xda7          |
  0da5 3e 09        ; ld a, 0x9            |

  ;print nth error message
  0da7 21 ed 0d     ; ld hl, 0xded         | Start of error messages
  0daa 4e           ; ld c, (hl)           |
  0dab cb 79        ; bit 0x7, c           | Message separators have Bit 7 set
  0dad 23           ; inc hl               |
  0dae 28 fa        ; jr z, 0xdaa          |
  0db0 3d           ; dec a                |
  0db1 20 f7        ; jr nz, 0xdaa         |
  0db3 cb b9        ; res 0x7, c           |
  0db5 cd 27 00     ; call 0x27            | print:  "NOT FOUND"
  0db8 0e 04        ; ld c, 0x4            |
  0dba 21 e8 0d     ; ld hl, 0xde8         | string: " ON "
  0dbd cd 27 00     ; call 0x27            | print:  " ON"
  0dc0 0e 08        ; ld c, 0x8            |
  0dc2 e1           ; pop hl               |
  0dc3 23           ; inc hl               |
  0dc4 23           ; inc hl               |
  0dc5 cd 27 00     ; call 0x27            | print:  "INDEX"
  0dc8 cd 30 00     ; call 0x30            | STOP
  0dcb 0e 01        ; ld c, 0x1            |
  0dcd 21 ec 0d     ; ld hl, 0xdec         |
  0dd0 c3 27 00     ; jp 0x27              |
  0dd3 2a 99 40     ; ld hl, (0x4099)      | get hl = THERE (addr for disk transfer)
  0dd6 3a 9c 40     ; ld a, (0x409c)       | get a = SNRT  (# recs to be transfd)
  0dd9 4f           ; ld c, a              |
  0dda cd 27 00     ; call 0x27            |
  0ddd 3e 04        ; ld a, 0x4            | A=4 - fourth err msg: "NOT FOUND"
  0ddf 18 c6        ; jr 0xda7             |

  ;text strings - INDEX .. WEIRD ERR
  0de1 49           ; ld c, c              |
  0de2 4e           ; ld c, (hl)           |
  0de3 44           ; ld b, h              |
  0de4 45           ; ld b, l              |
  0de5 58           ; ld e, b              |
  0de6 20 20        ; jr nz, 0xe08         |
  0de8 20 4f        ; jr nz, 0xe39         |
  0dea 4e           ; ld c, (hl)           |
  0deb 20 0d        ; jr nz, 0xdfa         |
  0ded 8a           ; adc a, d             |
  0dee 46           ; ld b, (hl)           |
  0def 4f           ; ld c, a              |
  0df0 52           ; ld d, d              |
  0df1 4d           ; ld c, l              |
  0df2 41           ; ld b, c              |
  0df3 54           ; ld d, h              |
  0df4 20 45        ; jr nz, 0xe3b         |
  0df6 52           ; ld d, d              |
  0df7 52           ; ld d, d              |
  0df8 88           ; adc a, b             |
  0df9 52           ; ld d, d              |
  0dfa 45           ; ld b, l              |
  0dfb 41           ; ld b, c              |
  0dfc 44           ; ld b, h              |
  0dfd 20 45        ; jr nz, 0xe44         |
  0dff 52           ; ld d, d              |
  0e00 52           ; ld d, d              |
  0e01 89           ; adc a, c             |
  0e02 57           ; ld d, a              |
  0e03 52           ; ld d, d              |
  0e04 49           ; ld c, c              |
  0e05 54           ; ld d, h              |
  0e06 45           ; ld b, l              |
  0e07 20 45        ; jr nz, 0xe4e         |
  0e09 52           ; ld d, d              |
  0e0a 52           ; ld d, d              |
  0e0b 8a           ; adc a, d             |
  0e0c 20 4e        ; jr nz, 0xe5c         |
  0e0e 4f           ; ld c, a              |
  0e0f 54           ; ld d, h              |
  0e10 20 46        ; jr nz, 0xe58         |
  0e12 4f           ; ld c, a              |
  0e13 55           ; ld d, l              |
  0e14 4e           ; ld c, (hl)           |
  0e15 44           ; ld b, h              |
  0e16 87           ; add a, a             |
  0e17 4e           ; ld c, (hl)           |
  0e18 4f           ; ld c, a              |
  0e19 20 44        ; jr nz, 0xe5f         |
  0e1b 49           ; ld c, c              |
  0e1c 53           ; ld d, e              |
  0e1d 4b           ; ld c, e              |
  0e1e 8a           ; adc a, d             |
  0e1f 50           ; ld d, b              |
  0e20 41           ; ld b, c              |
  0e21 53           ; ld d, e              |
  0e22 53           ; ld d, e              |
  0e23 45           ; ld b, l              |
  0e24 44           ; ld b, h              |
  0e25 20 45        ; jr nz, 0xe6c         |
  0e27 4f           ; ld c, a              |
  0e28 46           ; ld b, (hl)           |
  0e29 8d           ; adc a, l             |
  0e2a 57           ; ld d, a              |
  0e2b 52           ; ld d, d              |
  0e2c 49           ; ld c, c              |
  0e2d 54           ; ld d, h              |
  0e2e 45           ; ld b, l              |
  0e2f 20 50        ; jr nz, 0xe81         |
  0e31 52           ; ld d, d              |
  0e32 4f           ; ld c, a              |
  0e33 54           ; ld d, h              |
  0e34 45           ; ld b, l              |
  0e35 43           ; ld b, e              |
  0e36 54           ; ld d, h              |
  0e37 8d           ; adc a, l             |
  0e38 44           ; ld b, h              |
  0e39 41           ; ld b, c              |
  0e3a 54           ; ld d, h              |
  0e3b 41           ; ld b, c              |
  0e3c 20 4c        ; jr nz, 0xe8a         |
  0e3e 49           ; ld c, c              |
  0e3f 4e           ; ld c, (hl)           |
  0e40 4b           ; ld c, e              |
  0e41 20 45        ; jr nz, 0xe88         |
  0e43 52           ; ld d, d              |
  0e44 52           ; ld d, d              |
  0e45 89           ; adc a, c             |
  0e46 57           ; ld d, a              |
  0e47 45           ; ld b, l              |
  0e48 49           ; ld c, c              |
  0e49 52           ; ld d, d              |
  0e4a 44           ; ld b, h              |
  0e4b 20 45        ; jr nz, 0xe92         |
  0e4d 52           ; ld d, d              |
  0e4e 52           ; ld d, d              |

  ;key search()
  0e4f cd b8 0f     ; call 0xfb8           |
  0e52 c3 09 10     ; jp 0x1009            |
  0e55 e5           ; push hl              |
  0e56 d5           ; push de              |
  0e57 cd f0 0a     ; call 0xaf0           |
  0e5a d1           ; pop de               |
  0e5b e1           ; pop hl               |
  0e5c c0           ; ret nz               |
  0e5d 22 4a 42     ; ld (0x424a), hl      |
  0e60 dd 7e 0a     ; ld a, (ix + 0xa)     |
  0e63 dd b6 0b     ; or (ix + 0xb)        |
  0e66 ca 98 0f     ; jp z, 0xf98          |
  0e69 3a 9c 40     ; ld a, (0x409c)       | get a = SNRT  (# recs to be transfd)
  0e6c b7           ; or a                 |
  0e6d 28 f7        ; jr z, 0xe66          |
  0e6f 4f           ; ld c, a              |
  0e70 06 00        ; ld b, 0x0            |
  0e72 09           ; add hl, bc           |
  0e73 22 20 42     ; ld (0x4220), hl      |
  0e76 47           ; ld b, a              |
  0e77 3e 9b        ; ld a, 0x9b           |
  0e79 2b           ; dec hl               |
  0e7a 86           ; add a, (hl)          |
  0e7b 10 fc        ; djnz 0xe79           |
  0e7d 08           ; ex af, af'           |
  0e7e c5           ; push bc              |
  0e7f e1           ; pop hl               |
  0e80 19           ; add hl, de           |
  0e81 dd 7e 0c     ; ld a, (ix + 0xc)     |
  0e84 95           ; sub l                |
  0e85 6f           ; ld l, a              |
  0e86 dd 7e 0d     ; ld a, (ix + 0xd)     |
  0e89 9c           ; sbc a, h             |
  0e8a da 98 0f     ; jp c, 0xf98          |
  0e8d 08           ; ex af, af'           |
  0e8e 67           ; ld h, a              |
  0e8f 22 50 42     ; ld (0x4250), hl      |
  0e92 08           ; ex af, af'           |
  0e93 67           ; ld h, a              |
  0e94 b5           ; or l                 |
  0e95 2b           ; dec hl               |
  0e96 7c           ; ld a, h              |
  0e97 21 5b 0f     ; ld hl, 0xf5b         |
  0e9a 28 09        ; jr z, 0xea5          |
  0e9c b7           ; or a                 |
  0e9d 21 55 0f     ; ld hl, 0xf55         |
  0ea0 28 03        ; jr z, 0xea5          |
  0ea2 21 50 0f     ; ld hl, 0xf50         |
  0ea5 e5           ; push hl              |
  0ea6 fd e1        ; pop iy               |
  0ea8 63           ; ld h, e              |
  0ea9 2e 1a        ; ld l, 0x1a           |
  0eab 22 52 42     ; ld (0x4252), hl      |
  0eae 61           ; ld h, c              |
  0eaf 2d           ; dec l                |
  0eb0 22 4c 42     ; ld (0x424c), hl      |
  0eb3 7a           ; ld a, d              |
  0eb4 b3           ; or e                 |
  0eb5 21 33 0f     ; ld hl, 0xf33         |
  0eb8 28 0b        ; jr z, 0xec5          |
  0eba 1b           ; dec de               |
  0ebb 7a           ; ld a, d              |
  0ebc b7           ; or a                 |
  0ebd 21 2d 0f     ; ld hl, 0xf2d         |
  0ec0 28 03        ; jr z, 0xec5          |
  0ec2 21 28 0f     ; ld hl, 0xf28         |
  0ec5 22 4e 42     ; ld (0x424e), hl      |
  0ec8 21 46 0f     ; ld hl, 0xf46         |
  0ecb 22 54 42     ; ld (0x4254), hl      |
  0ece cd aa 0f     ; call 0xfaa           |
  0ed1 dd 6e 00     ; ld l, (ix + 0x0)     |
  0ed4 dd 66 01     ; ld h, (ix + 0x1)     |
  0ed7 22 48 42     ; ld (0x4248), hl      |
  0eda 1e ff        ; ld e, 0xff           |
  0edc 3e 24        ; ld a, 0x24           |
  0ede 32 9d 40     ; ld (0x409d), a       | set ERC   (disk error count) = a
  0ee1 cd 8d 0c     ; call 0xc8d           |
  0ee4 20 2b        ; jr nz, 0xf11         |
  0ee6 d5           ; push de              |
  0ee7 16 00        ; ld d, 0x0            |
  0ee9 ed 73 a2 40  ; ld (0x40a2), sp      | set TRKS  (track # for drive 2) = sp
  0eed 31 4a 42     ; ld sp, 0x424a        |
  0ef0 e1           ; pop hl               |
  0ef1 c1           ; pop bc               |
  0ef2 d9           ; exx                  |
  0ef3 e1           ; pop hl               |
  0ef4 d1           ; pop de               |
  0ef5 7a           ; ld a, d              |
  0ef6 08           ; ex af, af'           |
  0ef7 c1           ; pop bc               |
  0ef8 ed 78        ; in a, (c)            |
  0efa ed 78        ; in a, (c)            |
  0efc f2 fa 0e     ; jp p, 0xefa          |
  0eff 0d           ; dec c                |
  0f00 ed 78        ; in a, (c)            |
  0f02 fe 9b        ; cp 0x9b              |
  0f04 20 02        ; jr nz, 0xf08         |
  0f06 08           ; ex af, af'           |
  0f07 e9           ; jp (hl)              |
  0f08 ed 7b a2 40  ; ld sp, (0x40a2)      | get sp = TRKS  (track # for drive 2)
  0f0c 3e 02        ; ld a, 0x2            |
  0f0e d1           ; pop de               |
  0f0f 18 04        ; jr 0xf15             |
  0f11 1e ff        ; ld e, 0xff           |
  0f13 3e 01        ; ld a, 0x1            |
  0f15 21 9d 40     ; ld hl, 0x409d        |
  0f18 35           ; dec (hl)             |
  0f19 20 c6        ; jr nz, 0xee1         |
  0f1b 2a 48 42     ; ld hl, (0x4248)      |
  0f1e dd 75 00     ; ld (ix + 0x0), l     |
  0f21 dd 74 01     ; ld (ix + 0x1), h     |
  0f24 b7           ; or a                 |
  0f25 c3 45 09     ; jp 0x945             |
  0f28 ed 50        ; in d, (c)            |
  0f2a 82           ; add a, d             |
  0f2b 10 fb        ; djnz 0xf28           |
  0f2d ed 50        ; in d, (c)            |
  0f2f 82           ; add a, d             |
  0f30 10 fb        ; djnz 0xf2d           |
  0f32 57           ; ld d, a              |
  0f33 43           ; ld b, e              |
  0f34 d9           ; exx                  |
  0f35 db 19        ; in a, (0x19)         |
  0f37 96           ; sub (hl)             |
  0f38 c0           ; ret nz               |
  0f39 23           ; inc hl               |
  0f3a 10 f9        ; djnz 0xf35           |
  0f3c d9           ; exx                  |
  0f3d db 19        ; in a, (0x19)         |
  0f3f fd e9        ; jp (iy)              |
  0f41 ed 50        ; in d, (c)            |
  0f43 23           ; inc hl               |
  0f44 96           ; sub (hl)             |
  0f45 82           ; add a, d             |
  0f46 10 f9        ; djnz 0xf41           |
  0f48 47           ; ld b, a              |
  0f49 db 19        ; in a, (0x19)         |
  0f4b d9           ; exx                  |
  0f4c fd e9        ; jp (iy)              |
  0f4e ed 50        ; in d, (c)            |
  0f50 82           ; add a, d             |
  0f51 10 fb        ; djnz 0xf4e           |
  0f53 ed 50        ; in d, (c)            |
  0f55 82           ; add a, d             |
  0f56 10 fb        ; djnz 0xf53           |
  0f58 57           ; ld d, a              |
  0f59 db 19        ; in a, (0x19)         |
  0f5b 92           ; sub d                |
  0f5c d9           ; exx                  |
  0f5d 90           ; sub b                |
  0f5e 20 a8        ; jr nz, 0xf08         |
  0f60 db 19        ; in a, (0x19)         |
  0f62 fe 10        ; cp 0x10              |
  0f64 20 a2        ; jr nz, 0xf08         |
  0f66 eb           ; ex de, hl            |
  0f67 2a 20 42     ; ld hl, (0x4220)      |
  0f6a ed 52        ; sbc hl, de           |
  0f6c ed 7b a2 40  ; ld sp, (0x40a2)      | get sp = TRKS  (track # for drive 2)
  0f70 d1           ; pop de               |
  0f71 c2 77 0f     ; jp nz, 0xf77         |
  0f74 97           ; sub a                |
  0f75 18 30        ; jr 0xfa7             |
  0f77 1c           ; inc e                |
  0f78 dd 34 00     ; inc (ix + 0x0)       |
  0f7b c2 81 0f     ; jp nz, 0xf81         |
  0f7e dd 34 01     ; inc (ix + 0x1)       |
  0f81 cd 67 0b     ; call 0xb67           |
  0f84 cc ae 0f     ; call z, 0xfae        |
  0f87 2a 48 42     ; ld hl, (0x4248)      |
  0f8a 7d           ; ld a, l              |
  0f8b dd be 00     ; cp (ix + 0x0)        |
  0f8e c2 dc 0e     ; jp nz, 0xedc         |
  0f91 7c           ; ld a, h              |
  0f92 dd 96 01     ; sub (ix + 0x1)       |
  0f95 c2 dc 0e     ; jp nz, 0xedc         |
  0f98 dd 7e 0a     ; ld a, (ix + 0xa)     |
  0f9b dd 77 00     ; ld (ix + 0x0), a     |
  0f9e dd 7e 0b     ; ld a, (ix + 0xb)     |
  0fa1 dd 77 01     ; ld (ix + 0x1), a     |
  0fa4 3e 04        ; ld a, 0x4            |
  0fa6 b7           ; or a                 |
  0fa7 c3 45 09     ; jp 0x945             |
  0faa cd 67 0b     ; call 0xb67           |
  0fad c0           ; ret nz               |
  0fae 97           ; sub a                |
  0faf dd 77 00     ; ld (ix + 0x0), a     |
  0fb2 dd 77 01     ; ld (ix + 0x1), a     |
  0fb5 1e ff        ; ld e, 0xff           |
  0fb7 c9           ; ret                  |

  ;write()
  0fb8 c5           ; push bc              |
  0fb9 dd e1        ; pop ix               |
  0fbb 08           ; ex af, af'           |
  0fbc 3a a0 40     ; ld a, (0x40a0)       | get a = DISK  (selected disk drive #)
  0fbf dd be 0f     ; cp (ix + 0xf)        |
  0fc2 28 03        ; jr z, 0xfc7          |
  0fc4 cd 7e 0d     ; call 0xd7e           | deselect disks
  0fc7 3a 00 10     ; ld a, (0x1000)       |
  0fca 3c           ; inc a                |
  0fcb ca da 0f     ; jp z, 0xfda          | jump to 0xfda if no ROM in addr 0x1000
  0fce dd 7e 0f     ; ld a, (ix + 0xf)     | a = Disk #
  0fd1 3c           ; inc a                |
  0fd2 e6 fe        ; and 0xfe             |
  0fd4 fe 06        ; cp 0x6               | max disk # reached ?
  0fd6 28 02        ; jr z, 0xfda          |
  0fd8 08           ; ex af, af'           |
  0fd9 c9           ; ret                  | no, return ok?
  0fda e3           ; ex (sp), hl          |
  0fdb 23           ; inc hl               |
  0fdc 23           ; inc hl               |
  0fdd 23           ; inc hl               |
  0fde e3           ; ex (sp), hl          |
  0fdf 08           ; ex af, af'           |
  0fe0 c9           ; ret                  |

  ;Setup disk: Records:88, Rec per Track: 130, Rec len 24 bytes
  0fe1 d9           ; exx                  |
  0fe2 3a ad 40     ; ld a, (0x40ad)       | get a = Disk #
  0fe5 3c           ; inc a                |
  0fe6 e6 fe        ; and 0xfe             |
  0fe8 fe 06        ; cp 0x6               |
  0fea 21 58 00     ; ld hl, 0x58          | # records = 0x58 (88)
  0fed 28 02        ; jr z, 0xff1          |
  0fef 2e 82        ; ld l, 0x82           | Records per Track = 0x82 (130)
  0ff1 22 a8 40     ; ld (0x40a8), hl      | set Number of Records = hl
  0ff4 7d           ; ld a, l              |
  0ff5 32 ac 40     ; ld (0x40ac), a       | set Records/Track = a
  0ff8 2e 28        ; ld l, 0x28           | Record Length = 0x28 (24)
  0ffa 22 aa 40     ; ld (0x40aa), hl      | set Record Length = hl
  0ffd 97           ; sub a                |
  0ffe d9           ; exx                  |
  0fff c9           ; ret                  |

  ;UNEXPLORED
  1000 c3 8d 10     ; jp 0x108d            |

  ;write?
  1003 c3 44 11     ; jp 0x1144            |

  ;UNEXPLORED
  1006 c3 69 11     ; jp 0x1169            |

  ;key search jump vector
  1009 c3 6b 16     ; jp 0x166b            |

  ;UNEXPLORED
  100c c3 30 10     ; jp 0x1030            |
  100f c3 18 15     ; jp 0x1518            |
  1012 c3 c8 14     ; jp 0x14c8            |

  ;unknown IWS code jump vector
  1015 c3 6a 15     ; jp 0x156a            |
  1018 c3 ac 15     ; jp 0x15ac            |
  101b c3 99 13     ; jp 0x1399            |
  101e c3 1b 14     ; jp 0x141b            |
  1021 c3 2f 11     ; jp 0x112f            |
  1024 c3 3f 11     ; jp 0x113f            |
  1027 c3 25 13     ; jp 0x1325            |
  102a c3 44 13     ; jp 0x1344            |
  102d c3 51 13     ; jp 0x1351            |
  1030 97           ; sub a                |
  1031 32 ad 40     ; ld (0x40ad), a       | set Disk # = a
  1034 3e 80        ; ld a, 0x80           |
  1036 32 13 42     ; ld (0x4213), a       |
  1039 e5           ; push hl              |
  103a 3a a5 40     ; ld a, (0x40a5)       | get a = AD (access denined)
  103d 2f           ; cpl                  |
  103e 47           ; ld b, a              |
  103f 21 13 42     ; ld hl, 0x4213        |
  1042 7e           ; ld a, (hl)           |
  1043 07           ; rlca                 |
  1044 77           ; ld (hl), a           |
  1045 21 ad 40     ; ld hl, 0x40ad        |
  1048 34           ; inc (hl)             |
  1049 a0           ; and b                |
  104a e1           ; pop hl               |
  104b 28 2e        ; jr z, 0x107b         |
  104d e5           ; push hl              |
  104e 11 02 00     ; ld de, 0x2           |
  1051 01 9f 40     ; ld bc, 0x409f        |
  1054 97           ; sub a                |
  1055 02           ; ld (bc), a           |
  1056 0b           ; dec bc               |
  1057 02           ; ld (bc), a           |
  1058 3e 08        ; ld a, 0x8            |
  105a 23           ; inc hl               |
  105b 23           ; inc hl               |
  105c cd 09 10     ; call 0x1009          |
  105f e1           ; pop hl               |
  1060 c2 7b 10     ; jp nz, 0x107b        |
  1063 11 18 00     ; ld de, 0x18          |
  1066 3e 01        ; ld a, 0x1            |
  1068 cd 00 10     ; call 0x1000          |
  106b 21 ad 40     ; ld hl, 0x40ad        |
  106e 46           ; ld b, (hl)           |
  106f 2a 99 40     ; ld hl, (0x4099)      | get hl = THERE (addr for disk transfer)
  1072 11 0f 00     ; ld de, 0xf           |
  1075 19           ; add hl, de           |
  1076 70           ; ld (hl), b           |
  1077 01 03 16     ; ld bc, 0x1603        |
  107a c9           ; ret                  |
  107b e5           ; push hl              |
  107c 21 13 42     ; ld hl, 0x4213        |
  107f 7e           ; ld a, (hl)           |
  1080 fe 80        ; cp 0x80              |
  1082 fa 3a 10     ; jp m, 0x103a         |
  1085 3e 04        ; ld a, 0x4            |
  1087 b7           ; or a                 |
  1088 e1           ; pop hl               |
  1089 01 03 16     ; ld bc, 0x1603        |
  108c c9           ; ret                  |
  108d cd de 12     ; call 0x12de          |
  1090 c0           ; ret nz               |
  1091 21 9d 40     ; ld hl, 0x409d        |
  1094 36 20        ; ld (hl), 0x20        | set ERC (error count) to 32
  1096 cd 44 13     ; call 0x1344          |
  1099 cd c1 12     ; call 0x12c1          |
  109c cd 25 13     ; call 0x1325          |
  109f 1e ff        ; ld e, 0xff           |
  10a1 cd 51 13     ; call 0x1351          |
  10a4 ca 2f 11     ; jp z, 0x112f         |
  10a7 cd 75 14     ; call 0x1475          |
  10aa c2 2f 11     ; jp nz, 0x112f        |
  10ad 3a b8 40     ; ld a, (0x40b8)       | get a = PART2 unused length
  10b0 3c           ; inc a                |
  10b1 47           ; ld b, a              |
  10b2 0e 09        ; ld c, 0x9            |
  10b4 d9           ; exx                  |
  10b5 2a b6 40     ; ld hl, (0x40b6)      | get hl = PART1 (length to be transferred)
  10b8 7c           ; ld a, h              |
  10b9 1f           ; rra                  |
  10ba 7d           ; ld a, l              |
  10bb 1f           ; rra                  |
  10bc 47           ; ld b, a              |
  10bd 21 e7 10     ; ld hl, 0x10e7        |
  10c0 30 04        ; jr nc, 0x10c6        |
  10c2 21 ed 10     ; ld hl, 0x10ed        |
  10c5 04           ; inc b                |
  10c6 e5           ; push hl              |
  10c7 2a a2 40     ; ld hl, (0x40a2)      | get hl = TRKS  (track # for drive 2)
  10ca 2b           ; dec hl               |
  10cb 56           ; ld d, (hl)           |
  10cc db 0a        ; in a, (0xa)          |
  10ce 0e 0a        ; ld c, 0xa            |
  10d0 ed 78        ; in a, (c)            |
  10d2 f2 d0 10     ; jp p, 0x10d0         |
  10d5 0d           ; dec c                |
  10d6 db 09        ; in a, (0x9)          |
  10d8 fe 9b        ; cp 0x9b              |
  10da c8           ; ret z                |
  10db e1           ; pop hl               |
  10dc 21 9d 40     ; ld hl, 0x409d        |
  10df 3e 02        ; ld a, 0x2            |
  10e1 35           ; dec (hl)             |
  10e2 28 4b        ; jr z, 0x112f         |
  10e4 18 b9        ; jr 0x109f            |
  10e6 23           ; inc hl               |
  10e7 ed 58        ; in e, (c)            |
  10e9 72           ; ld (hl), d           |
  10ea 23           ; inc hl               |
  10eb 73           ; ld (hl), e           |
  10ec 83           ; add a, e             |
  10ed ed 50        ; in d, (c)            |
  10ef 82           ; add a, d             |
  10f0 05           ; dec b                |
  10f1 20 f3        ; jr nz, 0x10e6        |
  10f3 d9           ; exx                  |
  10f4 ed 68        ; in l, (c)            |
  10f6 85           ; add a, l             |
  10f7 05           ; dec b                |
  10f8 20 fa        ; jr nz, 0x10f4        |
  10fa 95           ; sub l                |
  10fb bd           ; cp l                 |
  10fc db 09        ; in a, (0x9)          |
  10fe 20 dc        ; jr nz, 0x10dc        |
  1100 d9           ; exx                  |
  1101 23           ; inc hl               |
  1102 72           ; ld (hl), d           |
  1103 fe 10        ; cp 0x10              | is end of record?
  1105 20 d5        ; jr nz, 0x10dc        |
  1107 07           ; rlca                 |
  1108 32 9d 40     ; ld (0x409d), a       | set ERC   (disk error count) = a
  110b 2a a2 40     ; ld hl, (0x40a2)      | get hl = TRKS  (track # for drive 2)
  110e eb           ; ex de, hl            |
  110f 2a 20 42     ; ld hl, (0x4220)      |
  1112 19           ; add hl, de           |
  1113 22 a2 40     ; ld (0x40a2), hl      | set TRKS  (track # for drive 2) = hl
  1116 d9           ; exx                  |
  1117 dd 34 00     ; inc (ix + 0x0)       |
  111a 20 03        ; jr nz, 0x111f        |
  111c dd 34 01     ; inc (ix + 0x1)       |
  111f 3e 20        ; ld a, 0x20           |
  1121 32 9d 40     ; ld (0x409d), a       | set ERC   (disk error count) = a
  1124 97           ; sub a                |
  1125 21 9c 40     ; ld hl, 0x409c        |
  1128 1c           ; inc e                |
  1129 35           ; dec (hl)             |
  112a c2 a1 10     ; jp nz, 0x10a1        |
  112d 18 10        ; jr 0x113f            | jump to return of (unknown) disk function

  ;increment current record number (and return)
  112f dd 34 00     ; inc (ix + 0x0)       |
  1132 20 03        ; jr nz, 0x1137        |
  1134 dd 34 01     ; inc (ix + 0x1)       |
  1137 21 9c 40     ; ld hl, 0x409c        |
  113a 35           ; dec (hl)             |
  113b c2 2f 11     ; jp nz, 0x112f        |
  113e b7           ; or a                 |

  ;return from (unknown) disk function
  113f fb           ; ei                   |
  1140 dd e5        ; push ix              |
  1142 c1           ; pop bc               |
  1143 c9           ; ret                  |

  ;write??
  1144 cd de 12     ; call 0x12de          |
  1147 c0           ; ret nz               |
  1148 cd 44 13     ; call 0x1344          |
  114b cd c1 12     ; call 0x12c1          |
  114e dd 5e 0e     ; ld e, (ix + 0xe)     |
  1151 16 00        ; ld d, 0x0            |
  1153 dd 7e 10     ; ld a, (ix + 0x10)    |
  1156 dd 96 12     ; sub (ix + 0x12)      |
  1159 21 00 00     ; ld hl, 0x0           |
  115c 3d           ; dec a                |
  115d 19           ; add hl, de           |
  115e 3c           ; inc a                |
  115f 20 fc        ; jr nz, 0x115d        |
  1161 dd 75 0a     ; ld (ix + 0xa), l     |
  1164 dd 74 0b     ; ld (ix + 0xb), h     |
  1167 18 07        ; jr 0x1170            |
  1169 cd de 12     ; call 0x12de          |
  116c c0           ; ret nz               |
  116d cd c1 12     ; call 0x12c1          |
  1170 21 9d 40     ; ld hl, 0x409d        |
  1173 36 20        ; ld (hl), 0x20        |
  1175 dd 7e 13     ; ld a, (ix + 0x13)    |
  1178 b7           ; or a                 |
  1179 3e 07        ; ld a, 0x7            |
  117b fa 2f 11     ; jp m, 0x112f         |
  117e 21 29 42     ; ld hl, 0x4229        |
  1181 77           ; ld (hl), a           |
  1182 21 22 42     ; ld hl, 0x4222        |
  1185 36 00        ; ld (hl), 0x0         |
  1187 22 24 42     ; ld (0x4224), hl      |
  118a cd 25 13     ; call 0x1325          |
  118d 1e ff        ; ld e, 0xff           |
  118f cd 51 13     ; call 0x1351          |
  1192 28 57        ; jr z, 0x11eb         |
  1194 cd 75 14     ; call 0x1475          |
  1197 20 96        ; jr nz, 0x112f        |
  1199 db 09        ; in a, (0x9)          |
  119b 3e 80        ; ld a, 0x80           |
  119d d3 0b        ; out (0xb), a         |
  119f d9           ; exx                  |
  11a0 2a b6 40     ; ld hl, (0x40b6)      | get hl = PART1 (length to be transferred)
  11a3 db 09        ; in a, (0x9)          |
  11a5 eb           ; ex de, hl            |
  11a6 2a a2 40     ; ld hl, (0x40a2)      | get hl = TRKS  (track # for drive 2)
  11a9 db 09        ; in a, (0x9)          |
  11ab 1b           ; dec de               |
  11ac 7a           ; ld a, d              |
  11ad 13           ; inc de               |
  11ae 0f           ; rrca                 |
  11af db 09        ; in a, (0x9)          |
  11b1 3a b8 40     ; ld a, (0x40b8)       | get a = PART2 unused length
  11b4 57           ; ld d, a              |
  11b5 db 09        ; in a, (0x9)          |
  11b7 14           ; inc d                |
  11b8 01 09 00     ; ld bc, 0x9           |
  11bb db 09        ; in a, (0x9)          |
  11bd 3e 9b        ; ld a, 0x9b           |
  11bf d3 09        ; out (0x9), a         | write Data Record identifier 0x9b
  11c1 d2 b6 12     ; jp nc, 0x12b6        |
  11c4 86           ; add a, (hl)          |
  11c5 ed a3        ; outi                 | write (hl+i) to disk, i = 0 to b
  11c7 20 fb        ; jr nz, 0x11c4        |
  11c9 43           ; ld b, e              |
  11ca 86           ; add a, (hl)          |
  11cb ed a3        ; outi                 | write (hl+i) to disk, i = 0 to b
  11cd 20 fb        ; jr nz, 0x11ca        |
  11cf 15           ; dec d                |
  11d0 28 05        ; jr z, 0x11d7         |
  11d2 ed 41        ; out (c), b           | write checksum
  11d4 15           ; dec d                |
  11d5 20 fb        ; jr nz, 0x11d2        |
  11d7 d3 09        ; out (0x9), a         |
  11d9 2a 24 42     ; ld hl, (0x4224)      |
  11dc 16 10        ; ld d, 0x10           | write end of record terminator 0x10
  11de ed 51        ; out (c), d           |
  11e0 86           ; add a, (hl)          |
  11e1 77           ; ld (hl), a           |
  11e2 af           ; xor a                |
  11e3 d3 09        ; out (0x9), a         |
  11e5 00           ; nop                  |
  11e6 00           ; nop                  |
  11e7 d3 09        ; out (0x9), a         |
  11e9 d3 0b        ; out (0xb), a         |
  11eb 2a a2 40     ; ld hl, (0x40a2)      | get hl = TRKS  (track # for drive 2)
  11ee eb           ; ex de, hl            |
  11ef 2a 20 42     ; ld hl, (0x4220)      |
  11f2 19           ; add hl, de           |
  11f3 22 a2 40     ; ld (0x40a2), hl      | set TRKS  (track # for drive 2) = hl
  11f6 d9           ; exx                  |
  11f7 1c           ; inc e                |
  11f8 dd 34 00     ; inc (ix + 0x0)       |
  11fb 20 03        ; jr nz, 0x1200        |
  11fd dd 34 01     ; inc (ix + 0x1)       |
  1200 21 9b 40     ; ld hl, 0x409b        |
  1203 35           ; dec (hl)             |
  1204 20 89        ; jr nz, 0x118f        |
  1206 23           ; inc hl               |
  1207 7e           ; ld a, (hl)           |
  1208 ed 44        ; neg                  |
  120a dd 86 00     ; add a, (ix + 0x0)    |
  120d dd 77 00     ; ld (ix + 0x0), a     |
  1210 38 03        ; jr c, 0x1215         |
  1212 dd 35 01     ; dec (ix + 0x1)       |
  1215 1e ff        ; ld e, 0xff           |
  1217 3e 23        ; ld a, 0x23           |
  1219 32 24 42     ; ld (0x4224), a       |
  121c cd 51 13     ; call 0x1351          |
  121f ca 2f 11     ; jp z, 0x112f         |
  1222 cd 75 14     ; call 0x1475          |
  1225 c2 2f 11     ; jp nz, 0x112f        |
  1228 db 09        ; in a, (0x9)          |
  122a dd 6e 0c     ; ld l, (ix + 0xc)     |
  122d dd 66 0d     ; ld h, (ix + 0xd)     |
  1230 2c           ; inc l                |
  1231 25           ; dec h                |
  1232 28 03        ; jr z, 0x1237         |
  1234 2d           ; dec l                |
  1235 26 01        ; ld h, 0x1            |
  1237 01 09 00     ; ld bc, 0x9           |
  123a db 0a        ; in a, (0xa)          |
  123c db 0a        ; in a, (0xa)          |
  123e b7           ; or a                 |
  123f f2 3c 12     ; jp p, 0x123c         |
  1242 db 09        ; in a, (0x9)          |
  1244 80           ; add a, b             |
  1245 ed 40        ; in b, (c)            |
  1247 2d           ; dec l                |
  1248 20 fa        ; jr nz, 0x1244        |
  124a 80           ; add a, b             |
  124b ed 40        ; in b, (c)            |
  124d 25           ; dec h                |
  124e 20 fa        ; jr nz, 0x124a        |
  1250 b8           ; cp b                 |
  1251 db 09        ; in a, (0x9)          |
  1253 20 49        ; jr nz, 0x129e        |
  1255 fe 10        ; cp 0x10              |
  1257 20 45        ; jr nz, 0x129e        |
  1259 3a 22 42     ; ld a, (0x4222)       |
  125c 90           ; sub b                |
  125d 32 22 42     ; ld (0x4222), a       |
  1260 21 9d 40     ; ld hl, 0x409d        |
  1263 36 14        ; ld (hl), 0x14        |
  1265 2a 20 42     ; ld hl, (0x4220)      |
  1268 44           ; ld b, h              |
  1269 4d           ; ld c, l              |
  126a 2a 99 40     ; ld hl, (0x4099)      | get hl = THERE (addr for disk transfer)
  126d 09           ; add hl, bc           |
  126e 22 99 40     ; ld (0x4099), hl      | set THERE (addr for disk transfer) = hl
  1271 1c           ; inc e                |
  1272 dd 34 00     ; inc (ix + 0x0)       |
  1275 20 03        ; jr nz, 0x127a        |
  1277 dd 34 01     ; inc (ix + 0x1)       |
  127a 21 9c 40     ; ld hl, 0x409c        |
  127d 35           ; dec (hl)             |
  127e 20 9c        ; jr nz, 0x121c        |
  1280 3a 22 42     ; ld a, (0x4222)       |
  1283 b7           ; or a                 |
  1284 ca 3f 11     ; jp z, 0x113f         |

  ;unknown (disk?) function
  1285 3f           ; ccf                  |
  1286 11 21 29     ; ld de, 0x2921        |
  1289 42           ; ld b, d              |
  128a 35           ; dec (hl)             |
  128b 3e 03        ; ld a, 0x3            |
  128d 28 15        ; jr z, 0x12a4         |
  128f 2a 26 42     ; ld hl, (0x4226)      |
  1292 22 99 40     ; ld (0x4099), hl      | set THERE (addr for disk transfer) = hl
  1295 3a 28 42     ; ld a, (0x4228)       |
  1298 32 9c 40     ; ld (0x409c), a       | set SNRT  (# recs to be transfd) = a
  129b c3 82 11     ; jp 0x1182            |
  129e 3e 03        ; ld a, 0x3            |
  12a0 21 9d 40     ; ld hl, 0x409d        |
  12a3 35           ; dec (hl)             |
  12a4 ca 2f 11     ; jp z, 0x112f         |
  12a7 2a 99 40     ; ld hl, (0x4099)      | get hl = THERE (addr for disk transfer)
  12aa 22 a2 40     ; ld (0x40a2), hl      | set TRKS  (track # for drive 2) = hl
  12ad 3a 9c 40     ; ld a, (0x409c)       | get a = SNRT  (# recs to be transfd)
  12b0 32 9b 40     ; ld (0x409b), a       | set NRT   (disk record count) = a
  12b3 c3 8d 11     ; jp 0x118d            |
  12b6 86           ; add a, (hl)          |
  12b7 ed a3        ; outi                 |
  12b9 43           ; ld b, e              |
  12ba 05           ; dec b                |
  12bb 86           ; add a, (hl)          |
  12bc ed a3        ; outi                 |
  12be c3 ca 11     ; jp 0x11ca            |

  ;Set PART1 and PART2
  12c1 dd 4e 0c     ; ld c, (ix + 0xc)     | bc = record length
  12c4 dd 46 0d     ; ld b, (ix + 0xd)     |
  12c7 7b           ; ld a, e              |
  12c8 2f           ; cpl                  |
  12c9 6f           ; ld l, a              |
  12ca 7a           ; ld a, d              |
  12cb 2f           ; cpl                  |
  12cc 67           ; ld h, a              |
  12cd 09           ; add hl, bc           |
  12ce 23           ; inc hl               |
  12cf 38 05        ; jr c, 0x12d6         |
  12d1 50           ; ld d, b              |
  12d2 59           ; ld e, c              |
  12d3 21 00 00     ; ld hl, 0x0           |
  12d6 22 b8 40     ; ld (0x40b8), hl      | set PART2 unused length = hl
  12d9 eb           ; ex de, hl            |
  12da 22 b6 40     ; ld (0x40b6), hl      | set PART1 (length to be transferred) = hl
  12dd c9           ; ret                  |

  ;Select disk, wait for drive/data ready
  12de 22 99 40     ; ld (0x4099), hl      | set THERE (addr for disk transfer) = hl
  12e1 32 9c 40     ; ld (0x409c), a       | set SNRT  (# recs to be transfd) = a
  12e4 6b           ; ld l, e              |
  12e5 62           ; ld h, d              |
  12e6 22 20 42     ; ld (0x4220), hl      | Store INDEX (curr rec no on index)
  12e9 dd 6e 0f     ; ld l, (ix + 0xf)     | get l = disk# on INDEX
  12ec 3a a0 40     ; ld a, (0x40a0)       | get a = DISK  (selected disk drive #)
  12ef bd           ; cp l                 |
  12f0 28 27        ; jr z, 0x1319         |
  12f2 3e 80        ; ld a, 0x80           |
  12f4 65           ; ld h, l              |
  12f5 07           ; rlca                 |
  12f6 2d           ; dec l                |
  12f7 20 fc        ; jr nz, 0x12f5        |
  12f9 6c           ; ld l, h              |
  12fa 67           ; ld h, a              |
  12fb d3 0a        ; out (0xa), a         |
  12fd db 0a        ; in a, (0xa)          |
  12ff 0f           ; rrca                 |
  1300 38 e7        ; jr c, 0x12e9         |
  1302 7c           ; ld a, h              |
  1303 d3 0a        ; out (0xa), a         | select disk
  1305 7d           ; ld a, l              |
  1306 32 a0 40     ; ld (0x40a0), a       | set DISK  (selected disk drive #) = a
  1309 3e ff        ; ld a, 0xff           |
  130b 32 a1 40     ; ld (0x40a1), a       | set TRKS  (track # for drive 1) = a
  130e 2e 24        ; ld l, 0x24           | Skip 143 bytes (track 0)
  1310 cd 0e 14     ; call 0x140e          |
  1313 cd 0e 14     ; call 0x140e          | Skip 1023 bytes (track 0)
  1316 cd 0e 14     ; call 0x140e          | Skip 1023 bytes (track 0)
  1319 db 0a        ; in a, (0xa)          | get disk status
  131b e6 40        ; and 0x40             | check if disk is ready
  131d 28 02        ; jr z, 0x1321         | goto error return
  131f 97           ; sub a                |
  1320 c9           ; ret                  | return OK
  1321 3e 05        ; ld a, 0x5            |
  1323 b7           ; or a                 |
  1324 c9           ; ret                  | return error # 5 (inferred)

  ;Copy rec before last to ROS INDEX
  1325 dd 7e 16     ; ld a, (ix + 0x16)    | rec before last
  1328 dd 77 00     ; ld (ix + 0x0), a     |
  132b dd 7e 17     ; ld a, (ix + 0x17)    |
  132e dd 77 01     ; ld (ix + 0x1), a     | set current record number on INDEX
  1331 2a 99 40     ; ld hl, (0x4099)      | get hl = THERE (addr for disk transfer)
  1334 22 a2 40     ; ld (0x40a2), hl      | set TRKS  (track # for drive 2) = hl
  1337 22 26 42     ; ld (0x4226), hl      |
  133a 3a 9c 40     ; ld a, (0x409c)       | get a = SNRT  (# recs to be transfd)
  133d 32 9b 40     ; ld (0x409b), a       | set NRT   (disk record count) = a
  1340 32 28 42     ; ld (0x4228), a       |
  1343 c9           ; ret                  |

  ;Adjust last record number???
  1344 dd 7e 00     ; ld a, (ix + 0x0)     | copy record number (hi+lo) to last reordnumber on INDEX FD
  1347 dd 77 16     ; ld (ix + 0x16), a    |
  134a dd 7e 01     ; ld a, (ix + 0x1)     |
  134d dd 77 17     ; ld (ix + 0x17), a    |
  1350 c9           ; ret                  |

  ;Compare ROS INDEX with INDEX FD???
  1351 dd 7e 01     ; ld a, (ix + 0x1)     | get a = current record # on INDEX (LO)
  1354 dd be 0b     ; cp (ix + 0xb)        | compare with same (LO) on INDEX FD
  1357 c2 60 13     ; jp nz, 0x1360        |
  135a dd 7e 00     ; ld a, (ix + 0x0)     | compare with same (HI) on INDEX FD
  135d dd be 0a     ; cp (ix + 0xa)        |
  1360 d8           ; ret c                |
  1361 97           ; sub a                |
  1362 3e 06        ; ld a, 0x6            |
  1364 c9           ; ret                  |

  ;Search for valid ID Record
  1365 d5           ; push de              |
  1366 0e 0a        ; ld c, 0xa            |
  1368 21 10 27     ; ld hl, 0x2710        | test for disk ready h*l times (0x27 * 0x10)
  136b f3           ; di                   |
  136c ed 78        ; in a, (c)            |
  136e ed 78        ; in a, (c)            |
  1370 fa 82 13     ; jp m, 0x1382         |
  1373 2d           ; dec l                |
  1374 20 f8        ; jr nz, 0x136e        |
  1376 ed 78        ; in a, (c)            |
  1378 fa 82 13     ; jp m, 0x1382         |
  137b 25           ; dec h                |
  137c 20 f0        ; jr nz, 0x136e        |
  137e fb           ; ei                   |
  137f d1           ; pop de               |
  1380 3c           ; inc a                |
  1381 c9           ; ret                  | drive was not ready for a while
  1382 db 09        ; in a, (0x9)          | read byte (ID record)
  1384 fe 9e        ; cp 0x9e              | check if ID record (0x9e)
  1386 20 e4        ; jr nz, 0x136c        |
  1388 0d           ; dec c                |
  1389 ed 40        ; in b, (c)            | get b = Track
  138b ed 48        ; in c, (c)            | get c = Sector
  138d db 09        ; in a, (0x9)          | get a = check sum
  138f 90           ; sub b                |
  1390 91           ; sub c                |
  1391 20 d9        ; jr nz, 0x136c        | bad cksum, find next ID record
  1393 fb           ; ei                   | ID Record, read with good cksum
  1394 21 a1 40     ; ld hl, 0x40a1        |
  1397 70           ; ld (hl), b           | store track# for current record
  1398 d1           ; pop de               |
  1399 21 a1 40     ; ld hl, 0x40a1        | Track # for drive 1
  139c 7e           ; ld a, (hl)           |
  139d 72           ; ld (hl), d           |
  139e fe fe        ; cp 0xfe              | check for ?? end of tracks or not index track
  13a0 d0           ; ret nc               |
  13a1 47           ; ld b, a              |
  13a2 21 00 4d     ; ld hl, 0x4d00        |
  13a5 bc           ; cp h                 |
  13a6 38 06        ; jr c, 0x13ae         |
  13a8 ed 44        ; neg                  |
  13aa c6 99        ; add a, 0x99          |
  13ac 47           ; ld b, a              |
  13ad 2c           ; inc l                |
  13ae 7a           ; ld a, d              |
  13af bc           ; cp h                 |
  13b0 38 07        ; jr c, 0x13b9         |
  13b2 ed 44        ; neg                  |
  13b4 c6 99        ; add a, 0x99          |
  13b6 57           ; ld d, a              |
  13b7 cb fd        ; set 0x7, l           |
  13b9 7d           ; ld a, l              |
  13ba b7           ; or a                 |
  13bb 28 18        ; jr z, 0x13d5         |
  13bd fe 81        ; cp 0x81              |
  13bf 28 14        ; jr z, 0x13d5         |
  13c1 3a a0 40     ; ld a, (0x40a0)       | get a = DISK  (selected disk drive #)
  13c4 67           ; ld h, a              |
  13c5 3e 80        ; ld a, 0x80           |
  13c7 07           ; rlca                 |
  13c8 25           ; dec h                |
  13c9 20 fc        ; jr nz, 0x13c7        |
  13cb cb 85        ; res 0x0, l           |
  13cd b5           ; or l                 |
  13ce d3 0a        ; out (0xa), a         | select drive (and side)
  13d0 2e 05        ; ld l, 0x5            |
  13d2 cd 0e 14     ; call 0x140e          | skip 23 bytes
  13d5 78           ; ld a, b              |
  13d6 92           ; sub d                |
  13d7 47           ; ld b, a              |
  13d8 c8           ; ret z                |
  13d9 0e 00        ; ld c, 0x0            |
  13db 30 05        ; jr nc, 0x13e2        |
  13dd 0e 40        ; ld c, 0x40           | step direction UP
  13df ed 44        ; neg                  |
  13e1 47           ; ld b, a              |
  13e2 79           ; ld a, c              |
  13e3 b7           ; or a                 |
  13e4 20 06        ; jr nz, 0x13ec        |
  13e6 db 0a        ; in a, (0xa)          |
  13e8 e6 10        ; and 0x10             | check if at Track 0
  13ea 20 1d        ; jr nz, 0x1409        |
  13ec 3e 20        ; ld a, 0x20           | Track step bit
  13ee b1           ; or c                 |
  13ef d3 0b        ; out (0xb), a         |
  13f1 79           ; ld a, c              |
  13f2 d3 0b        ; out (0xb), a         |
  13f4 2e 30        ; ld l, 0x30           | Skip 191 bytes
  13f6 cd 0e 14     ; call 0x140e          |
  13f9 db 0a        ; in a, (0xa)          |
  13fb e6 02        ; and 0x2              | Double density?
  13fd 20 05        ; jr nz, 0x1404        |
  13ff 2e 4d        ; ld l, 0x4d           | Skip 307 bytes
  1401 cd 0e 14     ; call 0x140e          |
  1404 05           ; dec b                |
  1405 20 db        ; jr nz, 0x13e2        |
  1407 04           ; inc b                |
  1408 c9           ; ret                  |
  1409 01 40 03     ; ld bc, 0x340         |
  140c 18 de        ; jr 0x13ec            | step to next track

  ;skip 4*l + 3 bytes
  140e db 09        ; in a, (0x9)          | read byte from disk
  1410 00           ; nop                  |
  1411 db 09        ; in a, (0x9)          | read byte from disk
  1413 2d           ; dec l                |
  1414 db 09        ; in a, (0x9)          | read byte from disk
  1416 c8           ; ret z                |
  1417 db 09        ; in a, (0x9)          | read byte from disk
  1419 18 f3        ; jr 0x140e            |

  ;UNEXPLORED
  141b 21 9d 40     ; ld hl, 0x409d        |
  141e 36 0a        ; ld (hl), 0xa         | set ERC to 10
  1420 fb           ; ei                   |
  1421 dd 5e 00     ; ld e, (ix + 0x0)     | record number (HI) from INDEX FD
  1424 dd 56 01     ; ld d, (ix + 0x1)     | record number (LO) from INDEX FD
  1427 dd 7e 0e     ; ld a, (ix + 0xe)     |
  142a dd 46 10     ; ld b, (ix + 0x10)    | first track (HI) ?
  142d 05           ; dec b                |
  142e 2f           ; cpl                  |
  142f 3c           ; inc a                |
  1430 6f           ; ld l, a              |
  1431 26 ff        ; ld h, 0xff           |
  1433 eb           ; ex de, hl            |
  1434 78           ; ld a, b              |
  1435 19           ; add hl, de           |
  1436 3c           ; inc a                |
  1437 38 fc        ; jr c, 0x1435         |
  1439 57           ; ld d, a              |
  143a 7d           ; ld a, l              |
  143b 93           ; sub e                |
  143c 5f           ; ld e, a              |
  143d cd 65 13     ; call 0x1365          |
  1440 21 a1 40     ; ld hl, 0x40a1        |
  1443 56           ; ld d, (hl)           |
  1444 28 2f        ; jr z, 0x1475         |
  1446 2e 46        ; ld l, 0x46           | Skip 279 bytes
  1448 cd 0e 14     ; call 0x140e          |
  144b 21 00 80     ; ld hl, 0x8000        |
  144e 0e 0a        ; ld c, 0xa            |
  1450 2d           ; dec l                |
  1451 28 0b        ; jr z, 0x145e         |
  1453 ed 40        ; in b, (c)            |
  1455 f2 50 14     ; jp p, 0x1450         |
  1458 db 09        ; in a, (0x9)          |
  145a d6 9b        ; sub 0x9b             | Data Record (0x9b)
  145c 28 17        ; jr z, 0x1475         |
  145e 25           ; dec h                |
  145f 20 ef        ; jr nz, 0x1450        |
  1461 21 9d 40     ; ld hl, 0x409d        | No Data Record found after 128 reads
  1464 35           ; dec (hl)             |
  1465 01 00 01     ; ld bc, 0x100         |
  1468 28 3a        ; jr z, 0x14a4         |
  146a db 0a        ; in a, (0xa)          | get disk status
  146c e6 10        ; and 0x10             | track 0 selected
  146e 20 34        ; jr nz, 0x14a4        |
  1470 cd e2 13     ; call 0x13e2          |
  1473 18 d1        ; jr 0x1446            |

  ;UNEXPLORED
  1475 7b           ; ld a, e              |
  1476 dd 6e 0e     ; ld l, (ix + 0xe)     | Track/Record
  1479 bd           ; cp l                 |
  147a 30 a4        ; jr nc, 0x1420        |

  ;search for INDEX file?
  147c 21 00 08     ; ld hl, 0x800         |
  147f 0e 0a        ; ld c, 0xa            |
  1481 f3           ; di                   |
  1482 db 0a        ; in a, (0xa)          | get disk status
  1484 ed 78        ; in a, (c)            |
  1486 f2 84 14     ; jp p, 0x1484         |
  1489 db 09        ; in a, (0x9)          | read byte (ID record) from disk
  148b fe 9e        ; cp 0x9e              | check if ID record (0x9e)
  148d 20 0f        ; jr nz, 0x149e        |
  148f db 09        ; in a, (0x9)          | read byte (TRACK#)    from disk
  1491 ba           ; cp d                 |
  1492 20 14        ; jr nz, 0x14a8        |
  1494 db 09        ; in a, (0x9)          | read byte (SECTOR#)   from disk
  1496 bb           ; cp e                 |
  1497 20 05        ; jr nz, 0x149e        |
  1499 db 09        ; in a, (0x9)          | read byte (CHECK SUM) from disk
  149b 93           ; sub e                |
  149c 92           ; sub d                |
  149d c8           ; ret z                | return if checksum good
  149e fb           ; ei                   |
  149f 2b           ; dec hl               |
  14a0 7d           ; ld a, l              |
  14a1 b4           ; or h                 |
  14a2 20 dd        ; jr nz, 0x1481        |
  14a4 3e 01        ; ld a, 0x1            | return error code 1?
  14a6 b7           ; or a                 |
  14a7 c9           ; ret                  |

  ;UNEXPLORED
  14a8 4f           ; ld c, a              |
  14a9 db 09        ; in a, (0x9)          | read byte from disk
  14ab 47           ; ld b, a              |
  14ac db 09        ; in a, (0x9)          | read byte from disk
  14ae 91           ; sub c                |
  14af 90           ; sub b                |
  14b0 41           ; ld b, c              |
  14b1 0e 0a        ; ld c, 0xa            |
  14b3 20 cc        ; jr nz, 0x1481        | checksum good if a = 0
  14b5 db 09        ; in a, (0x9)          |
  14b7 fe 10        ; cp 0x10              | end of record marker
  14b9 20 c6        ; jr nz, 0x1481        |
  14bb 78           ; ld a, b              |
  14bc 32 a1 40     ; ld (0x40a1), a       | set TRKS  (track # for drive 1) = a
  14bf 21 9d 40     ; ld hl, 0x409d        |
  14c2 35           ; dec (hl)             |
  14c3 28 df        ; jr z, 0x14a4         |
  14c5 c3 20 14     ; jp 0x1420            |
  14c8 01 0a 00     ; ld bc, 0xa           |
  14cb 54           ; ld d, h              |
  14cc 5d           ; ld e, l              |
  14cd 09           ; add hl, bc           |
  14ce eb           ; ex de, hl            |
  14cf 7e           ; ld a, (hl)           |
  14d0 36 00        ; ld (hl), 0x0         |
  14d2 12           ; ld (de), a           |
  14d3 23           ; inc hl               |
  14d4 13           ; inc de               |
  14d5 7e           ; ld a, (hl)           |
  14d6 36 00        ; ld (hl), 0x0         |
  14d8 12           ; ld (de), a           |
  14d9 13           ; inc de               |
  14da 13           ; inc de               |
  14db 13           ; inc de               |
  14dc 13           ; inc de               |
  14dd 1a           ; ld a, (de)           |
  14de 32 ad 40     ; ld (0x40ad), a       | set Disk # = a
  14e1 fe 07        ; cp 0x7               |
  14e3 fa f0 14     ; jp m, 0x14f0         |
  14e6 28 04        ; jr z, 0x14ec         |
  14e8 fe 08        ; cp 0x8               |
  14ea 20 04        ; jr nz, 0x14f0        |
  14ec 3e 7a        ; ld a, 0x7a           |
  14ee 18 02        ; jr 0x14f2            |
  14f0 3e 82        ; ld a, 0x82           |
  14f2 32 ac 40     ; ld (0x40ac), a       | set Records/Track = a
  14f5 97           ; sub a                |
  14f6 12           ; ld (de), a           |
  14f7 11 02 00     ; ld de, 0x2           |
  14fa 01 9e 40     ; ld bc, 0x409e        |
  14fd 02           ; ld (bc), a           |
  14fe 03           ; inc bc               |
  14ff 02           ; ld (bc), a           |
  1500 0b           ; dec bc               |
  1501 3e 08        ; ld a, 0x8            |
  1503 e5           ; push hl              |
  1504 23           ; inc hl               |
  1505 cd 09 10     ; call 0x1009          |
  1508 e1           ; pop hl               |
  1509 20 09        ; jr nz, 0x1514        |
  150b 2b           ; dec hl               |
  150c 3e 01        ; ld a, 0x1            |
  150e 11 14 00     ; ld de, 0x14          |
  1511 cc 03 10     ; call z, 0x1003       |
  1514 01 03 16     ; ld bc, 0x1603        |
  1517 c9           ; ret                  |
  1518 21 d0 40     ; ld hl, 0x40d0        |
  151b cd 30 10     ; call 0x1030          |
  151e c0           ; ret nz               |
  151f 06 03        ; ld b, 0x3            |
  1521 3a da 40     ; ld a, (0x40da)       | get a = Number of Records (LFILE)
  1524 4f           ; ld c, a              |
  1525 78           ; ld a, b              |
  1526 b9           ; cp c                 |
  1527 30 37        ; jr nc, 0x1560        |
  1529 21 d0 40     ; ld hl, 0x40d0        |
  152c 70           ; ld (hl), b           |
  152d 04           ; inc b                |
  152e 04           ; inc b                |
  152f 04           ; inc b                |
  1530 04           ; inc b                |
  1531 11 ff 00     ; ld de, 0xff          |
  1534 c5           ; push bc              |
  1535 01 d0 40     ; ld bc, 0x40d0        |
  1538 21 00 42     ; ld hl, 0x4200        |
  153b 3e 01        ; ld a, 0x1            |
  153d cd 00 10     ; call 0x1000          |
  1540 e1           ; pop hl               |
  1541 c0           ; ret nz               |
  1542 e5           ; push hl              |
  1543 21 ff 42     ; ld hl, 0x42ff        |
  1546 36 00        ; ld (hl), 0x0         |
  1548 2c           ; inc l                |
  1549 c1           ; pop bc               |
  154a 7e           ; ld a, (hl)           |
  154b b7           ; or a                 |
  154c 28 d3        ; jr z, 0x1521         |
  154e c5           ; push bc              |
  154f 23           ; inc hl               |
  1550 5e           ; ld e, (hl)           |
  1551 23           ; inc hl               |
  1552 56           ; ld d, (hl)           |
  1553 23           ; inc hl               |
  1554 4e           ; ld c, (hl)           |
  1555 0c           ; inc c                |
  1556 0d           ; dec c                |
  1557 23           ; inc hl               |
  1558 28 ef        ; jr z, 0x1549         |
  155a 06 00        ; ld b, 0x0            |
  155c ed b0        ; ldir                 |
  155e 18 e9        ; jr 0x1549            |
  1560 3e 03        ; ld a, 0x3            |
  1562 a0           ; and b                |
  1563 3d           ; dec a                |
  1564 fe ff        ; cp 0xff              |
  1566 c8           ; ret z                |
  1567 47           ; ld b, a              |
  1568 18 b7        ; jr 0x1521            |

  ;unknown IWS function i
  156a 97           ; sub a                |
  156b d3 0b        ; out (0xb), a         |
  156d 32 a0 40     ; ld (0x40a0), a       | set DISK  (selected disk drive #) = a
  1570 3e 00        ; ld a, 0x0            |
  1572 d3 0a        ; out (0xa), a         |
  1574 21 a8 40     ; ld hl, 0x40a8        |
  1577 3e 82        ; ld a, 0x82           |
  1579 77           ; ld (hl), a           |
  157a 23           ; inc hl               |
  157b 23           ; inc hl               |
  157c 36 28        ; ld (hl), 0x28        |
  157e 23           ; inc hl               |
  157f 23           ; inc hl               |
  1580 77           ; ld (hl), a           |
  1581 cd 94 15     ; call 0x1594          |
  1584 ca 37 14     ; jp z, 0x1437         |
  1587 cd 9c 15     ; call 0x159c          |
  158a ca 15 10     ; jp z, 0x1015         |
  158d c9           ; ret                  |

  ;UNEXPLORED
  158e 4d           ; ld c, l              |
  158f 55           ; ld d, l              |
  1590 58           ; ld e, b              |
  1591 49           ; ld c, c              |
  1592 57           ; ld d, a              |
  1593 53           ; ld d, e              |

  ;unknown IWS function ii
  1594 21 8e 15     ; ld hl, 0x158e        |
  1597 11 fa 17     ; ld de, 0x17fa        |
  159a 18 06        ; jr 0x15a2            |
  159c 21 91 15     ; ld hl, 0x1591        |
  159f 11 31 14     ; ld de, 0x1431        |
  15a2 06 03        ; ld b, 0x3            |
  15a4 1a           ; ld a, (de)           |
  15a5 be           ; cp (hl)              |
  15a6 c0           ; ret nz               |
  15a7 23           ; inc hl               |
  15a8 13           ; inc de               |
  15a9 10 f9        ; djnz 0x15a4          |
  15ab c9           ; ret                  |

  ;unknown IWS functions
  15ac c5           ; push bc              |
  15ad f5           ; push af              |
  15ae cd 6a 15     ; call 0x156a          |
  15b1 21 10 16     ; ld hl, 0x1610        |
  15b4 0e 01        ; ld c, 0x1            |
  15b6 cd 27 00     ; call 0x27            |
  15b9 f1           ; pop af               |
  15ba fe 04        ; cp 0x4               |
  15bc 28 39        ; jr z, 0x15f7         |
  15be fe 09        ; cp 0x9               |
  15c0 fa c5 15     ; jp m, 0x15c5         |
  15c3 3e 09        ; ld a, 0x9            |
  15c5 21 11 16     ; ld hl, 0x1611        | error text "FORMAT ERR"
  15c8 4e           ; ld c, (hl)           |
  15c9 cb 79        ; bit 0x7, c           |
  15cb 23           ; inc hl               |
  15cc 28 fa        ; jr z, 0x15c8         |
  15ce 3d           ; dec a                |
  15cf 20 f7        ; jr nz, 0x15c8        |
  15d1 cb b9        ; res 0x7, c           |
  15d3 cd 27 00     ; call 0x27            | call DISPLAY
  15d6 0e 04        ; ld c, 0x4            |
  15d8 21 0c 16     ; ld hl, 0x160c        | error text "ON"
  15db cd 27 00     ; call 0x27            | call DISPLAY
  15de 0e 08        ; ld c, 0x8            |
  15e0 e1           ; pop hl               |
  15e1 23           ; inc hl               |
  15e2 23           ; inc hl               |
  15e3 cd 27 00     ; call 0x27            | call DISPLAY
  15e6 cd 94 15     ; call 0x1594          |
  15e9 ca 37 14     ; jp z, 0x1437         |
  15ec cd 30 00     ; call 0x30            | call STOP
  15ef 0e 01        ; ld c, 0x1            |
  15f1 21 10 16     ; ld hl, 0x1610        |
  15f4 c3 27 00     ; jp 0x27              |
  15f7 2a 99 40     ; ld hl, (0x4099)      | get hl = THERE (addr for disk transfer)
  15fa 3a 9c 40     ; ld a, (0x409c)       | get a = SNRT  (# recs to be transfd)
  15fd 4f           ; ld c, a              |
  15fe cd 27 00     ; call 0x27            | call DISPLAY
  1601 3e 04        ; ld a, 0x4            |
  1603 18 c0        ; jr 0x15c5            |

  ;ASCI CHARS ERROR MESSAGES
  1605 49           ; ld c, c              |
  1606 4e           ; ld c, (hl)           |
  1607 44           ; ld b, h              |
  1608 45           ; ld b, l              |
  1609 58           ; ld e, b              |
  160a 20 20        ; jr nz, 0x162c        |
  160c 20 4f        ; jr nz, 0x165d        |
  160e 4e           ; ld c, (hl)           |
  160f 20 0d        ; jr nz, 0x161e        |
  1611 8a           ; adc a, d             |
  1612 46           ; ld b, (hl)           |
  1613 4f           ; ld c, a              |
  1614 52           ; ld d, d              |
  1615 4d           ; ld c, l              |
  1616 41           ; ld b, c              |
  1617 54           ; ld d, h              |
  1618 20 45        ; jr nz, 0x165f        |
  161a 52           ; ld d, d              |
  161b 52           ; ld d, d              |
  161c 02           ; ld (bc), a           |
  161d 89           ; adc a, c             |
  161e 57           ; ld d, a              |
  161f 52           ; ld d, d              |
  1620 49           ; ld c, c              |
  1621 54           ; ld d, h              |
  1622 45           ; ld b, l              |
  1623 20 45        ; jr nz, 0x166a        |
  1625 52           ; ld d, d              |
  1626 52           ; ld d, d              |
  1627 8a           ; adc a, d             |
  1628 20 4e        ; jr nz, 0x1678        |
  162a 4f           ; ld c, a              |
  162b 54           ; ld d, h              |
  162c 20 46        ; jr nz, 0x1674        |
  162e 4f           ; ld c, a              |
  162f 55           ; ld d, l              |
  1630 4e           ; ld c, (hl)           |
  1631 44           ; ld b, h              |
  1632 87           ; add a, a             |
  1633 4e           ; ld c, (hl)           |
  1634 4f           ; ld c, a              |
  1635 20 44        ; jr nz, 0x167b        |
  1637 49           ; ld c, c              |
  1638 53           ; ld d, e              |
  1639 4b           ; ld c, e              |
  163a 8a           ; adc a, d             |
  163b 50           ; ld d, b              |
  163c 41           ; ld b, c              |
  163d 53           ; ld d, e              |
  163e 53           ; ld d, e              |
  163f 45           ; ld b, l              |
  1640 44           ; ld b, h              |
  1641 20 45        ; jr nz, 0x1688        |
  1643 4f           ; ld c, a              |
  1644 46           ; ld b, (hl)           |
  1645 8d           ; adc a, l             |
  1646 57           ; ld d, a              |
  1647 52           ; ld d, d              |
  1648 49           ; ld c, c              |
  1649 54           ; ld d, h              |
  164a 45           ; ld b, l              |
  164b 20 50        ; jr nz, 0x169d        |
  164d 52           ; ld d, d              |
  164e 4f           ; ld c, a              |
  164f 54           ; ld d, h              |
  1650 45           ; ld b, l              |
  1651 43           ; ld b, e              |
  1652 54           ; ld d, h              |
  1653 8d           ; adc a, l             |
  1654 44           ; ld b, h              |
  1655 41           ; ld b, c              |
  1656 54           ; ld d, h              |
  1657 41           ; ld b, c              |
  1658 20 4c        ; jr nz, 0x16a6        |
  165a 49           ; ld c, c              |
  165b 4e           ; ld c, (hl)           |
  165c 4b           ; ld c, e              |
  165d 20 45        ; jr nz, 0x16a4        |
  165f 52           ; ld d, d              |
  1660 52           ; ld d, d              |
  1661 89           ; adc a, c             |
  1662 57           ; ld d, a              |
  1663 45           ; ld b, l              |
  1664 49           ; ld c, c              |
  1665 52           ; ld d, d              |
  1666 44           ; ld b, h              |
  1667 20 45        ; jr nz, 0x16ae        |
  1669 52           ; ld d, d              |
  166a 52           ; ld d, d              |

  ;KEY ()?
  166b e5           ; push hl              |
  166c d5           ; push de              |
  166d cd de 12     ; call 0x12de          |
  1670 d1           ; pop de               |
  1671 e1           ; pop hl               |
  1672 c0           ; ret nz               |
  1673 22 4a 42     ; ld (0x424a), hl      |
  1676 dd 7e 0a     ; ld a, (ix + 0xa)     | get a = # of records HI
  1679 dd b6 0b     ; or (ix + 0xb)        | get a = # of records LO
  167c ca b1 17     ; jp z, 0x17b1         |
  167f 3a 9c 40     ; ld a, (0x409c)       | get a = SNRT  (# recs to be transfd)
  1682 b7           ; or a                 |
  1683 28 f7        ; jr z, 0x167c         |
  1685 4f           ; ld c, a              |
  1686 06 00        ; ld b, 0x0            |
  1688 09           ; add hl, bc           | checksum on FILE FD?
  1689 22 20 42     ; ld (0x4220), hl      |
  168c 47           ; ld b, a              |
  168d 3e 9b        ; ld a, 0x9b           |
  168f 2b           ; dec hl               |
  1690 86           ; add a, (hl)          | checksum on filename (increment)
  1691 10 fc        ; djnz 0x168f          |
  1693 08           ; ex af, af'           |
  1694 c5           ; push bc              |
  1695 e1           ; pop hl               |
  1696 19           ; add hl, de           |
  1697 dd 7e 0c     ; ld a, (ix + 0xc)     | record len on INDEX FD (HI)
  169a 95           ; sub l                |
  169b 6f           ; ld l, a              |
  169c dd 7e 0d     ; ld a, (ix + 0xd)     | record len on INDEX FD (LO)
  169f 9c           ; sbc a, h             |
  16a0 da b1 17     ; jp c, 0x17b1         |
  16a3 08           ; ex af, af'           |
  16a4 67           ; ld h, a              |
  16a5 22 50 42     ; ld (0x4250), hl      |
  16a8 08           ; ex af, af'           |
  16a9 67           ; ld h, a              |
  16aa b5           ; or l                 |
  16ab 2b           ; dec hl               |
  16ac 7c           ; ld a, h              |
  16ad 21 74 17     ; ld hl, 0x1774        |
  16b0 28 09        ; jr z, 0x16bb         |
  16b2 b7           ; or a                 |
  16b3 21 6e 17     ; ld hl, 0x176e        |
  16b6 28 03        ; jr z, 0x16bb         |
  16b8 21 69 17     ; ld hl, 0x1769        |
  16bb e5           ; push hl              |
  16bc fd e1        ; pop iy               |
  16be 63           ; ld h, e              |
  16bf 2e 0a        ; ld l, 0xa            |
  16c1 22 52 42     ; ld (0x4252), hl      |
  16c4 61           ; ld h, c              |
  16c5 2d           ; dec l                |
  16c6 22 4c 42     ; ld (0x424c), hl      |
  16c9 7a           ; ld a, d              |
  16ca b3           ; or e                 |
  16cb 21 4c 17     ; ld hl, 0x174c        |
  16ce 28 0b        ; jr z, 0x16db         |
  16d0 1b           ; dec de               |
  16d1 7a           ; ld a, d              |
  16d2 b7           ; or a                 |
  16d3 21 46 17     ; ld hl, 0x1746        |
  16d6 28 03        ; jr z, 0x16db         |
  16d8 21 41 17     ; ld hl, 0x1741        |
  16db 22 4e 42     ; ld (0x424e), hl      |
  16de 21 5f 17     ; ld hl, 0x175f        |
  16e1 22 54 42     ; ld (0x4254), hl      |
  16e4 cd c3 17     ; call 0x17c3          |
  16e7 dd 6e 00     ; ld l, (ix + 0x0)     | hl = current record number
  16ea dd 66 01     ; ld h, (ix + 0x1)     |
  16ed 22 48 42     ; ld (0x4248), hl      |
  16f0 1e ff        ; ld e, 0xff           |
  16f2 3e 24        ; ld a, 0x24           |
  16f4 32 9d 40     ; ld (0x409d), a       | set ERC   (disk error count) = a
  16f7 cd 75 14     ; call 0x1475          |
  16fa 20 2e        ; jr nz, 0x172a        |
  16fc d5           ; push de              |
  16fd 21 00 00     ; ld hl, 0x0           |
  1700 54           ; ld d, h              |
  1701 39           ; add hl, sp           |
  1702 22 a2 40     ; ld (0x40a2), hl      | set TRKS  (track # for drive 2) = hl
  1705 21 4a 42     ; ld hl, 0x424a        |
  1708 f9           ; ld sp, hl            |
  1709 e1           ; pop hl               |
  170a c1           ; pop bc               |
  170b d9           ; exx                  |
  170c e1           ; pop hl               |
  170d d1           ; pop de               |
  170e 7a           ; ld a, d              |
  170f 08           ; ex af, af'           |
  1710 c1           ; pop bc               |
  1711 ed 78        ; in a, (c)            |
  1713 ed 78        ; in a, (c)            |
  1715 f2 13 17     ; jp p, 0x1713         |
  1718 0d           ; dec c                |
  1719 ed 78        ; in a, (c)            |
  171b fe 9b        ; cp 0x9b              |
  171d 20 02        ; jr nz, 0x1721        |
  171f 08           ; ex af, af'           |
  1720 e9           ; jp (hl)              |
  1721 2a a2 40     ; ld hl, (0x40a2)      | get hl = TRKS  (track # for drive 2)
  1724 f9           ; ld sp, hl            |
  1725 3e 02        ; ld a, 0x2            |
  1727 d1           ; pop de               |
  1728 18 04        ; jr 0x172e            |
  172a 1e ff        ; ld e, 0xff           |
  172c 3e 01        ; ld a, 0x1            |
  172e 21 9d 40     ; ld hl, 0x409d        | hl = addr of ERC (disk error count)
  1731 35           ; dec (hl)             |
  1732 20 c3        ; jr nz, 0x16f7        |
  1734 2a 48 42     ; ld hl, (0x4248)      |
  1737 dd 75 00     ; ld (ix + 0x0), l     |
  173a dd 74 01     ; ld (ix + 0x1), h     |
  173d b7           ; or a                 |
  173e c3 3f 11     ; jp 0x113f            |
  1741 ed 50        ; in d, (c)            |
  1743 82           ; add a, d             |
  1744 10 fb        ; djnz 0x1741          |
  1746 ed 50        ; in d, (c)            |
  1748 82           ; add a, d             |
  1749 10 fb        ; djnz 0x1746          |
  174b 57           ; ld d, a              |
  174c 43           ; ld b, e              |
  174d d9           ; exx                  |
  174e db 09        ; in a, (0x9)          |
  1750 96           ; sub (hl)             |
  1751 c0           ; ret nz               |
  1752 23           ; inc hl               |
  1753 10 f9        ; djnz 0x174e          |
  1755 d9           ; exx                  | filename match on record
  1756 db 09        ; in a, (0x9)          |
  1758 fd e9        ; jp (iy)              |
  175a ed 50        ; in d, (c)            |
  175c 23           ; inc hl               |
  175d 96           ; sub (hl)             |
  175e 82           ; add a, d             |
  175f 10 f9        ; djnz 0x175a          |
  1761 47           ; ld b, a              |
  1762 db 09        ; in a, (0x9)          |
  1764 d9           ; exx                  |
  1765 fd e9        ; jp (iy)              |
  1767 ed 50        ; in d, (c)            |
  1769 82           ; add a, d             |
  176a 10 fb        ; djnz 0x1767          |
  176c ed 50        ; in d, (c)            |
  176e 82           ; add a, d             |
  176f 10 fb        ; djnz 0x176c          |
  1771 57           ; ld d, a              |
  1772 db 09        ; in a, (0x9)          |
  1774 92           ; sub d                |
  1775 d9           ; exx                  |
  1776 90           ; sub b                |
  1777 20 a8        ; jr nz, 0x1721        |
  1779 db 09        ; in a, (0x9)          | checksum good on data record
  177b fe 10        ; cp 0x10              | end-of-record marker
  177d 20 a2        ; jr nz, 0x1721        |
  177f eb           ; ex de, hl            |
  1780 2a 20 42     ; ld hl, (0x4220)      |
  1783 ed 52        ; sbc hl, de           |
  1785 2a a2 40     ; ld hl, (0x40a2)      | get hl = TRKS  (track # for drive 2)
  1788 f9           ; ld sp, hl            |
  1789 d1           ; pop de               |
  178a c2 90 17     ; jp nz, 0x1790        |
  178d 97           ; sub a                |
  178e 18 30        ; jr 0x17c0            |
  1790 1c           ; inc e                |
  1791 dd 34 00     ; inc (ix + 0x0)       |
  1794 c2 9a 17     ; jp nz, 0x179a        |
  1797 dd 34 01     ; inc (ix + 0x1)       |
  179a cd 51 13     ; call 0x1351          |
  179d cc c7 17     ; call z, 0x17c7       |
  17a0 2a 48 42     ; ld hl, (0x4248)      |
  17a3 7d           ; ld a, l              |
  17a4 dd be 00     ; cp (ix + 0x0)        |
  17a7 c2 f2 16     ; jp nz, 0x16f2        |
  17aa 7c           ; ld a, h              |
  17ab dd 96 01     ; sub (ix + 0x1)       |
  17ae c2 f2 16     ; jp nz, 0x16f2        |
  17b1 dd 7e 0a     ; ld a, (ix + 0xa)     |
  17b4 dd 77 00     ; ld (ix + 0x0), a     |
  17b7 dd 7e 0b     ; ld a, (ix + 0xb)     |
  17ba dd 77 01     ; ld (ix + 0x1), a     |
  17bd 3e 04        ; ld a, 0x4            |
  17bf b7           ; or a                 |
  17c0 c3 3f 11     ; jp 0x113f            |
  17c3 cd 51 13     ; call 0x1351          |
  17c6 c0           ; ret nz               |
  17c7 97           ; sub a                |
  17c8 dd 77 00     ; ld (ix + 0x0), a     |
  17cb dd 77 01     ; ld (ix + 0x1), a     |
  17ce 1e ff        ; ld e, 0xff           |
  17d0 c9           ; ret                  |
  17d1 ff           ; rst 0x38             |
  17d2 ff           ; rst 0x38             |
  17d3 ff           ; rst 0x38             |
  17d4 ff           ; rst 0x38             |
  17d5 ff           ; rst 0x38             |
  17d6 ff           ; rst 0x38             |
  17d7 ff           ; rst 0x38             |
  17d8 ff           ; rst 0x38             |
  17d9 ff           ; rst 0x38             |
  17da ff           ; rst 0x38             |
  17db ff           ; rst 0x38             |
  17dc ff           ; rst 0x38             |
  17dd ff           ; rst 0x38             |
  17de ff           ; rst 0x38             |
  17df ff           ; rst 0x38             |
  17e0 ff           ; rst 0x38             |
  17e1 ff           ; rst 0x38             |
  17e2 ff           ; rst 0x38             |
  17e3 ff           ; rst 0x38             |
  17e4 ff           ; rst 0x38             |
  17e5 ff           ; rst 0x38             |
  17e6 ff           ; rst 0x38             |
  17e7 ff           ; rst 0x38             |
  17e8 ff           ; rst 0x38             |
  17e9 ff           ; rst 0x38             |
  17ea ff           ; rst 0x38             |
  17eb ff           ; rst 0x38             |
  17ec ff           ; rst 0x38             |
  17ed ff           ; rst 0x38             |
  17ee ff           ; rst 0x38             |
  17ef ff           ; rst 0x38             |
  17f0 ff           ; rst 0x38             |
  17f1 ff           ; rst 0x38             |
  17f2 ff           ; rst 0x38             |
  17f3 ff           ; rst 0x38             |
  17f4 ff           ; rst 0x38             |
  17f5 ff           ; rst 0x38             |
  17f6 ff           ; rst 0x38             |
  17f7 ff           ; rst 0x38             |
  17f8 ff           ; rst 0x38             |
  17f9 ff           ; rst 0x38             |
  17fa ff           ; rst 0x38             |
  17fb ff           ; rst 0x38             |
  17fc ff           ; rst 0x38             |
  17fd ff           ; rst 0x38             |
  17fe ff           ; rst 0x38             |
  17ff ff           ; rst 0x38             |

  ;PL/1 jump vectors
  1800 c3 ce 1c     ; jp 0x1cce            | PL/1 AAAA
  1803 c3 78 18     ; jp 0x1878            | PL/1 return from subroutine?
  1806 c3 53 1f     ; jp 0x1f53            | PL/1 CCCC
  1809 c3 7c 18     ; jp 0x187c            | PL/1 RUN Microcode Program

  ;PL/1 instruction vectors
  180c 9d           ; sbc a, l             |
  180d 18 fb        ; jr 0x180a            |
  180f 1c           ; inc e                |
  1810 cb 1d        ; rr l                 |
  1812 ac           ; xor h                |
  1813 18 15        ; jr 0x182a            |
  1815 1d           ; dec e                |
  1816 78           ; ld a, b              |
  1817 1d           ; dec e                |
  1818 92           ; sub d                |
  1819 19           ; add hl, de           |
  181a 37           ; scf                  |
  181b 1c           ; inc e                |
  181c dd 1b        ; dec de               |
  181e 12           ; ld (de), a           |
  181f 1c           ; inc e                |
  1820 a5           ; and l                |
  1821 18 4d        ; jr 0x1870            |
  1823 1c           ; inc e                |
  1824 b4           ; or h                 |
  1825 18 be        ; jr 0x17e5            |
  1827 1d           ; dec e                |
  1828 bb           ; cp e                 |
  1829 18 b3        ; jr 0x17de            |
  182b 1e c3        ; ld e, 0xc3           |
  182d 18 24        ; jr 0x1853            |
  182f 1e 2c        ; ld e, 0x2c           |
  1831 1b           ; dec de               |
  1832 38 1b        ; jr c, 0x184f         |
  1834 44           ; ld b, h              |
  1835 1b           ; dec de               |
  1836 cc 18 e8     ; call z, 0xe818       |
  1839 1a           ; ld a, (de)           |
  183a d7           ; rst 0x10             |
  183b 1b           ; dec de               |
  183c f1           ; pop af               |
  183d 1a           ; ld a, (de)           |
  183e 20 1b        ; jr nz, 0x185b        |
  1840 f5           ; push af              |
  1841 18 18        ; jr 0x185b            |
  1843 00           ; nop                  |
  1844 34           ; inc (hl)             |
  1845 1d           ; dec e                |
  1846 38 1d        ; jr c, 0x1865         |
  1848 fb           ; ei                   |
  1849 18 38        ; jr 0x1883            |
  184b 19           ; add hl, de           |
  184c 61           ; ld h, c              |
  184d 1d           ; dec e                |
  184e 42           ; ld b, d              |
  184f 1d           ; dec e                |
  1850 c9           ; ret                  |
  1851 1b           ; dec de               |
  1852 4a           ; ld c, d              |
  1853 19           ; add hl, de           |
  1854 39           ; add hl, sp           |
  1855 19           ; add hl, de           |
  1856 50           ; ld d, b              |
  1857 19           ; add hl, de           |
  1858 6b           ; ld l, e              |
  1859 19           ; add hl, de           |
  185a 58           ; ld e, b              |
  185b 19           ; add hl, de           |
  185c 73           ; ld (hl), e           |
  185d 19           ; add hl, de           |
  185e db 19        ; in a, (0x19)         |
  1860 3f           ; ccf                  |
  1861 19           ; add hl, de           |
  1862 77           ; ld (hl), a           |
  1863 1b           ; dec de               |
  1864 af           ; xor a                |
  1865 1b           ; dec de               |
  1866 bc           ; cp h                 |
  1867 1b           ; dec de               |
  1868 4d           ; ld c, l              |
  1869 1b           ; dec de               |
  186a d0           ; ret nc               |
  186b 1b           ; dec de               |
  186c db 1f        ; in a, (0x1f)         |
  186e b9           ; cp c                 |
  186f 19           ; add hl, de           |
  1870 ea           ; db 0xea              |
  1871 18 df        ; jr 0x1852            |
  1873 18 b0        ; jr 0x1825            |
  1875 1f           ; rra                  |
  1876 f2 1f e1     ; jp p, 0xe11f         |

  ;return from subrouine?
  1878 e1           ; pop hl               |
  1879 c3 7f 18     ; jp 0x187f            |

  ;run microcode program
  187c 2a fe 40     ; ld hl, (0x40fe)      | Interpretive Program Counter
  187f 7e           ; ld a, (hl)           | get instruction (or data)
  1880 23           ; inc hl               |
  1881 87           ; add a, a             |
  1882 fa 95 18     ; jp m, 0x1895         | jump if a > 63 (is address?)
  1885 da 95 18     ; jp c, 0x1895         |
  1888 22 fe 40     ; ld (0x40fe), hl      |
  188b c6 0c        ; add a, 0xc           |
  188d 6f           ; ld l, a              |
  188e 26 18        ; ld h, 0x18           |
  1890 7e           ; ld a, (hl)           | a = (0x18xx) xx = 2*a + 12; ex. instr 0xa is at 0x1820 -> jp 0x18a5
  1891 23           ; inc hl               |
  1892 66           ; ld h, (hl)           |
  1893 6f           ; ld l, a              |
  1894 e9           ; jp (hl)              | jump to instruction code
  1895 1f           ; rra                  | get original value of a
  1896 5e           ; ld e, (hl)           | get next byte of address
  1897 23           ; inc hl               |
  1898 57           ; ld d, a              |
  1899 d5           ; push de              | push address on stack
  189a c3 7f 18     ; jp 0x187f            | get next instr or address
  189d e1           ; pop hl               | INST 00 - stack number from address on stack
  189e 4e           ; ld c, (hl)           |
  189f 23           ; inc hl               |
  18a0 46           ; ld b, (hl)           |
  18a1 c5           ; push bc              |
  18a2 c3 7c 18     ; jp 0x187c            |
  18a5 e1           ; pop hl               | INST 0A - add
  18a6 d1           ; pop de               |
  18a7 19           ; add hl, de           |
  18a8 e5           ; push hl              |
  18a9 c3 7c 18     ; jp 0x187c            |
  18ac d1           ; pop de               | INST 03 - store binary number at stack address
  18ad e1           ; pop hl               |
  18ae 73           ; ld (hl), e           |
  18af 23           ; inc hl               |
  18b0 72           ; ld (hl), d           |
  18b1 c3 7c 18     ; jp 0x187c            |
  18b4 e1           ; pop hl               | INST 0C - replace binary number with negation
  18b5 cd 15 00     ; call 0x15            | call NhL routine
  18b8 c3 a8 18     ; jp 0x18a8            |
  18bb d1           ; pop de               | INST 0E - multiply binary
  18bc c1           ; pop bc               |
  18bd cd 0c 00     ; call 0xc             | call MUL routine
  18c0 c3 a8 18     ; jp 0x18a8            |
  18c3 d1           ; pop de               |
  18c4 e1           ; pop hl               |
  18c5 cd 0f 00     ; call 0xf             | call DIV routine
  18c8 d5           ; push de              |
  18c9 c3 7c 18     ; jp 0x187c            |
  18cc cd 2b 1d     ; call 0x1d2b          | INST 15 - PUT data to specified device driver
  18cf 41           ; ld b, c              |
  18d0 cd 2b 1d     ; call 0x1d2b          | increment IPC
  18d3 21 fb 40     ; ld hl, 0x40fb        | Output routine for PUT
  18d6 36 c3        ; ld (hl), 0xc3        |
  18d8 23           ; inc hl               |
  18d9 71           ; ld (hl), c           |
  18da 23           ; inc hl               |
  18db 70           ; ld (hl), b           |
  18dc c3 7c 18     ; jp 0x187c            |
  18df 2a fe 40     ; ld hl, (0x40fe)      |
  18e2 46           ; ld b, (hl)           |
  18e3 23           ; inc hl               |
  18e4 4e           ; ld c, (hl)           |
  18e5 c5           ; push bc              |
  18e6 23           ; inc hl               |
  18e7 c3 7f 18     ; jp 0x187f            |
  18ea 2a fe 40     ; ld hl, (0x40fe)      |
  18ed 4e           ; ld c, (hl)           |
  18ee 23           ; inc hl               |
  18ef 06 00        ; ld b, 0x0            |
  18f1 c5           ; push bc              |
  18f2 c3 7f 18     ; jp 0x187f            |
  18f5 cd 03 00     ; call 0x3             | call TOSTR routine
  18f8 c3 7c 18     ; jp 0x187c            |
  18fb e1           ; pop hl               |
  18fc 7e           ; ld a, (hl)           |
  18fd 23           ; inc hl               |
  18fe 23           ; inc hl               |
  18ff fe 04        ; cp 0x4               |
  1901 d2 fc 18     ; jp nc, 0x18fc        |
  1904 2b           ; dec hl               |
  1905 2b           ; dec hl               |
  1906 22 00 42     ; ld (0x4200), hl      |
  1909 d1           ; pop de               |
  190a 14           ; inc d                |
  190b 15           ; dec d                |
  190c ca 1b 19     ; jp z, 0x191b         |
  190f 2b           ; dec hl               |
  1910 4e           ; ld c, (hl)           |
  1911 2b           ; dec hl               |
  1912 46           ; ld b, (hl)           |
  1913 7b           ; ld a, e              |
  1914 02           ; ld (bc), a           |
  1915 7a           ; ld a, d              |
  1916 03           ; inc bc               |
  1917 02           ; ld (bc), a           |
  1918 c3 09 19     ; jp 0x1909            |
  191b 2a 00 42     ; ld hl, (0x4200)      |
  191e 7e           ; ld a, (hl)           |
  191f 23           ; inc hl               |
  1920 eb           ; ex de, hl            |
  1921 2a fe 40     ; ld hl, (0x40fe)      |
  1924 eb           ; ex de, hl            |
  1925 01 78 18     ; ld bc, 0x1878        |
  1928 d5           ; push de              |
  1929 c5           ; push bc              |
  192a b7           ; or a                 |
  192b c2 7f 18     ; jp nz, 0x187f        |
  192e e9           ; jp (hl)              |
  192f 21 ff 42     ; ld hl, 0x42ff        |
  1932 2d           ; dec l                |
  1933 77           ; ld (hl), a           |
  1934 0d           ; dec c                |
  1935 c2 32 19     ; jp nz, 0x1932        |
  1938 c9           ; ret                  | INST 1F - return from subroutine
  1939 cd 21 00     ; call 0x21            | call GETDN routine
  193c c3 7c 18     ; jp 0x187c            |
  193f c1           ; pop bc               |
  1940 d1           ; pop de               |
  1941 7b           ; ld a, e              |
  1942 41           ; ld b, c              |
  1943 cd 2f 19     ; call 0x192f          |
  1946 48           ; ld c, b              |
  1947 c3 6d 19     ; jp 0x196d            |
  194a cd 24 00     ; call 0x24            | INST 23 - get new line of keyboard input
  194d c3 7c 18     ; jp 0x187c            |
  1950 c1           ; pop bc               |
  1951 e1           ; pop hl               |
  1952 cd 1e 00     ; call 0x1e            |
  1955 c3 7c 18     ; jp 0x187c            |
  1958 cd 03 00     ; call 0x3             | call TOSTR
  195b 3e 20        ; ld a, 0x20           |
  195d 0e 10        ; ld c, 0x10           |
  195f cd 2f 19     ; call 0x192f          |
  1962 c1           ; pop bc               |
  1963 3e 10        ; ld a, 0x10           |
  1965 91           ; sub c                |
  1966 c5           ; push bc              |
  1967 4f           ; ld c, a              |
  1968 cd fb 40     ; call 0x40fb          |
  196b c1           ; pop bc               |
  196c e1           ; pop hl               |
  196d cd fb 40     ; call 0x40fb          |
  1970 c3 7c 18     ; jp 0x187c            |
  1973 d1           ; pop de               |
  1974 c1           ; pop bc               |
  1975 e1           ; pop hl               |
  1976 e5           ; push hl              |
  1977 d5           ; push de              |
  1978 cd e7 1f     ; call 0x1fe7          |
  197b 7b           ; ld a, e              |
  197c 90           ; sub b                |
  197d da 6b 19     ; jp c, 0x196b         |
  1980 e1           ; pop hl               |
  1981 e1           ; pop hl               |
  1982 f5           ; push af              |
  1983 48           ; ld c, b              |
  1984 cd fb 40     ; call 0x40fb          |
  1987 c1           ; pop bc               |
  1988 48           ; ld c, b              |
  1989 3e 20        ; ld a, 0x20           |
  198b cd 2f 19     ; call 0x192f          |
  198e 48           ; ld c, b              |
  198f c3 6d 19     ; jp 0x196d            |
  1992 c1           ; pop bc               | INST 06 - store a string of bytes
  1993 e1           ; pop hl               |
  1994 d1           ; pop de               |
  1995 03           ; inc bc               |
  1996 13           ; inc de               |
  1997 1b           ; dec de               |
  1998 7a           ; ld a, d              |
  1999 b3           ; or e                 |
  199a ca b5 19     ; jp z, 0x19b5         |
  199d 0b           ; dec bc               |
  199e 78           ; ld a, b              |
  199f b1           ; or c                 |
  19a0 7e           ; ld a, (hl)           |
  19a1 23           ; inc hl               |
  19a2 e3           ; ex (sp), hl          |
  19a3 ca ac 19     ; jp z, 0x19ac         |
  19a6 77           ; ld (hl), a           |
  19a7 23           ; inc hl               |
  19a8 e3           ; ex (sp), hl          |
  19a9 c3 97 19     ; jp 0x1997            |
  19ac 36 00        ; ld (hl), 0x0         |
  19ae 23           ; inc hl               |
  19af 1b           ; dec de               |
  19b0 7a           ; ld a, d              |
  19b1 b3           ; or e                 |
  19b2 c2 ac 19     ; jp nz, 0x19ac        |
  19b5 e1           ; pop hl               |
  19b6 c3 7c 18     ; jp 0x187c            |
  19b9 c1           ; pop bc               |
  19ba 79           ; ld a, c              |
  19bb e1           ; pop hl               |
  19bc c1           ; pop bc               |
  19bd 47           ; ld b, a              |
  19be d1           ; pop de               |
  19bf 0c           ; inc c                |
  19c0 04           ; inc b                |
  19c1 0d           ; dec c                |
  19c2 ca d4 19     ; jp z, 0x19d4         |
  19c5 05           ; dec b                |
  19c6 ca d4 19     ; jp z, 0x19d4         |
  19c9 7e           ; ld a, (hl)           |
  19ca b7           ; or a                 |
  19cb ca d4 19     ; jp z, 0x19d4         |
  19ce 23           ; inc hl               |
  19cf 12           ; ld (de), a           |
  19d0 13           ; inc de               |
  19d1 c3 c1 19     ; jp 0x19c1            |
  19d4 06 00        ; ld b, 0x0            |
  19d6 d5           ; push de              |
  19d7 c5           ; push bc              |
  19d8 c3 7c 18     ; jp 0x187c            |
  19db c1           ; pop bc               |
  19dc 79           ; ld a, c              |
  19dd c1           ; pop bc               |
  19de d1           ; pop de               |
  19df e1           ; pop hl               |
  19e0 57           ; ld d, a              |
  19e1 14           ; inc d                |
  19e2 1c           ; inc e                |
  19e3 7e           ; ld a, (hl)           |
  19e4 32 1f 42     ; ld (0x421f), a       |
  19e7 fe 2d        ; cp 0x2d              |
  19e9 ca f1 19     ; jp z, 0x19f1         |
  19ec fe 30        ; cp 0x30              |
  19ee c2 f3 19     ; jp nz, 0x19f3        |
  19f1 23           ; inc hl               |
  19f2 1d           ; dec e                |
  19f3 c5           ; push bc              |
  19f4 01 ff 00     ; ld bc, 0xff          |
  19f7 ca 1e 1a     ; jp z, 0x1a1e         |
  19fa 7b           ; ld a, e              |
  19fb d6 05        ; sub 0x5              |
  19fd da 10 1a     ; jp c, 0x1a10         |
  1a00 e5           ; push hl              |
  1a01 85           ; add a, l             |
  1a02 6f           ; ld l, a              |
  1a03 d2 07 1a     ; jp nc, 0x1a07        |
  1a06 24           ; inc h                |
  1a07 7e           ; ld a, (hl)           |
  1a08 e1           ; pop hl               |
  1a09 fe 45        ; cp 0x45              |
  1a0b c2 10 1a     ; jp nz, 0x1a10        |
  1a0e 1e 01        ; ld e, 0x1            |
  1a10 0c           ; inc c                |
  1a11 1d           ; dec e                |
  1a12 ca 1e 1a     ; jp z, 0x1a1e         |
  1a15 7e           ; ld a, (hl)           |
  1a16 23           ; inc hl               |
  1a17 fe 2e        ; cp 0x2e              |
  1a19 c2 10 1a     ; jp nz, 0x1a10        |
  1a1c 1d           ; dec e                |
  1a1d 2b           ; dec hl               |
  1a1e e3           ; ex (sp), hl          |
  1a1f 04           ; inc b                |
  1a20 15           ; dec d                |
  1a21 ca 2d 1a     ; jp z, 0x1a2d         |
  1a24 7e           ; ld a, (hl)           |
  1a25 23           ; inc hl               |
  1a26 fe 56        ; cp 0x56              |
  1a28 c2 1f 1a     ; jp nz, 0x1a1f        |
  1a2b 15           ; dec d                |
  1a2c 2b           ; dec hl               |
  1a2d eb           ; ex de, hl            |
  1a2e e3           ; ex (sp), hl          |
  1a2f d5           ; push de              |
  1a30 e5           ; push hl              |
  1a31 e5           ; push hl              |
  1a32 21 41 42     ; ld hl, 0x4241        |
  1a35 36 00        ; ld (hl), 0x0         |
  1a37 2b           ; dec hl               |
  1a38 1b           ; dec de               |
  1a39 05           ; dec b                |
  1a3a ca ad 1a     ; jp z, 0x1aad         |
  1a3d 0c           ; inc c                |
  1a3e 0d           ; dec c                |
  1a3f ca 6f 1a     ; jp z, 0x1a6f         |
  1a42 1a           ; ld a, (de)           |
  1a43 1b           ; dec de               |
  1a44 fe 2e        ; cp 0x2e              |
  1a46 ca 58 1a     ; jp z, 0x1a58         |
  1a49 fe 2c        ; cp 0x2c              |
  1a4b ca 58 1a     ; jp z, 0x1a58         |
  1a4e fe 20        ; cp 0x20              |
  1a50 ca 58 1a     ; jp z, 0x1a58         |
  1a53 e3           ; ex (sp), hl          |
  1a54 0d           ; dec c                |
  1a55 2b           ; dec hl               |
  1a56 7e           ; ld a, (hl)           |
  1a57 e3           ; ex (sp), hl          |
  1a58 77           ; ld (hl), a           |
  1a59 2b           ; dec hl               |
  1a5a c3 39 1a     ; jp 0x1a39            |
  1a5d 1a           ; ld a, (de)           |
  1a5e e6 fd        ; and 0xfd             |
  1a60 fe 2c        ; cp 0x2c              |
  1a62 1a           ; ld a, (de)           |
  1a63 c0           ; ret nz               |
  1a64 1b           ; dec de               |
  1a65 1a           ; ld a, (de)           |
  1a66 13           ; inc de               |
  1a67 fe 30        ; cp 0x30              |
  1a69 d8           ; ret c                |
  1a6a fe 5a        ; cp 0x5a              |
  1a6c c8           ; ret z                |
  1a6d 1a           ; ld a, (de)           |
  1a6e c9           ; ret                  |
  1a6f cd 5d 1a     ; call 0x1a5d          |
  1a72 fe 24        ; cp 0x24              |
  1a74 ca a6 1a     ; jp z, 0x1aa6         |
  1a77 fe 2d        ; cp 0x2d              |
  1a79 c2 86 1a     ; jp nz, 0x1a86        |
  1a7c 3a 1f 42     ; ld a, (0x421f)       |
  1a7f fe 2d        ; cp 0x2d              |
  1a81 ca a6 1a     ; jp z, 0x1aa6         |
  1a84 3e 20        ; ld a, 0x20           |
  1a86 fe 30        ; cp 0x30              |
  1a88 ca 6f 1a     ; jp z, 0x1a6f         |
  1a8b cd 5d 1a     ; call 0x1a5d          |
  1a8e fe 2d        ; cp 0x2d              |
  1a90 da a1 1a     ; jp c, 0x1aa1         |
  1a93 fe 2e        ; cp 0x2e              |
  1a95 ca a1 1a     ; jp z, 0x1aa1         |
  1a98 fe 39        ; cp 0x39              |
  1a9a 3e 30        ; ld a, 0x30           |
  1a9c ca a6 1a     ; jp z, 0x1aa6         |
  1a9f 3e 20        ; ld a, 0x20           |
  1aa1 fe 24        ; cp 0x24              |
  1aa3 ca 9f 1a     ; jp z, 0x1a9f         |
  1aa6 1b           ; dec de               |
  1aa7 77           ; ld (hl), a           |
  1aa8 2b           ; dec hl               |
  1aa9 05           ; dec b                |
  1aaa c2 86 1a     ; jp nz, 0x1a86        |
  1aad f1           ; pop af               |
  1aae c1           ; pop bc               |
  1aaf d1           ; pop de               |
  1ab0 e3           ; ex (sp), hl          |
  1ab1 24           ; inc h                |
  1ab2 c5           ; push bc              |
  1ab3 01 40 42     ; ld bc, 0x4240        |
  1ab6 25           ; dec h                |
  1ab7 ca df 1a     ; jp z, 0x1adf         |
  1aba 2c           ; inc l                |
  1abb 2d           ; dec l                |
  1abc ca d0 1a     ; jp z, 0x1ad0         |
  1abf 13           ; inc de               |
  1ac0 1a           ; ld a, (de)           |
  1ac1 fe 39        ; cp 0x39              |
  1ac3 c2 cb 1a     ; jp nz, 0x1acb        |
  1ac6 e3           ; ex (sp), hl          |
  1ac7 23           ; inc hl               |
  1ac8 7e           ; ld a, (hl)           |
  1ac9 e3           ; ex (sp), hl          |
  1aca 2d           ; dec l                |
  1acb 03           ; inc bc               |
  1acc 02           ; ld (bc), a           |
  1acd c3 b6 1a     ; jp 0x1ab6            |
  1ad0 13           ; inc de               |
  1ad1 1a           ; ld a, (de)           |
  1ad2 fe 39        ; cp 0x39              |
  1ad4 c2 d9 1a     ; jp nz, 0x1ad9        |
  1ad7 3e 30        ; ld a, 0x30           |
  1ad9 03           ; inc bc               |
  1ada 02           ; ld (bc), a           |
  1adb 25           ; dec h                |
  1adc c2 d0 1a     ; jp nz, 0x1ad0        |
  1adf f1           ; pop af               |
  1ae0 e1           ; pop hl               |
  1ae1 79           ; ld a, c              |
  1ae2 95           ; sub l                |
  1ae3 23           ; inc hl               |
  1ae4 4f           ; ld c, a              |
  1ae5 c3 6d 19     ; jp 0x196d            |
  1ae8 c1           ; pop bc               |
  1ae9 e1           ; pop hl               |
  1aea cd 2d 00     ; call 0x2d            | call CARB (ch to binary)
  1aed d5           ; push de              |
  1aee c3 7c 18     ; jp 0x187c            |
  1af1 e1           ; pop hl               |
  1af2 22 64 42     ; ld (0x4264), hl      |
  1af5 e1           ; pop hl               |
  1af6 22 66 42     ; ld (0x4266), hl      |
  1af9 e1           ; pop hl               |
  1afa 22 68 42     ; ld (0x4268), hl      |
  1afd e1           ; pop hl               |
  1afe 22 6a 42     ; ld (0x426a), hl      |
  1b01 e1           ; pop hl               |
  1b02 11 32 42     ; ld de, 0x4232        |
  1b05 cd 12 00     ; call 0x12            | call BICHAR
  1b08 d5           ; push de              |
  1b09 c5           ; push bc              |
  1b0a cd 06 00     ; call 0x6             | call TOSTR
  1b0d 2a 6a 42     ; ld hl, (0x426a)      |
  1b10 e5           ; push hl              |
  1b11 2a 68 42     ; ld hl, (0x4268)      |
  1b14 e5           ; push hl              |
  1b15 2a 66 42     ; ld hl, (0x4266)      |
  1b18 e5           ; push hl              |
  1b19 2a 64 42     ; ld hl, (0x4264)      |
  1b1c e5           ; push hl              |
  1b1d c3 7c 18     ; jp 0x187c            |
  1b20 e1           ; pop hl               |
  1b21 11 32 42     ; ld de, 0x4232        |
  1b24 cd 12 00     ; call 0x12            | call TODEC
  1b27 d5           ; push de              |
  1b28 c5           ; push bc              |
  1b29 c3 7c 18     ; jp 0x187c            |
  1b2c e1           ; pop hl               |
  1b2d d1           ; pop de               |
  1b2e 7d           ; ld a, l              |
  1b2f a3           ; and e                |
  1b30 6f           ; ld l, a              |
  1b31 7c           ; ld a, h              |
  1b32 a2           ; and d                |
  1b33 67           ; ld h, a              |
  1b34 e5           ; push hl              |
  1b35 c3 7c 18     ; jp 0x187c            |
  1b38 e1           ; pop hl               |
  1b39 d1           ; pop de               |
  1b3a 7d           ; ld a, l              |
  1b3b b3           ; or e                 |
  1b3c 6f           ; ld l, a              |
  1b3d 7c           ; ld a, h              |
  1b3e b2           ; or d                 |
  1b3f 67           ; ld h, a              |
  1b40 e5           ; push hl              |
  1b41 c3 7c 18     ; jp 0x187c            |
  1b44 e1           ; pop hl               |
  1b45 cd 15 00     ; call 0x15            | call NHL (negate binary in hl)
  1b48 2b           ; dec hl               |
  1b49 e5           ; push hl              |
  1b4a c3 7c 18     ; jp 0x187c            |
  1b4d d1           ; pop de               |
  1b4e e1           ; pop hl               |
  1b4f 22 14 42     ; ld (0x4214), hl      |
  1b52 e1           ; pop hl               |
  1b53 22 16 42     ; ld (0x4216), hl      |
  1b56 c1           ; pop bc               |
  1b57 e1           ; pop hl               |
  1b58 e3           ; ex (sp), hl          |
  1b59 7d           ; ld a, l              |
  1b5a e1           ; pop hl               |
  1b5b cd 09 08     ; call 0x809           | call KEY[SEARCH]
  1b5e 2a fe 40     ; ld hl, (0x40fe)      |
  1b61 5e           ; ld e, (hl)           |
  1b62 23           ; inc hl               |
  1b63 22 fe 40     ; ld (0x40fe), hl      |
  1b66 c2 81 1b     ; jp nz, 0x1b81        |
  1b69 7b           ; ld a, e              |
  1b6a 2a 16 42     ; ld hl, (0x4216)      |
  1b6d eb           ; ex de, hl            |
  1b6e 2a 14 42     ; ld hl, (0x4214)      |
  1b71 cd 00 08     ; call 0x800           | call READ
  1b74 c3 81 1b     ; jp 0x1b81            |
  1b77 cd 2b 1d     ; call 0x1d2b          | increment IPC
  1b7a 79           ; ld a, c              |
  1b7b e1           ; pop hl               |
  1b7c d1           ; pop de               |
  1b7d c1           ; pop bc               |
  1b7e cd 00 08     ; call 0x800           | call READ

  ;return from file operations
  1b81 32 f5 40     ; ld (0x40f5), a       | set ONCODE = a
  1b84 ca 97 1b     ; jp z, 0x1b97         |
  1b87 fe 06        ; cp 0x6               |
  1b89 ca a9 1b     ; jp z, 0x1ba9         |
  1b8c 2a f7 40     ; ld hl, (0x40f7)      |
  1b8f 24           ; inc h                |
  1b90 25           ; dec h                |
  1b91 ca a3 1b     ; jp z, 0x1ba3         |
  1b94 22 fe 40     ; ld (0x40fe), hl      |
  1b97 21 00 00     ; ld hl, 0x0           |
  1b9a 22 f9 40     ; ld (0x40f9), hl      |
  1b9d 22 f7 40     ; ld (0x40f7), hl      |
  1ba0 c3 7c 18     ; jp 0x187c            | run loaded program!

  ;UNEXPLORED
  1ba3 cd 18 08     ; call 0x818           | call (error) REPORT
  1ba6 c3 97 1b     ; jp 0x1b97            |
  1ba9 2a f9 40     ; ld hl, (0x40f9)      |
  1bac c3 8f 1b     ; jp 0x1b8f            |
  1baf cd 2b 1d     ; call 0x1d2b          | INST 2C - write on disk
  1bb2 79           ; ld a, c              |
  1bb3 e1           ; pop hl               |
  1bb4 d1           ; pop de               |
  1bb5 c1           ; pop bc               |
  1bb6 cd 03 08     ; call 0x803           | call WRITE
  1bb9 c3 81 1b     ; jp 0x1b81            |
  1bbc cd 2b 1d     ; call 0x1d2b          | INST 2D - rewrite on disk
  1bbf 79           ; ld a, c              |
  1bc0 e1           ; pop hl               |
  1bc1 d1           ; pop de               |
  1bc2 c1           ; pop bc               |
  1bc3 cd 06 08     ; call 0x806           | call REWRITE
  1bc6 c3 81 1b     ; jp 0x1b81            |
  1bc9 e1           ; pop hl               | INST 22 - open file
  1bca cd 0c 08     ; call 0x80c           | call OPEN
  1bcd c3 81 1b     ; jp 0x1b81            |
  1bd0 e1           ; pop hl               |
  1bd1 cd 12 08     ; call 0x812           |
  1bd4 c3 81 1b     ; jp 0x1b81            |
  1bd7 cd 06 00     ; call 0x6             |
  1bda c3 7c 18     ; jp 0x187c            |
  1bdd cd fb 1d     ; call 0x1dfb          | INST 08 - compare decimal
  1be0 e5           ; push hl              |
  1be1 1a           ; ld a, (de)           |
  1be2 0e 08        ; ld c, 0x8            |
  1be4 b6           ; or (hl)              |
  1be5 f2 e9 1b     ; jp p, 0x1be9         |
  1be8 eb           ; ex de, hl            |
  1be9 1a           ; ld a, (de)           |
  1bea be           ; cp (hl)              |
  1beb c2 f4 1b     ; jp nz, 0x1bf4        |
  1bee 2b           ; dec hl               |
  1bef 1b           ; dec de               |
  1bf0 0d           ; dec c                |
  1bf1 c2 e9 1b     ; jp nz, 0x1be9        |
  1bf4 e1           ; pop hl               |
  1bf5 23           ; inc hl               |
  1bf6 f9           ; ld sp, hl            |
  1bf7 3e 02        ; ld a, 0x2            |
  1bf9 ca 02 1c     ; jp z, 0x1c02         |
  1bfc 3d           ; dec a                |
  1bfd d2 02 1c     ; jp nc, 0x1c02        |
  1c00 07           ; rlca                 |
  1c01 07           ; rlca                 |
  1c02 2a fe 40     ; ld hl, (0x40fe)      |
  1c05 a6           ; and (hl)             |
  1c06 01 00 00     ; ld bc, 0x0           |
  1c09 23           ; inc hl               |
  1c0a ca 0e 1c     ; jp z, 0x1c0e         |
  1c0d 0b           ; dec bc               |
  1c0e c5           ; push bc              |
  1c0f c3 7f 18     ; jp 0x187f            |
  1c12 c1           ; pop bc               | INST 09 - compare character strings
  1c13 79           ; ld a, c              |
  1c14 d1           ; pop de               |
  1c15 c1           ; pop bc               |
  1c16 e1           ; pop hl               |
  1c17 47           ; ld b, a              |
  1c18 04           ; inc b                |
  1c19 0c           ; inc c                |
  1c1a 1a           ; ld a, (de)           |
  1c1b 05           ; dec b                |
  1c1c c2 21 1c     ; jp nz, 0x1c21        |
  1c1f 04           ; inc b                |
  1c20 97           ; sub a                |
  1c21 0d           ; dec c                |
  1c22 c2 2e 1c     ; jp nz, 0x1c2e        |
  1c25 0c           ; inc c                |
  1c26 21 07 1c     ; ld hl, 0x1c07        |
  1c29 05           ; dec b                |
  1c2a ca f7 1b     ; jp z, 0x1bf7         |
  1c2d 04           ; inc b                |
  1c2e be           ; cp (hl)              |
  1c2f c2 f7 1b     ; jp nz, 0x1bf7        |
  1c32 23           ; inc hl               |
  1c33 13           ; inc de               |
  1c34 c3 1a 1c     ; jp 0x1c1a            |
  1c37 d1           ; pop de               | INST 07 - compare binary numbers
  1c38 e1           ; pop hl               |
  1c39 7a           ; ld a, d              |
  1c3a ac           ; xor h                |
  1c3b fa 48 1c     ; jp m, 0x1c48         |
  1c3e 7a           ; ld a, d              |
  1c3f bc           ; cp h                 |
  1c40 c2 f7 1b     ; jp nz, 0x1bf7        |
  1c43 7b           ; ld a, e              |
  1c44 bd           ; cp l                 |
  1c45 c3 f7 1b     ; jp 0x1bf7            |
  1c48 7c           ; ld a, h              |
  1c49 ba           ; cp d                 |
  1c4a c3 f7 1b     ; jp 0x1bf7            |
  1c4d cd fb 1d     ; call 0x1dfb          | INST 0B - add decimal
  1c50 47           ; ld b, a              |
  1c51 ae           ; xor (hl)             |
  1c52 4f           ; ld c, a              |
  1c53 e6 80        ; and 0x80             |
  1c55 80           ; add a, b             |
  1c56 96           ; sub (hl)             |
  1c57 da 60 1c     ; jp c, 0x1c60         |
  1c5a ca 9a 1c     ; jp z, 0x1c9a         |
  1c5d 2f           ; cpl                  |
  1c5e 3c           ; inc a                |
  1c5f eb           ; ex de, hl            |
  1c60 e5           ; push hl              |
  1c61 61           ; ld h, c              |
  1c62 3d           ; dec a                |
  1c63 47           ; ld b, a              |
  1c64 c6 07        ; add a, 0x7           |
  1c66 d2 c0 1c     ; jp nc, 0x1cc0        |
  1c69 4f           ; ld c, a              |
  1c6a 0c           ; inc c                |
  1c6b 2f           ; cpl                  |
  1c6c 83           ; add a, e             |
  1c6d 5f           ; ld e, a              |
  1c6e 7d           ; ld a, l              |
  1c6f d6 07        ; sub 0x7              |
  1c71 6f           ; ld l, a              |
  1c72 24           ; inc h                |
  1c73 25           ; dec h                |
  1c74 62           ; ld h, d              |
  1c75 fa 8b 1c     ; jp m, 0x1c8b         |
  1c78 cd 06 1e     ; call 0x1e06          |
  1c7b d2 c0 1c     ; jp nc, 0x1cc0        |
  1c7e 04           ; inc b                |
  1c7f ca b3 1c     ; jp z, 0x1cb3         |
  1c82 7e           ; ld a, (hl)           |
  1c83 ce 00        ; adc a, 0x0           |
  1c85 27           ; daa                  |
  1c86 77           ; ld (hl), a           |
  1c87 23           ; inc hl               |
  1c88 c3 7b 1c     ; jp 0x1c7b            |
  1c8b cd 12 1e     ; call 0x1e12          |
  1c8e da c0 1c     ; jp c, 0x1cc0         |
  1c91 3e 99        ; ld a, 0x99           |
  1c93 86           ; add a, (hl)          |
  1c94 27           ; daa                  |
  1c95 77           ; ld (hl), a           |
  1c96 23           ; inc hl               |
  1c97 c3 8e 1c     ; jp 0x1c8e            |
  1c9a 1b           ; dec de               |
  1c9b 2b           ; dec hl               |
  1c9c 1a           ; ld a, (de)           |
  1c9d be           ; cp (hl)              |
  1c9e da ac 1c     ; jp c, 0x1cac         |
  1ca1 ca 9a 1c     ; jp z, 0x1c9a         |
  1ca4 cd fb 1d     ; call 0x1dfb          |
  1ca7 eb           ; ex de, hl            |
  1ca8 97           ; sub a                |
  1ca9 c3 60 1c     ; jp 0x1c60            |
  1cac cd fb 1d     ; call 0x1dfb          |
  1caf 97           ; sub a                |
  1cb0 c3 60 1c     ; jp 0x1c60            |
  1cb3 1e 07        ; ld e, 0x7            |
  1cb5 16 01        ; ld d, 0x1            |
  1cb7 34           ; inc (hl)             |
  1cb8 2b           ; dec hl               |
  1cb9 7e           ; ld a, (hl)           |
  1cba 72           ; ld (hl), d           |
  1cbb 57           ; ld d, a              |
  1cbc 1d           ; dec e                |
  1cbd c2 b8 1c     ; jp nz, 0x1cb8        |
  1cc0 e1           ; pop hl               |
  1cc1 11 11 00     ; ld de, 0x11          |
  1cc4 cd d1 1c     ; call 0x1cd1          |
  1cc7 f1           ; pop af               |
  1cc8 f1           ; pop af               |
  1cc9 f1           ; pop af               |
  1cca f1           ; pop af               |
  1ccb c3 7c 18     ; jp 0x187c            |

  ;aaaa()
  1cce 11 09 00     ; ld de, 0x9           |
  1cd1 4e           ; ld c, (hl)           |
  1cd2 eb           ; ex de, hl            |
  1cd3 39           ; add hl, sp           |
  1cd4 06 07        ; ld b, 0x7            |
  1cd6 1b           ; dec de               |
  1cd7 1a           ; ld a, (de)           |
  1cd8 b7           ; or a                 |
  1cd9 c2 e6 1c     ; jp nz, 0x1ce6        |
  1cdc 0d           ; dec c                |
  1cdd 05           ; dec b                |
  1cde c2 d6 1c     ; jp nz, 0x1cd6        |
  1ce1 0e 07        ; ld c, 0x7            |
  1ce3 c3 f6 1c     ; jp 0x1cf6            |
  1ce6 71           ; ld (hl), c           |
  1ce7 3e 07        ; ld a, 0x7            |
  1ce9 90           ; sub b                |
  1cea 4f           ; ld c, a              |
  1ceb 2b           ; dec hl               |
  1cec 1a           ; ld a, (de)           |
  1ced 1b           ; dec de               |
  1cee 77           ; ld (hl), a           |
  1cef 05           ; dec b                |
  1cf0 c2 eb 1c     ; jp nz, 0x1ceb        |
  1cf3 0d           ; dec c                |
  1cf4 f8           ; ret m                |
  1cf5 2b           ; dec hl               |
  1cf6 36 00        ; ld (hl), 0x0         |
  1cf8 c3 f3 1c     ; jp 0x1cf3            |
  1cfb d1           ; pop de               | INST 01 - stack float from address on stack
  1cfc 01 00 00     ; ld bc, 0x0           | push 8 0x00 on stack (subroutine?)
  1cff c5           ; push bc              |
  1d00 c5           ; push bc              |
  1d01 c5           ; push bc              |
  1d02 c5           ; push bc              |
  1d03 cd 2b 1d     ; call 0x1d2b          | increment IPC
  1d06 21 07 00     ; ld hl, 0x7           |
  1d09 39           ; add hl, sp           |
  1d0a 1a           ; ld a, (de)           |
  1d0b 13           ; inc de               |
  1d0c 77           ; ld (hl), a           |
  1d0d 2b           ; dec hl               |
  1d0e 0d           ; dec c                |
  1d0f c2 0a 1d     ; jp nz, 0x1d0a        |
  1d12 c3 7c 18     ; jp 0x187c            |
  1d15 cd 2b 1d     ; call 0x1d2b          | INST 04 - store float
  1d18 21 09 00     ; ld hl, 0x9           |
  1d1b 39           ; add hl, sp           |
  1d1c 56           ; ld d, (hl)           |
  1d1d 2b           ; dec hl               |
  1d1e 5e           ; ld e, (hl)           |
  1d1f 2b           ; dec hl               |
  1d20 7e           ; ld a, (hl)           |
  1d21 12           ; ld (de), a           |
  1d22 13           ; inc de               |
  1d23 0d           ; dec c                |
  1d24 c2 1f 1d     ; jp nz, 0x1d1f        |
  1d27 f1           ; pop af               |
  1d28 c3 c7 1c     ; jp 0x1cc7            |

  ;increment IPC value
  1d2b 2a fe 40     ; ld hl, (0x40fe)      | hl = IPC addr
  1d2e 4e           ; ld c, (hl)           |
  1d2f 23           ; inc hl               |
  1d30 22 fe 40     ; ld (0x40fe), hl      |
  1d33 c9           ; ret                  |

  ;UNEXPLORED
  1d34 e1           ; pop hl               |
  1d35 c3 7f 18     ; jp 0x187f            |
  1d38 e1           ; pop hl               |
  1d39 c1           ; pop bc               |
  1d3a 78           ; ld a, b              |
  1d3b b1           ; or c                 |
  1d3c c2 7c 18     ; jp nz, 0x187c        | run microcode program
  1d3f c3 7f 18     ; jp 0x187f            |
  1d42 21 0b 00     ; ld hl, 0xb           |
  1d45 39           ; add hl, sp           |
  1d46 4e           ; ld c, (hl)           |
  1d47 11 08 00     ; ld de, 0x8           |
  1d4a 19           ; add hl, de           |
  1d4b 7e           ; ld a, (hl)           |
  1d4c 23           ; inc hl               |
  1d4d b7           ; or a                 |
  1d4e ca 5c 1d     ; jp z, 0x1d5c         |
  1d51 a9           ; xor c                |
  1d52 fa 5c 1d     ; jp m, 0x1d5c         |
  1d55 d1           ; pop de               |
  1d56 d1           ; pop de               |
  1d57 f9           ; ld sp, hl            |
  1d58 eb           ; ex de, hl            |
  1d59 c3 7f 18     ; jp 0x187f            |
  1d5c d1           ; pop de               |
  1d5d c1           ; pop bc               |
  1d5e c3 57 1d     ; jp 0x1d57            |
  1d61 d1           ; pop de               |
  1d62 e1           ; pop hl               |
  1d63 c1           ; pop bc               |
  1d64 e3           ; ex (sp), hl          |
  1d65 7c           ; ld a, h              |
  1d66 b5           ; or l                 |
  1d67 ca 73 1d     ; jp z, 0x1d73         |
  1d6a 7c           ; ld a, h              |
  1d6b a8           ; xor b                |
  1d6c fa 73 1d     ; jp m, 0x1d73         |
  1d6f e1           ; pop hl               |
  1d70 c3 7f 18     ; jp 0x187f            |
  1d73 eb           ; ex de, hl            |
  1d74 d1           ; pop de               |
  1d75 c3 7f 18     ; jp 0x187f            |
  1d78 2a fe 40     ; ld hl, (0x40fe)      | INST 05 - store decimal number as fixed point
  1d7b 4e           ; ld c, (hl)           |
  1d7c 23           ; inc hl               |
  1d7d 46           ; ld b, (hl)           |
  1d7e 23           ; inc hl               |
  1d7f 22 fe 40     ; ld (0x40fe), hl      |
  1d82 21 09 00     ; ld hl, 0x9           |
  1d85 39           ; add hl, sp           |
  1d86 56           ; ld d, (hl)           |
  1d87 2b           ; dec hl               |
  1d88 5e           ; ld e, (hl)           |
  1d89 2b           ; dec hl               |
  1d8a 7e           ; ld a, (hl)           |
  1d8b eb           ; ex de, hl            |
  1d8c e5           ; push hl              |
  1d8d d5           ; push de              |
  1d8e 90           ; sub b                |
  1d8f 87           ; add a, a             |
  1d90 f2 9f 1d     ; jp p, 0x1d9f         |
  1d93 36 00        ; ld (hl), 0x0         |
  1d95 23           ; inc hl               |
  1d96 0d           ; dec c                |
  1d97 ca b9 1d     ; jp z, 0x1db9         |
  1d9a 3c           ; inc a                |
  1d9b 3c           ; inc a                |
  1d9c fa 93 1d     ; jp m, 0x1d93         |
  1d9f 1b           ; dec de               |
  1da0 1a           ; ld a, (de)           |
  1da1 77           ; ld (hl), a           |
  1da2 23           ; inc hl               |
  1da3 0d           ; dec c                |
  1da4 c2 9f 1d     ; jp nz, 0x1d9f        |
  1da7 e6 f0        ; and 0xf0             |
  1da9 2b           ; dec hl               |
  1daa 05           ; dec b                |
  1dab f2 af 1d     ; jp p, 0x1daf         |
  1dae 77           ; ld (hl), a           |
  1daf d1           ; pop de               |
  1db0 e1           ; pop hl               |
  1db1 1a           ; ld a, (de)           |
  1db2 e6 80        ; and 0x80             |
  1db4 b6           ; or (hl)              |
  1db5 77           ; ld (hl), a           |
  1db6 c3 27 1d     ; jp 0x1d27            |
  1db9 f1           ; pop af               |
  1dba f1           ; pop af               |
  1dbb c3 27 1d     ; jp 0x1d27            |
  1dbe cd fb 1d     ; call 0x1dfb          | INST 0D - negate decimal?
  1dc1 b7           ; or a                 |
  1dc2 ca 7c 18     ; jp z, 0x187c         |
  1dc5 ee 80        ; xor 0x80             |
  1dc7 12           ; ld (de), a           |
  1dc8 c3 7c 18     ; jp 0x187c            |
  1dcb d1           ; pop de               | INST 02 - stack dec num from address on stack
  1dcc 01 00 00     ; ld bc, 0x0           |
  1dcf c5           ; push bc              |
  1dd0 c5           ; push bc              |
  1dd1 c5           ; push bc              |
  1dd2 c5           ; push bc              |
  1dd3 2a fe 40     ; ld hl, (0x40fe)      |
  1dd6 4e           ; ld c, (hl)           |
  1dd7 23           ; inc hl               |
  1dd8 7e           ; ld a, (hl)           |
  1dd9 23           ; inc hl               |
  1dda 22 fe 40     ; ld (0x40fe), hl      |
  1ddd 21 07 00     ; ld hl, 0x7           |
  1de0 39           ; add hl, sp           |
  1de1 e5           ; push hl              |
  1de2 77           ; ld (hl), a           |
  1de3 2b           ; dec hl               |
  1de4 1a           ; ld a, (de)           |
  1de5 13           ; inc de               |
  1de6 0d           ; dec c                |
  1de7 f2 e2 1d     ; jp p, 0x1de2         |
  1dea e1           ; pop hl               |
  1deb 2b           ; dec hl               |
  1dec 7e           ; ld a, (hl)           |
  1ded 47           ; ld b, a              |
  1dee e6 7f        ; and 0x7f             |
  1df0 77           ; ld (hl), a           |
  1df1 a8           ; xor b                |
  1df2 23           ; inc hl               |
  1df3 b6           ; or (hl)              |
  1df4 77           ; ld (hl), a           |
  1df5 cd ce 1c     ; call 0x1cce          | call aaaa()
  1df8 c3 7c 18     ; jp 0x187c            | run microcode program
  1dfb 21 09 00     ; ld hl, 0x9           |
  1dfe 11 08 00     ; ld de, 0x8           |
  1e01 39           ; add hl, sp           |
  1e02 eb           ; ex de, hl            |
  1e03 19           ; add hl, de           |
  1e04 1a           ; ld a, (de)           |
  1e05 c9           ; ret                  |
  1e06 b7           ; or a                 |
  1e07 1a           ; ld a, (de)           |
  1e08 8e           ; adc a, (hl)          |
  1e09 27           ; daa                  |
  1e0a 77           ; ld (hl), a           |
  1e0b 23           ; inc hl               |
  1e0c 13           ; inc de               |
  1e0d 0d           ; dec c                |
  1e0e c2 07 1e     ; jp nz, 0x1e07        |
  1e11 c9           ; ret                  |
  1e12 37           ; scf                  |
  1e13 3e 99        ; ld a, 0x99           |
  1e15 ce 00        ; adc a, 0x0           |
  1e17 eb           ; ex de, hl            |
  1e18 96           ; sub (hl)             |
  1e19 eb           ; ex de, hl            |
  1e1a 86           ; add a, (hl)          |
  1e1b 27           ; daa                  |
  1e1c 77           ; ld (hl), a           |
  1e1d 13           ; inc de               |
  1e1e 23           ; inc hl               |
  1e1f 0d           ; dec c                |
  1e20 c2 13 1e     ; jp nz, 0x1e13        |
  1e23 c9           ; ret                  |
  1e24 cd 53 1f     ; call 0x1f53          |
  1e27 cd fb 1d     ; call 0x1dfb          |
  1e2a b7           ; or a                 |
  1e2b ca c7 1c     ; jp z, 0x1cc7         |
  1e2e 7e           ; ld a, (hl)           |
  1e2f b7           ; or a                 |
  1e30 ca c7 1c     ; jp z, 0x1cc7         |
  1e33 e5           ; push hl              |
  1e34 06 07        ; ld b, 0x7            |
  1e36 21 18 42     ; ld hl, 0x4218        |
  1e39 36 00        ; ld (hl), 0x0         |
  1e3b 2b           ; dec hl               |
  1e3c 1b           ; dec de               |
  1e3d 1a           ; ld a, (de)           |
  1e3e 77           ; ld (hl), a           |
  1e3f b7           ; or a                 |
  1e40 ca 44 1e     ; jp z, 0x1e44         |
  1e43 4d           ; ld c, l              |
  1e44 2b           ; dec hl               |
  1e45 05           ; dec b                |
  1e46 c2 3c 1e     ; jp nz, 0x1e3c        |
  1e49 36 ff        ; ld (hl), 0xff        |
  1e4b 69           ; ld l, c              |
  1e4c e3           ; ex (sp), hl          |
  1e4d 11 0d 42     ; ld de, 0x420d        |
  1e50 06 07        ; ld b, 0x7            |
  1e52 2b           ; dec hl               |
  1e53 7e           ; ld a, (hl)           |
  1e54 12           ; ld (de), a           |
  1e55 1b           ; dec de               |
  1e56 05           ; dec b                |
  1e57 c2 52 1e     ; jp nz, 0x1e52        |
  1e5a 06 11        ; ld b, 0x11           |
  1e5c 05           ; dec b                |
  1e5d c2 76 1e     ; jp nz, 0x1e76        |
  1e60 f1           ; pop af               |
  1e61 cd fb 1d     ; call 0x1dfb          |
  1e64 96           ; sub (hl)             |
  1e65 2f           ; cpl                  |
  1e66 c6 41        ; add a, 0x41          |
  1e68 21 07 42     ; ld hl, 0x4207        |
  1e6b 34           ; inc (hl)             |
  1e6c 35           ; dec (hl)             |
  1e6d ca 72 1e     ; jp z, 0x1e72         |
  1e70 3c           ; inc a                |
  1e71 23           ; inc hl               |
  1e72 77           ; ld (hl), a           |
  1e73 c3 c1 1c     ; jp 0x1cc1            |
  1e76 cd 3c 00     ; call 0x3c            |
  1e79 11 18 42     ; ld de, 0x4218        |
  1e7c 21 0f 42     ; ld hl, 0x420f        |
  1e7f 1a           ; ld a, (de)           |
  1e80 be           ; cp (hl)              |
  1e81 1b           ; dec de               |
  1e82 2b           ; dec hl               |
  1e83 ca 7f 1e     ; jp z, 0x1e7f         |
  1e86 3c           ; inc a                |
  1e87 ca 8d 1e     ; jp z, 0x1e8d         |
  1e8a d2 5c 1e     ; jp nc, 0x1e5c        |
  1e8d 21 00 42     ; ld hl, 0x4200        |
  1e90 34           ; inc (hl)             |
  1e91 d1           ; pop de               |
  1e92 d5           ; push de              |
  1e93 7b           ; ld a, e              |
  1e94 d6 09        ; sub 0x9              |
  1e96 6f           ; ld l, a              |
  1e97 3e 19        ; ld a, 0x19           |
  1e99 93           ; sub e                |
  1e9a 4f           ; ld c, a              |
  1e9b cd 12 1e     ; call 0x1e12          |
  1e9e c3 79 1e     ; jp 0x1e79            |
  1ea1 12           ; ld (de), a           |
  1ea2 1f           ; rra                  |
  1ea3 78           ; ld a, b              |
  1ea4 1f           ; rra                  |
  1ea5 71           ; ld (hl), c           |
  1ea6 1f           ; rra                  |
  1ea7 89           ; adc a, c             |
  1ea8 1f           ; rra                  |
  1ea9 69           ; ld l, c              |
  1eaa 1f           ; rra                  |
  1eab 93           ; sub e                |
  1eac 1f           ; rra                  |
  1ead 9e           ; sbc a, (hl)          |
  1eae 1f           ; rra                  |
  1eaf 81           ; add a, c             |
  1eb0 1f           ; rra                  |
  1eb1 62           ; ld h, d              |
  1eb2 1f           ; rra                  |
  1eb3 cd 53 1f     ; call 0x1f53          | INST 0F - multiply decimal
  1eb6 cd fb 1d     ; call 0x1dfb          |
  1eb9 86           ; add a, (hl)          |
  1eba d6 41        ; sub 0x41             |
  1ebc 32 10 42     ; ld (0x4210), a       |
  1ebf 3e ff        ; ld a, 0xff           |
  1ec1 12           ; ld (de), a           |
  1ec2 06 07        ; ld b, 0x7            |
  1ec4 4b           ; ld c, e              |
  1ec5 0d           ; dec c                |
  1ec6 1b           ; dec de               |
  1ec7 1a           ; ld a, (de)           |
  1ec8 b7           ; or a                 |
  1ec9 ca cd 1e     ; jp z, 0x1ecd         |
  1ecc 4b           ; ld c, e              |
  1ecd 05           ; dec b                |
  1ece c2 c6 1e     ; jp nz, 0x1ec6        |
  1ed1 59           ; ld e, c              |
  1ed2 06 01        ; ld b, 0x1            |
  1ed4 e5           ; push hl              |
  1ed5 0e 07        ; ld c, 0x7            |
  1ed7 e5           ; push hl              |
  1ed8 26 42        ; ld h, 0x42           |
  1eda 7b           ; ld a, e              |
  1edb 95           ; sub l                |
  1edc c6 17        ; add a, 0x17          |
  1ede 6f           ; ld l, a              |
  1edf e3           ; ex (sp), hl          |
  1ee0 2b           ; dec hl               |
  1ee1 7e           ; ld a, (hl)           |
  1ee2 e3           ; ex (sp), hl          |
  1ee3 c5           ; push bc              |
  1ee4 e5           ; push hl              |
  1ee5 d5           ; push de              |
  1ee6 05           ; dec b                |
  1ee7 c2 ee 1e     ; jp nz, 0x1eee        |
  1eea 0f           ; rrca                 |
  1eeb 0f           ; rrca                 |
  1eec 0f           ; rrca                 |
  1eed 0f           ; rrca                 |
  1eee e6 0f        ; and 0xf              |
  1ef0 ca 36 1f     ; jp z, 0x1f36         |
  1ef3 07           ; rlca                 |
  1ef4 c6 9f        ; add a, 0x9f          |
  1ef6 4f           ; ld c, a              |
  1ef7 06 1e        ; ld b, 0x1e           |
  1ef9 d2 fd 1e     ; jp nc, 0x1efd        |
  1efc 04           ; inc b                |
  1efd 0a           ; ld a, (bc)           |
  1efe 32 81 40     ; ld (0x4081), a       |
  1f01 03           ; inc bc               |
  1f02 0a           ; ld a, (bc)           |
  1f03 32 82 40     ; ld (0x4082), a       |
  1f06 06 00        ; ld b, 0x0            |
  1f08 1a           ; ld a, (de)           |
  1f09 13           ; inc de               |
  1f0a 48           ; ld c, b              |
  1f0b d5           ; push de              |
  1f0c 06 00        ; ld b, 0x0            |
  1f0e 5f           ; ld e, a              |
  1f0f c3 80 40     ; jp 0x4080            |
  1f12 d1           ; pop de               |
  1f13 86           ; add a, (hl)          |
  1f14 27           ; daa                  |
  1f15 d2 19 1f     ; jp nc, 0x1f19        |
  1f18 04           ; inc b                |
  1f19 81           ; add a, c             |
  1f1a 27           ; daa                  |
  1f1b d2 1f 1f     ; jp nc, 0x1f1f        |
  1f1e 04           ; inc b                |
  1f1f 77           ; ld (hl), a           |
  1f20 23           ; inc hl               |
  1f21 1a           ; ld a, (de)           |
  1f22 3c           ; inc a                |
  1f23 c2 08 1f     ; jp nz, 0x1f08        |
  1f26 7e           ; ld a, (hl)           |
  1f27 80           ; add a, b             |
  1f28 27           ; daa                  |
  1f29 77           ; ld (hl), a           |
  1f2a d2 36 1f     ; jp nc, 0x1f36        |
  1f2d 23           ; inc hl               |
  1f2e 7e           ; ld a, (hl)           |
  1f2f ce 00        ; adc a, 0x0           |
  1f31 27           ; daa                  |
  1f32 77           ; ld (hl), a           |
  1f33 da 2d 1f     ; jp c, 0x1f2d         |
  1f36 d1           ; pop de               |
  1f37 e1           ; pop hl               |
  1f38 2b           ; dec hl               |
  1f39 c1           ; pop bc               |
  1f3a 0d           ; dec c                |
  1f3b c2 df 1e     ; jp nz, 0x1edf        |
  1f3e 05           ; dec b                |
  1f3f ca 4b 1f     ; jp z, 0x1f4b         |
  1f42 e1           ; pop hl               |
  1f43 21 10 42     ; ld hl, 0x4210        |
  1f46 7e           ; ld a, (hl)           |
  1f47 2b           ; dec hl               |
  1f48 c3 6b 1e     ; jp 0x1e6b            |
  1f4b cd 3c 00     ; call 0x3c            |
  1f4e e1           ; pop hl               |
  1f4f e1           ; pop hl               |
  1f50 c3 d5 1e     ; jp 0x1ed5            |

  ;cccc() - clear 16 bytes in scratch
  1f53 06 08        ; ld b, 0x8            |
  1f55 21 0f 42     ; ld hl, 0x420f        |
  1f58 97           ; sub a                |
  1f59 77           ; ld (hl), a           |
  1f5a 2b           ; dec hl               |
  1f5b 77           ; ld (hl), a           |
  1f5c 2b           ; dec hl               |
  1f5d 05           ; dec b                |
  1f5e c2 59 1f     ; jp nz, 0x1f59        |
  1f61 c9           ; ret                  |

  ;UNEXPLORED
  1f62 83           ; add a, e             |
  1f63 27           ; daa                  |
  1f64 d2 69 1f     ; jp nc, 0x1f69        |
  1f67 06 04        ; ld b, 0x4            |
  1f69 57           ; ld d, a              |
  1f6a 82           ; add a, d             |
  1f6b 27           ; daa                  |
  1f6c d2 71 1f     ; jp nc, 0x1f71        |
  1f6f 04           ; inc b                |
  1f70 04           ; inc b                |
  1f71 57           ; ld d, a              |
  1f72 82           ; add a, d             |
  1f73 27           ; daa                  |
  1f74 d2 78 1f     ; jp nc, 0x1f78        |
  1f77 04           ; inc b                |
  1f78 83           ; add a, e             |
  1f79 27           ; daa                  |
  1f7a d2 12 1f     ; jp nc, 0x1f12        |
  1f7d 04           ; inc b                |
  1f7e c3 12 1f     ; jp 0x1f12            |
  1f81 83           ; add a, e             |
  1f82 27           ; daa                  |
  1f83 d2 88 1f     ; jp nc, 0x1f88        |
  1f86 06 04        ; ld b, 0x4            |
  1f88 5f           ; ld e, a              |
  1f89 83           ; add a, e             |
  1f8a 27           ; daa                  |
  1f8b 5f           ; ld e, a              |
  1f8c d2 78 1f     ; jp nc, 0x1f78        |
  1f8f 04           ; inc b                |
  1f90 c3 77 1f     ; jp 0x1f77            |
  1f93 83           ; add a, e             |
  1f94 27           ; daa                  |
  1f95 5f           ; ld e, a              |
  1f96 d2 71 1f     ; jp nc, 0x1f71        |
  1f99 06 03        ; ld b, 0x3            |
  1f9b c3 71 1f     ; jp 0x1f71            |
  1f9e 57           ; ld d, a              |
  1f9f 83           ; add a, e             |
  1fa0 27           ; daa                  |
  1fa1 5f           ; ld e, a              |
  1fa2 d2 a7 1f     ; jp nc, 0x1fa7        |
  1fa5 06 03        ; ld b, 0x3            |
  1fa7 83           ; add a, e             |
  1fa8 27           ; daa                  |
  1fa9 d2 72 1f     ; jp nc, 0x1f72        |
  1fac 04           ; inc b                |
  1fad c3 72 1f     ; jp 0x1f72            |
  1fb0 c1           ; pop bc               |
  1fb1 e1           ; pop hl               |
  1fb2 d1           ; pop de               |
  1fb3 1c           ; inc e                |
  1fb4 1d           ; dec e                |
  1fb5 ca d4 1f     ; jp z, 0x1fd4         |
  1fb8 e3           ; ex (sp), hl          |
  1fb9 7e           ; ld a, (hl)           |
  1fba 23           ; inc hl               |
  1fbb e3           ; ex (sp), hl          |
  1fbc c5           ; push bc              |
  1fbd e5           ; push hl              |
  1fbe be           ; cp (hl)              |
  1fbf ca cf 1f     ; jp z, 0x1fcf         |
  1fc2 23           ; inc hl               |
  1fc3 0d           ; dec c                |
  1fc4 c2 be 1f     ; jp nz, 0x1fbe        |
  1fc7 41           ; ld b, c              |
  1fc8 f1           ; pop af               |
  1fc9 f1           ; pop af               |
  1fca f1           ; pop af               |
  1fcb c5           ; push bc              |
  1fcc c3 7c 18     ; jp 0x187c            | run microcode program
  1fcf e1           ; pop hl               |
  1fd0 c1           ; pop bc               |
  1fd1 c3 b4 1f     ; jp 0x1fb4            |
  1fd4 f1           ; pop af               |
  1fd5 53           ; ld d, e              |
  1fd6 1b           ; dec de               |
  1fd7 d5           ; push de              |
  1fd8 c3 7c 18     ; jp 0x187c            | run microcode program
  1fdb c1           ; pop bc               |
  1fdc e1           ; pop hl               |
  1fdd cd e7 1f     ; call 0x1fe7          |
  1fe0 48           ; ld c, b              |
  1fe1 06 00        ; ld b, 0x0            |
  1fe3 c5           ; push bc              |
  1fe4 c3 7c 18     ; jp 0x187c            | run microcode program
  1fe7 0c           ; inc c                |
  1fe8 7e           ; ld a, (hl)           |
  1fe9 23           ; inc hl               |
  1fea b7           ; or a                 |
  1feb c8           ; ret z                |
  1fec 0d           ; dec c                |
  1fed c8           ; ret z                |
  1fee 04           ; inc b                |
  1fef c3 e8 1f     ; jp 0x1fe8            |
  1ff2 c1           ; pop bc               |
  1ff3 d1           ; pop de               |
  1ff4 79           ; ld a, c              |
  1ff5 c1           ; pop bc               |
  1ff6 e1           ; pop hl               |
  1ff7 47           ; ld b, a              |
  1ff8 cd 39 00     ; call 0x39            | jump via 0x4f to 0x734
  1ffb e5           ; push hl              |
  1ffc c3 7c 18     ; jp 0x187c            | run microcode program
  1fff ff           ; rst 0x38             |
