; Disassembly of the file "E:\q1\q1_all"
;
; last anotated 9 June 2024 by Karl-Wilhelm Wacker
;
; CPU Type: Z80
;
; Created with dZ80 2.0
;
; Note: Some of the less than optimum [for Z80] code is a
; 	carry over [legacy] of Q1/LMC [8080] code,
;	as the Z80 code is a decendant of the 8080 code.
;
;
; Note: labels prefixed with a lower case "q" are in the
;       4000h-402ffh RAM area. see the Q1/ROS manual as
;	to ther usage [Q1/ROS labels don't have the "q".
;
; Note:	Refer to the Q1/ROS maunal for the usage and
;	calling parametrs for the followin jump vectors:
;
; Note:	A lower case "L" followed by a number is an unlabeled
;	address in the ROM/ARM memory space
;
;
PI:     jp      INIT			;goto system startup routine
TOSTR:  jp      l007f			;goto TOSTR routine
TODEC:  jp      l0174			;goto TODEC routine
UPDIS:  jp      l04f7			;goto UPDIS routine
MUL:    jp      l0669			;goto MUL routine
DIV:    jp      l067b			;goto DIV routine
BICHAR  jp      l06b6			;goto BICHAR routine
NHL:    jp      l06aa			;goto NHL routine
START:  jp      DONE			;programs jump to here when finished [misc cleanup code]
KFILE:  jp      l03f7			;goto KFILE routine
KEYIN:  jp      l049d			;goto KEYIN routine
GETDN:  jp      l06e1			;goto GETDN routine
NKEY:   jp      l0429			;goto NKEY routine
DISPLAY:jp      l0477			;goto DISPLAY routine
PRINTER:jp      l03aa			;goto PRINTER routine
CARB:   jp      l0715			;goto CARB routine
STOP:   jp      l0660			;goto STOP routine
PROCH:  jp      l0507			;goto PROCH routine
INTRET:	jr      EXITINT                 ;goto INTERRUPT exit code jump
INTRUPT:jr      INTVECT                 ;goto INTERRUPT handler code jump
        inc     d			;note: two overlapping JR codes @ 38h & 39h
        nop     			;note second jumps to INDEXJP
SHIFTY:	jp      l079c			;goto SHIFTY routine
        ret     			;fill of return op codes
        ret
        ret
        ret
        ret
        ret
        ret
        ret
        ret
        ret
        ret
        ret
        ret
EXITINT:jp      l037d			;jump to INTERRUPT exit code
INDEXJP:jp      l0769			;jump to SHIFTY routine
INTVECT:jp      INTSAVE			;jump to INTERRUPT handler code
;
l0055:	0dh
l0056:	"    Q1/Lite at Your Service          " ;[40 char]

l007f:  pop     hl
        ld      (4081h),hl
        ld      hl,4214h
        ld      c,04h
l0088:  pop     de
        ld      a,e
        call    l0107
        ld      a,d
        call    l0107
        dec     c
        jp      nz,l0088
        inc     hl
        inc     hl
l0097:  ld      a,d
        add     a,a
l0099:  push    af
        ld      e,a
l009b:  ld      a,(hl)
        cp      30h
        jp      z,l00fa
l00a1:  ld      d,l
        ld      l,14h
l00a4:  dec     hl
        ld      a,(hl)
        cp      30h
        jp      z,l00a4
        ld      a,l
        ld      c,a
        inc     a
        sub     d
        ld      b,a
        ld      hl,3030h
        ld      (4202h),hl
        ld      (4204h),hl
        ld      h,42h
        ld      a,e
        ld      l,c
        inc     hl
        inc     hl
        cp      81h
        jp      c,l0164
        cp      8fh
        jp      nc,l011f
        sub     7bh
        ld      l,a
        sub     c
        jp      z,l00de
        jp      nc,l011a
        dec     d
l00d4:  inc     b
        ld      c,2eh
l00d7:  ld      a,(hl)
        ld      (hl),c
        dec     l
        ld      c,a
        jp      nz,l00d7
l00de:  pop     af
        jp      nc,l00e7
        dec     d
        inc     b
        ld      l,d
        ld      (hl),2dh
l00e7:  ld      e,d
        ld      d,42h
        ld      a,b
        cp      10h
        jp      c,l00f2
        ld      b,10h
l00f2:  ld      c,b
        ld      b,00h
        push    de
        push    bc
        jp      l4080
l00fa:  inc     l
        inc     b
        dec     b
        jp      nz,l00a1
        ld      b,01h
        ld      d,13h
        jp      l00de
l0107:  ld      b,a
        and     0fh
        add     a,30h
        dec     hl
        ld      (hl),a
        dec     hl
        ld      a,b
        rrca
        rrca
        rrca
        rrca
        and     0fh
        add     a,30h
        ld      (hl),a
        ret

l011a:  add     a,b
        ld      b,a
        jp      l00de
l011f:  ld      c,2bh
        sub     80h
l0123:  ld      e,a
        ld      a,l
        cp      11h
        jp      c,l012c
        ld      l,11h
l012c:  ld      (hl),c
        inc     d
        dec     d
        ld      a,e
        jp      pe,l0137
        ld      a,c
        sub     2ch
        add     a,e
l0137:  dec     l
        ld      (hl),45h
        ld      c,2fh
        inc     hl
        inc     hl
l013e:  inc     c
        sub     0ah
        jp      nc,l013e
        add     a,3ah
        ld      b,a
        ld      a,c
        cp      3ah
        jr      c,l014e                 ; (+02h)
        ld      c,39h
l014e:  ld      (hl),c
        inc     hl
        ld      (hl),b
        dec     d
        ld      a,l
        sub     d
        inc     a
        ld      b,a
        ld      l,d
        ld      (hl),2eh
        jp      l00de
l015c:  ld      c,2dh
        cpl
        add     a,81h
        jp      l0123
l0164:  cp      7ch
        jp      c,l015c
        sub     7bh
        ld      d,a
        ld      l,a
        sub     c
        cpl
        inc     a
        ld      b,a
        jp      l00d4
l0174:  call    l1806
        pop     hl
        ld      (4081h),hl
        pop     bc
        inc     c
        ld      e,00h
        ld      b,e
        ld      d,e
        pop     hl
l0182:  call    l01df
        jp      z,l01a6
        jp      nc,l0182
l018b:  push    hl
        ld      hl,4206h
        or      (hl)
        ld      (hl),a
        call    l079c
        pop     hl
        ld      a,b
        sub     d
        ld      b,a
        call    l01df
        jp      z,l01a6
        jp      c,l018b
        cp      15h
        jp      z,l01d2
l01a6:  ld      a,b
        rra
        ld      c,a
        jp      c,l01b0
        call    l079c
        dec     c
l01b0:  ld      hl,4210h
l01b3:  dec     hl
        ld      a,l
        cp      06h
        jp      z,l01bf
        ld      a,(hl)
        or      a
        jp      z,l01b3
l01bf:  ld      a,c
        add     a,l
        add     a,3bh
        and     7fh
        or      e
        inc     hl
        ld      (hl),a
        push    bc
        push    bc
        push    bc
        push    bc
        call    l1800
        jp      l4080
l01d2:  push    de
        push    hl
        call    l0715
        ld      a,e
        add     a,b
        pop     hl
        ld      b,a
        pop     de
        jp      l01a6
l01df:  dec     c
        ret     z

        ld      a,(hl)
        and     7fh
        inc     hl
        sub     30h
        jp      c,l01ef
        cp      0ah
        ret     nz

        or      a
        ret

l01ef:  inc     a
        inc     a
        jp      z,l0204
        inc     a
        jp      z,l01ff
        inc     a
        inc     a
        jp      z,l01df
        or      a
        ret

l01ff:  ld      e,80h
        jp      l01df
l0204:  ld      d,01h
        jp      l01df
l0209:  ld      a,(l0815)
        cp      0c3h
        jp      z,l4086
        ret
;
INTSAVE:push    af			;save regs on stack
        push    bc
        push    de
        push    hl
        jp      l4083			;jump via interrupt vector
;
; this start everything up
;
INIT:	im      1			;interupt mode 1 [vector to 38h on interrupt]]
        ld      a,04h
        out     (01h),a			;turn on shift lock LED [keyboard mode 1]
        ld      de,l02b9		;address of default jump vectors
        ld      hl,l4080
        ld      sp,hl			;set STACK pointer to 4080h [stack ram area]
        ld      c,09h			;set xfer count to 9
l0228:  ld      a,(de)			;this copies 3 jump vaector into RAM
        ld      (hl),a			;starting at 4080h & up
        inc     de			;inc put & take adresses [NOTE this is 8080 way]
        inc     hl			;NOTE that Z80 has more eligant way of doing this
        dec     c			;dec xfer count
        jr      nz,l0228                ; (-07h) loop if more bytes to copy
l022f:  sub     a			;zero A
        ld      (hl),a			;this code zeros out 4089h - 40ffh
        inc     l			;inc L to inc hl pointer
        jr      nz,l022f                ; (-05h) loop if L not zero
        ld      a,0a0h			;reset & home printer & set to 1/120" spacing mode
        out     (07h),a			;issue command
        in      a,(05h)			;test printer status
        or      a			;is it zero [idle, no faults]
        jr      nz,l0243                ; (+06h) skip to here if not
        ld      hl,07fdh		;modify interrupt vector if not ready
        ld      (4084h),hl
l0243:  call    l04d3			;
        call    l042e
;
;	on program exit, run his code while waiting for keyboard
;
DONE:
	ld      hl,l4080		;reset stack pointer to 4080h
        ld      sp,hl			;when exiting user program
        ld      a,(l0815)		;look for jump at 815 [CLRDK]
        cp      0c3h
        jp      nz,l8000	NOTE:	;if not there, jump to ROM code at 8000
;					;this was for the Q1/LMC field unit
;					;which instead of floppies, had a
;					;bank of EPROMs starting at 8000h that
;					;held the application program
;
l0255:  call    l0815			;otherwise do call to CLRDK
        ld      hl,qPLC			;this waits until print buffer is empty
        ld      a,(hl)			;by testing if PLC & PTC are the same
        inc     hl			;
        sub     (hl)			;
        jr      nz,l0255                ;loop back if they are not the same
        in      a,(0ch)
        bit     6,a
        jr      nz,l026e                ; (+08h)
        bit     7,a
        jr      nz,l0255                ; (-15h)
        ld      a,81h
        out     (0ch),a
l026e:  ld      hl,0055h
        ld      c,01h
        call    l0477
        in      a,(04h)
        bit     4,a
        jr      nz,l0284                ; (+08h)
        ld      hl,0056h
        ld      c,03h
        call    l0477
l0284:  ld      hl,0056h
        ld      c,28h
        call    l0477
        in      a,(04h)
        bit     4,a
        jr      nz,l029a                ; (+08h)
        ld      hl,0056h
        ld      c,04h
        call    l0477
l029a:  call    l03f7
        ld      hl,0055h
        ld      c,01h
        call    l0477
        ld      hl,l0249
        ld      (4081h),hl
        call    l080f
        jp      z,l4080
        call    l0818
        call    l042e
        jr      l0249                   ; (-70h)
l02b9:  jp      l02b9
        jp      l02c2
        jp      l0815
l02c2:  ld      a,(qACKT)
        or      a
        jr      nz,l02ce                ; (+06h)
        in      a,(01h)
        or      a
        call    nz,l0507
l02ce:  in      a,(05h)
        or      a
        jp      m,l037d
        ld      bc,0000h
        ld      d,c
        ld      e,c
        ld      a,(qRIB)
        or      a
        jr      z,l02e1                 ; (+02h)
        ld      e,0ah
l02e1:  ld      hl,qPLC
        ld      a,(hl)
        inc     hl
        sub     (hl)
        jr      z,l0346                 ; (+5dh)
        ld      l,(hl)
        ld      h,41h
        inc     l
        ld      a,l
        or      80h
        ld      l,a
        ld      (qPTC),a
        ld      a,(hl)
        ld      h,d
        ld      l,e
        inc     a
        cp      20h
        jr      z,l0346                 ; (+4ah)
        dec     a
        cp      20h
        jr      c,l0307                 ; (+06h)
        jr      nz,l0346                ; (+43h)
        ld      hl,000ah
        add     hl,de
l0307:  cp      08h
        jr      nz,l030f                ; (+04h)
        ld      hl,0fff6h
        add     hl,de
l030f:  cp      0dh
        jr      nz,l031b                ; (+08h)
        ld      hl,(qPOS)
        push    af
        call    l06aa
        pop     af
l031b:  ex      de,hl
        ld      l,c
        ld      h,b
        cp      02h
        jr      nz,l0324                ; (+02h)
        inc     de
        inc     de
l0324:  cp      06h
        jr      nz,l0329                ; (+01h)
        inc     de
l0329:  cp      0dh
        jr      z,l032f                 ; (+02h)
        cp      0ah
l032f:  jr      nz,l0335                ; (+04h)
        ld      hl,0008h
        add     hl,bc
l0335:  cp      01h
        jr      nz,l033d                ; (+04h)
        dec     hl
        dec     hl
        dec     hl
        dec     hl
l033d:  cp      03h
        jr      nz,l0342                ; (+01h)
        inc     hl
l0342:  ld      b,h
        ld      c,l
        jr      l02e1                   ; (-65h)
l0346:  ld      (qRIB),a
        push    af
        push    bc
        ld      a,d
        or      e
        jr      z,l0371                 ; (+22h)
        ld      hl,(qPOS)
        add     hl,de
        ld      (qPOS),hl
        ld      c,00h
        jr      nc,l0362                ; (+08h)
        ld      c,04h
        ex      de,hl
        call    l06aa
        ex      de,hl
        or      a
l0362:  ld      a,d
        rra
        ld      d,a
        ld      a,e
        rra
        ld      e,a
        rra
        rra
        and     40h
        or      c
        ld      c,a
        call    l0386
l0371:  pop     de
        ld      c,08h
        call    l0383
        pop     af
        or      a
        jr      z,l037d                 ; (+02h)
        out     (05h),a
l037d:  pop     hl
        pop     de
        pop     bc
        pop     af
        ei
        ret

l0383:  ld      a,e
        or      d
        ret     z

l0386:  ld      h,d
        ld      l,e
        inc     d
        dec     d
        jp      p,l0394
        inc     c
        inc     c
        inc     c
        inc     c
        call    l06aa
l0394:  ld      a,h
        or      c
        out     (07h),a
        ld      a,l
        out     (06h),a
        ret

        dec     c
        ld      b,l
        ld      c,(hl)
        ld      b,h
        jr      nz,l03f1                ; (+4fh)
        ld      b,(hl)
        jr      nz,l03f7                ; (+52h)
        ld      c,c
        ld      b,d
        ld      b,d
        ld      c,a
        ld      c,(hl)
l03aa:  inc     c
        dec     c
        ret     z

l03ad:  in      a,(05h)
        bit     5,a
        jr      z,l03c5                 ; (+12h)
        exx
        push    af
        ld      c,0eh
        ld      hl,039ch
        call    l0477
        call    l0660
        call    l04d3
        pop     af
        exx
l03c5:  ld      a,(hl)
        or      a
        jr      z,l03e7                 ; (+1eh)
        push    hl
        ld      hl,qPTC
        ld      a,(hl)
        dec     hl
        sub     (hl)
        and     7fh
        dec     a
        jr      z,l03ea                 ; (+15h)
        ld      a,(hl)
        inc     a
        or      80h
        pop     hl
        ld      e,a
        ld      d,41h
        ld      a,(hl)
        ld      (de),a
        ld      a,e
        ld      (qPLC),a
        inc     hl
        dec     c
        jr      nz,l03ad                ; (-3ah)
l03e7:  di
        rst     38h
        ret

l03ea:  push    bc
        call    l0209
        pop     bc
        pop     hl
        di
l03f1:  rst     38h
        jr      l03aa                   ; (-4ah)
l03f4:  call    l042e
l03f7:  call    l04c9
        ld      a,(qTOOK)
        ld      l,a
        ld      h,41h
        ld      c,00h
l0402:  ld      a,(hl)
        inc     l
        jp      m,l03f4
        cp      20h
        jr      z,l0402                 ; (-09h)
        ld      a,l
        dec     a
        ld      (qTOOK),a
        ld      b,08h
l0412:  inc     c
        ld      a,(hl)
        inc     hl
        cp      30h
        dec     b
        jr      z,l041c                 ; (+02h)
        jr      nc,l0412                ; (-0ah)
l041c:  ld      hl,40dah
        ld      b,08h
l0421:  dec     hl
        ld      (hl),20h
        dec     b
        jr      nz,l0421                ; (-06h)
        jr      l049d                   ; (+74h)
l0429:  ld      a,(qTOOK)
        or      a
        ret     z

l042e:  ld      hl,4100h
        di
        ld      (hl),00h
        inc     l
        ld      a,20h
l0437:  ld      (hl),a
        inc     l
        jp      p,l0437
        ld      (qUNDER),a
        call    l04f7
        sub     a
        ld      (qTOOK),a
        ld      (qKSIZ),a
        ld      (qCURSE),a
        ld      (qACKT),a
        ld      (qHEXX),a
        ld      (qINSF),a
        rst     38h			;force interrupt
        ret     			;and return

l0457:  ex      de,hl
        ld      hl,(qOSEZ)
        ex      de,hl
        ld      a,05h
        out     (04h),a
        ld      a,08h
        inc     e
        call    l046d
l0466:  dec     d
        ret     m

        call    l046f
        jr      l0466                   ; (-07h)
l046d:  dec     e
        ret     z

l046f:  out     (04h),a
        dec     e
        ret     z

        out     (04h),a
        jr      l046d                   ; (-0ah)
l0477:  di
        call    l0457
        ex      de,hl
        ld      hl,(qOSEZ)
        ex      de,hl
        inc     c
        dec     c
        jr      z,l0494                 ; (+10h)
l0484:  ld      a,(hl)
        inc     hl
        or      a
        jr      z,l0494                 ; (+0bh)
        out     (03h),a
        inc     de
        cp      0dh
        call    z,l04d3
        dec     c
        jr      nz,l0484                ; (-10h)
l0494:  ex      de,hl
        ld      (qOSEZ),hl
        call    l04fa
        ei
        ret

l049d:  push    hl
        call    l04c9
        pop     de
        ld      hl,qTOOK
        ld      l,(hl)
        ld      h,41h
        ld      a,(qKSIZ)
        ld      b,a
        inc     c
l04ad:  ld      a,b
        cp      l
        jr      z,l04bf                 ; (+0eh)
        dec     c
        jr      z,l04ba                 ; (+06h)
        ld      a,(hl)
        ld      (de),a
        inc     hl
        inc     de
        jr      l04ad                   ; (-0dh)
l04ba:  ld      a,l
        ld      (qTOOK),a
        ret

l04bf:  dec     c
        jp      z,l042e
        ld      a,20h
        ld      (de),a
        inc     de
        jr      l04bf                   ; (-0ah)
l04c9:  ld      a,(qACKT)
        or      a
        ret     nz

        call    l0209
        jr      l04c9                   ; (-0ah)
l04d3:  sub     a
        ld      (qOSEZ),a
        ld      (qOSEZ+1),a
        ld      e,a
        ld      d,a
l04dc:  out     (03h),a
        ld      a,20h
        out     (03h),a
        dec     e
        out     (03h),a
        jr      nz,l04dc                ; (-0bh)
        ld      a,05h
        out     (04h),a
        ret

l04ec:  ld      (qACKT),a
        ld      (qFUNKEY),a
        ld      a,(de)
        ld      l,(hl)
        ld      h,41h
        ld      (hl),a
l04f7:  call    l0457
l04fa:  ld      hl,4100h
        ld      a,(qKSIZ)
        ld      b,a
        inc     b
        ld      c,03h
        otir
        ret

l0507:  ld      hl,qCURSE
        ld      de,qUNDER
l050d:  ld      b,(hl)
        ld      c,b
        cp      0eh
        ret     z

        cp      9ah
        jp      z,l05ab
        cp      9eh
        jp      z,l05bf
        cp      0fh
        jp      z,l0660
        cp      0a0h
        jr      nc,l0566                ; (+41h)
        cp      83h
        jr      nc,l04ec                ; (-3dh)
        cp      1bh
        jp      z,l042e
        cp      1eh
        jp      z,l05f2
        cp      1dh
        jp      z,l0614
        cp      10h
        jp      z,l0607
        cp      09h
        jp      z,l05f8
        cp      1ah
        jp      z,l05ec
        cp      04h
        jr      nz,l0553                ; (+08h)
        ld      a,(de)
        dec     c
        jp      p,l0592
l0550:  inc     c
        jr      l0592                   ; (+3fh)
l0553:  jr      c,l0566                 ; (+11h)
        cp      1ch
        jr      nz,l055c                ; (+03h)
        ld      a,(de)
        jr      l058d                   ; (+31h)
l055c:  jr      nc,l0566                ; (+08h)
        cp      0ch
        jr      nc,l04ec                ; (-76h)
        cp      08h
        jr      c,l04ec                 ; (-7ah)
l0566:  and     7fh
        cp      03h
        jr      nz,l0572                ; (+06h)
        call    l05d3
        or      (hl)
        ld      (hl),a
        ret

l0572:  cp      02h
        jr      nz,l057d                ; (+07h)
        call    l05d3
        cpl
        and     (hl)
        ld      (hl),a
        ret

l057d:  ld      hl,qHEXX
        inc     (hl)
        dec     (hl)
        jp      nz,l0625
l0585:  ld      hl,qINSF
        inc     (hl)
        dec     (hl)
        call    nz,l0649
l058d:  inc     c
        jp      p,l0592
l0591:  dec     c
l0592:  ld      h,41h
        ld      l,b
        ld      (hl),a
        ld      l,c
l0597:  ld      a,(hl)
        ld      (hl),00h
        ld      (de),a
        ld      hl,qCURSE
        ld      (hl),c
        ld      hl,qKSIZ
        ld      a,(hl)
        cp      c
        jp      nc,l04f7
        ld      (hl),c
        jp      l04f7
l05ab:  in      a,(04h)
        bit     4,a
        ld      a,c
        jr      nz,l05b4                ; (+02h)
        sub     07h
l05b4:  sub     28h
        ld      c,a
        ld      a,(de)
        jp      p,l0592
        ld      c,00h
        jr      l0592                   ; (-2dh)
l05bf:  in      a,(04h)
        bit     4,a
        ld      a,c
        jr      nz,l05c8                ; (+02h)
        add     a,07h
l05c8:  add     a,28h
        ld      c,a
        ld      a,(de)
        jp      p,l0592
        ld      c,7fh
        jr      l0592                   ; (-41h)
l05d3:  ld      a,c
        and     0f8h
        rrca
        rrca
        rrca
        add     a,0c0h
        ld      h,40h
        ld      l,a
        ld      a,c
        and     07h
        push    de
        ld      d,a
        ld      a,80h
l05e5:  dec     d
        rlca
        jp      p,l05e5
        pop     de
        ret

l05ec:  ld      a,81h
        ld      (qHEXX),a
        ret

l05f2:  ld      hl,qINSF
        xor     (hl)
        ld      (hl),a
        ret

l05f8:  inc     c
        ld      a,(de)
        jp      m,l0591
        call    l05d3
        and     (hl)
        jr      z,l05f8                 ; (-0bh)
l0603:  ld      a,(de)
        jp      l0592
l0607:  dec     c
        ld      a,(de)
        jp      m,l0550
        call    l05d3
        and     (hl)
        jr      z,l0607                 ; (-0bh)
        jr      l0603                   ; (-11h)
l0614:  ld      hl,417fh
        ld      c,20h
l0619:  ld      a,l
        cp      b
        ld      a,(hl)
        ld      (hl),c
        ld      c,b
        jp      z,l0597
        dec     l
        ld      c,a
        jr      l0619                   ; (-0ch)
l0625:  or      20h
        sub     30h
        cp      10h
        jr      c,l062f                 ; (+02h)
        sub     27h
l062f:  dec     (hl)
        inc     (hl)
        jp      p,l063b
        add     a,10h
        ld      (hl),a
        ld      a,(de)
        jp      l0592
l063b:  ld      c,a
        ld      a,(hl)
        rlca
        rlca
        rlca
        rlca
        dec     a
        or      c
        ld      (hl),00h
        ld      c,b
        jp      l0585
l0649:  ld      h,41h
        ld      l,b
        inc     l
        ret     m

        push    af
        ld      a,(de)
l0650:  ld      c,(hl)
        ld      (hl),a
        ld      a,c
        inc     l
        jp      p,l0650
        ld      c,b
        pop     af
        ld      hl,qKSIZ
        inc     (hl)
        ret     p

        dec     (hl)
        ret

l0660:  di
        in      a,(01h)
        cp      0eh
        jr      nz,l0660                ; (-07h)
        ei
        ret

l0669:  ld      a,10h
        ld      hl,0000h
l066e:  add     hl,hl
        ex      de,hl
        add     hl,hl
        ex      de,hl
        jp      nc,l0676
        add     hl,bc
l0676:  dec     a
        jp      nz,l066e
        ret

l067b:  ld      a,d
        xor     h
        push    af
        xor     d
        call    m,l06aa
        add     hl,hl
        ex      de,hl
        inc     h
        dec     h
        call    p,l06aa
        ld      b,h
        ld      c,l
        ld      hl,0000h
        ld      a,0fh
l0690:  add     hl,hl
        ex      de,hl
        add     hl,hl
        ex      de,hl
        jp      nc,l0698
        inc     hl
l0698:  push    hl
        add     hl,bc
        jr      nc,l06b2                ; (+16h)
        inc     de
        inc     sp
        inc     sp
l069f:  dec     a
        jp      nz,l0690
        pop     af
        ret     p

        ex      de,hl
        call    l06aa
        ex      de,hl
l06aa:  ld      a,h
        cpl
        ld      h,a
        ld      a,l
        cpl
        ld      l,a
        inc     hl
        ret

l06b2:  pop     hl
        jp      l069f
l06b6:  ld      bc,0000h
        inc     h
        dec     h
        push    af
        call    m,l06aa
l06bf:  push    de
        push    bc
        ld      de,000ah
        call    l067b
        ld      a,l
        add     a,30h
        pop     bc
        inc     c
        pop     hl
        ld      (hl),a
        dec     hl
        ex      de,hl
        ld      a,h
        or      l
        jp      nz,l06bf
        inc     de
        pop     af
        ret     p

        inc     c
        ld      a,2dh
        dec     de
        ld      (de),a
        ret

l06de:  call    l042e
l06e1:  call    l04c9
        ld      hl,qTOOK
        ld      l,(hl)
        ld      h,41h
        ld      a,(qKSIZ)
        sub     l
        ld      c,a
        ld      b,a
        jr      z,l06de                 ; (-14h)
        inc     c
l06f3:  call    l01df
        jr      z,l06de                 ; (-1ah)
        jr      nc,l06f3                ; (-07h)
l06fa:  call    l01df
        jr      z,l0705                 ; (+06h)
        jr      c,l06fa                 ; (-07h)
        cp      15h
        jr      z,l06fa                 ; (-0bh)
l0705:  pop     de
        ld      a,b
        sub     c
        ld      c,a
        ld      hl,4240h
        push    hl
        push    bc
        push    de
        call    l049d
        jp      l0174
l0715:  ld      de,0000h
        inc     c
l0719:  dec     c
        ret     z

        ld      a,(hl)
        and     7fh
        inc     hl
        sub     30h
        jp      c,l0757
        cp      0ah
        jp      nc,l0719
        dec     hl
l072a:  push    hl
        ld      h,d
        ld      l,e
        add     hl,hl
        jp      c,l0741
        add     hl,hl
        jp      c,l0741
        add     hl,de
        jp      c,l0741
        add     hl,hl
        jp      c,l0741
        ld      e,a
        ld      d,00h
        add     hl,de
l0741:  ex      de,hl
        pop     hl
        ret     c

        dec     c
        ret     z

        inc     hl
        ld      a,(hl)
        or      80h
        sub     30h
        ret     p

        and     7fh
        cp      0ah
        jp      c,l072a
        inc     d
        dec     d
        ret

l0757:  sub     0feh
        ret     z

        inc     a
        jp      nz,l0719
        call    l0719
        ret     c

        ex      de,hl
        call    l06aa
        cp      a
        ex      de,hl
        ret

l0769:  push    hl
        inc     c
        inc     b
        dec     hl
l076d:  inc     hl
        dec     c
        jr      z,l0797                 ; (+26h)
        ld      a,(hl)
        or      a
        jr      z,l0797                 ; (+22h)
        push    hl
        push    de
        push    bc
        inc     c
l0779:  dec     b
        jr      z,l078d                 ; (+11h)
        ld      a,(de)
        or      a
        jr      z,l078d                 ; (+0dh)
        dec     c
        jr      z,l0788                 ; (+05h)
        inc     de
        cp      (hl)
        inc     hl
        jr      z,l0779                 ; (-0fh)
l0788:  pop     bc
        pop     de
        pop     hl
        jr      l076d                   ; (-20h)
l078d:  pop     af
        pop     af
        pop     de
        pop     hl
        call    l06aa
        add     hl,de
        inc     hl
        ret

l0797:  pop     af
        ld      hl,0000h
        ret

l079c:  push    bc
        push    de
        ld      b,10h
        ld      hl,4200h
        xor     a
l07a4:  rld
        inc     hl
        djnz    l07a4                   ; (-05h)
        pop     de
        pop     bc
        ret

l07ac:  ld      a,(qACKT)
        or      a
        jr      nz,l07b8                ; (+06h)
        in      a,(01h)
        or      a
        call    nz,l0033
l07b8:  ld      hl,qPLC
        ld      a,(hl)
        inc     hl
        cp      (hl)
        jr      z,l07fa                 ; (+3ah)
        in      a,(0ch)
        bit     6,a
        jr      z,l07cc                 ; (+06h)
        ld      a,0c0h
        out     (0ch),a
        jr      l07fa                   ; (+2eh)
l07cc:  and     80h
        jr      nz,l07fa                ; (+2ah)
        ld      hl,qPLC
        ld      a,(hl)
        inc     hl
        sub     (hl)
        jr      z,l07fa                 ; (+22h)
        ld      l,(hl)
        ld      h,41h
        inc     l
        ld      a,l
        or      80h
        ld      (qPTC),a
        ld      l,a
        ld      a,(hl)
        cp      0dh
        jr      nz,l07ec                ; (+04h)
        ld      a,0ah
        jr      l07f2                   ; (+06h)
l07ec:  cp      0ah
        jr      nz,l07f2                ; (+02h)
        ld      a,0dh
l07f2:  cp      7fh
        jr      nz,l07f8                ; (+02h)
        ld      a,7eh
l07f8:  out     (0ch),a
l07fa:  jp      l0036
        jr      l07ac                   ; (-53h)
        ld      b,c
;
;	start of floppy disk ROMs
;
;	See the Q1/ROS manual for the calling parameters
;	and usage of the following jump vectors
;
l0800:  jp      l088f			;READ
l0803:  jp      l094c			;WRITE
        jp      l0977			;REWRITE
l0809:  jp      l0e70			;KEY[SEARCH]
        jp      l0830			;OPEN
l080f:  jp      l0ce2			;LOADER
        jp      l0ca4			;CLOSE
l0815:  jp      l0d3b			;CLRDK
l0818:  jp      l0d6e			;REPORT
        jp      l0b76
        jp      l0bf8
        jp      l0937
        jp      l0947
        jp      l0b08
        jp      l0b21
        jp      l0b2e
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;					;
;	OPEN				;
;					;
;	HL = ADDR OF FILE DESCRIPTION   ;
;					;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
l0830:  sub     a			;OPEN
        ld      (40adh),a		;
        ld      a,80h
        ld      (4213h),a
        push    hl
l083a:  ld      a,(qAD)
        cpl
        ld      b,a
        ld      hl,4213h
        ld      a,(hl)
        rlca
        ld      (hl),a
        ld      hl,40adh
        inc     (hl)
        and     b
        pop     hl
        jr      z,l087d                 ; (+30h)
        push    hl
        ld      de,0002h
        ld      bc,409fh
        call    l0fd9
        ld      (bc),a
        dec     bc
        ld      (bc),a
        ld      a,08h
        inc     hl
        inc     hl
        call    l0809
        pop     hl
        jp      nz,l087d
        ld      de,0018h
        ld      a,01h
        call    l0800
        ld      hl,40adh
        ld      b,(hl)
        ld      hl,(qTHERE)
        ld      de,000fh
        add     hl,de
        ld      (hl),b
        ld      bc,0dc1h
        ret

l087d:  push    hl
        ld      hl,4213h
        ld      a,(hl)
        cp      80h
        jp      m,l083a
        ld      a,04h
        or      a
        pop     hl
        ld      bc,0dc1h
        ret
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;					;
;	READ				;
;					;
;	A  = # RECORDS			;
;	BC = FILE DESCRIPTION ADDR	;
;	DE = ALLOCATED SPACE PER RECORD	;
;	HL = ADDR OF FIRST RECORD       ;
;					;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
l088f:  call    l0e58			;READ routine
        jp      l1000			;goto 1000h [hard disk or IWS EPROM] if disk 7 or 8 selected
        call    l0ac1
        ret     nz

        ld      hl,qERC
        ld      (hl),20h
        call    l0b21
        call    l0aa4
        call    l0b08
l08a7:  ld      e,0ffh
l08a9:  call    l0b2e
        jp      z,l0937
        call    l0c52
        jp      nz,l0937
        ld      a,(qPART2)
        inc     a
        ld      b,a
        ld      c,09h
        exx
        ld      hl,(qPART1)
        ld      a,h
        rra
        ld      a,l
        rra
        ld      b,a
        ld      hl,08efh
        jr      nc,l08ce                ; (+04h)
        ld      hl,08f5h
        inc     b
l08ce:  push    hl
        ld      hl,(qTRKS1)
        dec     hl
        ld      d,(hl)
        in      a,(0ah)			;reset addr mark
        ld      c,0ah
l08d8:  in      a,(c)			;test for addr mark
        jp      p,l08d8			;if not, loop
        dec     c
        in      a,(09h)
        cp      9bh			;is it a data addr mark?
        ret     z

        pop     hl
l08e4:  ld      hl,qERC
        ld      a,02h
        dec     (hl)
        jr      z,l0937                 ; (+4bh)
        jr      l08a7                   ; (-47h)
l08ee:  inc     hl
        in      e,(c)
        ld      (hl),d
        inc     hl
        ld      (hl),e
        add     a,e
        in      d,(c)
        add     a,d
        dec     b
        jr      nz,l08ee                ; (-0dh)
        exx
l08fc:  in      l,(c)
        add     a,l
        dec     b
        jr      nz,l08fc                ; (-06h)
        sub     l
        cp      l
        in      a,(09h)
        jr      nz,l08e4                ; (-24h)
        exx
        inc     hl
        ld      (hl),d
        cp      10h
        jr      nz,l08e4                ; (-2bh)
        rlca
        ld      (qERC),a
        ld      hl,(qTRKS1)
        ex      de,hl
        ld      hl,(4220h)
        add     hl,de
        ld      (qTRKS1),hl
        exx
        inc     (ix+00h)
        jr      nz,l0927                ; (+03h)
        inc     (ix+01h)
l0927:  ld      a,20h
        ld      (qERC),a
        sub     a
        ld      hl,qSNRT
        inc     e
        dec     (hl)
        jp      nz,l08a9
        jr      l0947                   ; (+10h)
l0937:  inc     (ix+00h)
        jr      nz,l093f                ; (+03h)
        inc     (ix+01h)
l093f:  ld      hl,qSNRT
        dec     (hl)
        jp      nz,l0937
        or      a
l0947:  ei
        push    ix
        pop     bc
        ret
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;					;
;	WRITE				;
;					;
;	A  = # RECORDS			;
;	BC = FILE DESCRIPTIONR ADDR	;
;	DE = ALLOCATED SPACE PER RECORD	;
;	HL = ADDR OF FIRST RECORD       ;
;					;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
l094c:  call    l0e58			;WRITE routine
        jp      l1003			;goto 1003h [hard disk or IWS EPROM] if disk 7 or 8 selected
        call    l0ac1
        ret     nz

        call    l0b21
        call    l0aa4
        ld      e,(ix+0eh)
        ld      d,00h
        ld      a,(ix+10h)
        sub     (ix+12h)
        ld      hl,0000h
        dec     a
l096b:  add     hl,de
        inc     a
        jr      nz,l096b                ; (-04h)
        ld      (ix+0ah),l
        ld      (ix+0bh),h
        jr      l0984                   ; (+0dh)
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;					;
;	REWRITE 			;
;					;
;	A  = # RECORDS			;
;	BC = FILE DESCRIPTION ADDR	;
;	DE = ALLOCATED SPACE PER RECORD	;
;	HL = ADDR OF FIRST RECORD       ;
;					;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
l0977:  call    l0e58			;REWRITE routine
        jp      l1006			;goto 1006h [hard disk or IWS EPROM] if disk 7 or 8 selected
        call    l0ac1
        ret     nz

        call    l0aa4
l0984:  ld      hl,qERC
        ld      (hl),20h
        ld      a,(ix+13h)
        or      a
        ld      a,07h
        jp      m,l0937
        call    l0b08
l0995:  ld      e,0ffh
l0997:  call    l0b2e			;
        jr      z,l09ef                 ; (+53h)
        call    l0c52
        jr      nz,l0937                ; (-6ah)
        in      a,(09h)
        ld      a,80h
        out     (0bh),a			;bit 7 turns on write
        exx
        ld      hl,(qPART1)
        in      a,(09h)			;write zero by reading
        ex      de,hl
        ld      hl,(qTRKS1)
        in      a,(09h)			;write another zero by reading
        dec     de
        ld      a,d
        inc     de
        rrca
        in      a,(09h)			;and another zero
        ld      a,(qPART2)
        ld      d,a
        in      a,(09h)			;and another
        inc     d
        ld      bc,0009h
        in      a,(09h)			;and another
        ld      a,9bh
        out     (09h),a			;write addr mark & 09bh
        jp      nc,l0a99
l09cc:  add     a,(hl)			;add byte to cksum
        outi    			;write it to disk
        jr      nz,l09cc                ;if more to write, loop (-05h)
        ld      b,e			;set up count for second half
l09d2:  add     a,(hl)			;add byte to cksum
        outi    			;output it
        jr      nz,l09d2                ;if more to write, loop (-05h)
        dec     d
        jr      z,l09df                 ; (+05h)
l09da:  out     (c),b			;output cksum to disk
        dec     d
        jr      nz,l09da                ; (-05h)
l09df:  out     (09h),a			;write a zero byte
        ld      a,10h
        out     (09h),a			;write trailing 10h
        ld      a,00h
        out     (09h),a			;write a zero to flush buffer
        nop
        nop
        out     (09h),a			;wait till its done by doing this write
        out     (0bh),a			;A7 off, turns off write gare
l09ef:  ld      hl,(qTRKS1)
        ex      de,hl
        ld      hl,(4220h)
        add     hl,de
        ld      (qTRKS1),hl
        exx
        inc     e
        inc     (ix+00h)
        jr      nz,l0a04                ; (+03h)
        inc     (ix+01h)
l0a04:  ld      hl,qNRT
        dec     (hl)
        ld      a,20h
        ld      (qERC),a
        jr      nz,l0997                ; (-78h)
        inc     hl
        ld      a,(hl)
        neg
        add     a,(ix+00h)
        ld      (ix+00h),a
        jr      c,l0a1e                 ; (+03h)
        dec     (ix+01h)
l0a1e:  ld      e,0ffh
l0a20:  call    l0b2e
        jp      z,l0937
        call    l0c52
        jp      nz,l0937
        in      a,(09h)
        ld      l,(ix+0ch)
        ld      h,(ix+0dh)
        inc     l
        dec     h
        jr      z,l0a3b                 ; (+03h)
        dec     l
        ld      h,01h
l0a3b:  ld      bc,0009h
        in      a,(0ah)			;reset addr mark
l0a40:  in      a,(0ah)			;test for addr mark
        or      a
        jp      p,l0a40
        in      a,(09h)
l0a48:  add     a,b
        in      b,(c)
        dec     l
        jr      nz,l0a48                ; (-06h)
l0a4e:  add     a,b
        in      b,(c)
        dec     h
        jr      nz,l0a4e                ; (-06h)
        cp      b
        in      a,(09h)
        jr      nz,l0a81                ; (+28h)
        cp      10h
        jr      nz,l0a81                ; (+24h)
        ld      hl,qERC
        ld      (hl),14h
        ld      hl,(4220h)
        ld      b,h
        ld      c,l
        ld      hl,(qTHERE)
        add     hl,bc
        ld      (qTHERE),hl
        inc     e
        inc     (ix+00h)
        jr      nz,l0a77                ; (+03h)
        inc     (ix+01h)
l0a77:  ld      hl,qSNRT
        dec     (hl)
        jr      nz,l0a20                ; (-5dh)
        sub     a
        jp      l0947
l0a81:  ld      a,03h
        ld      hl,qERC
        dec     (hl)
        jp      z,l0937
        ld      hl,(qTHERE)
        ld      (qTRKS1),hl
        ld      a,(qSNRT)
        ld      (qNRT),a
        jp      l0995
l0a99:  add     a,(hl)
        outi
        ld      b,e
        dec     b
        add     a,(hl)
        outi
        jp      l09d2
l0aa4:  ld      c,(ix+0ch)
        ld      b,(ix+0dh)
        ld      a,e
        cpl
        ld      l,a
        ld      a,d
        cpl
        ld      h,a
        add     hl,bc
        inc     hl
        jr      c,l0ab9                 ; (+05h)
        ld      d,b
        ld      e,c
        ld      hl,0000h
l0ab9:  ld      (qPART2),hl
        ex      de,hl
        ld      (qPART1),hl
        ret

l0ac1:  ld      (qTHERE),hl
        ld      (qSNRT),a
        ld      l,e
        ld      h,d
        ld      (4220h),hl
l0acc:  ld      l,(ix+0fh)
        ld      a,(qDISK)
        cp      l			;I think this does drive select
        jr      z,l0afc                 ; (+27h)
        ld      a,80h
        ld      h,l
l0ad8:  rlca
        dec     l
        jr      nz,l0ad8                ; (-04h)
        ld      l,h
        ld      h,a
        out     (0ah),a			;output drive select
        in      a,(0ah)
        rrca
        jr      c,l0acc                 ; (-19h)
        ld      a,h
        out     (0ah),a
        ld      a,l
        ld      (qDISK),a
        ld      a,0ffh
        ld      (qTRKS),a
        ld      l,24h
        call    l0beb
        call    l0beb
        call    l0beb
l0afc:  in      a,(0ah)
        and     40h
        jr      z,l0b04                 ; (+02h)
        sub     a
        ret

l0b04:  ld      a,05h
        or      a
        ret

l0b08:  ld      a,(ix+16h)
        ld      (ix+00h),a
        ld      a,(ix+17h)
        ld      (ix+01h),a
        ld      hl,(qTHERE)
        ld      (qTRKS+1),hl
        ld      a,(qSNRT)
        ld      (qNRT),a
        ret

l0b21:  ld      a,(ix+00h)
        ld      (ix+16h),a
        ld      a,(ix+01h)
        ld      (ix+17h),a
        ret

l0b2e:  ld      a,(ix+01h)
        cp      (ix+0bh)
        jp      nz,l0b3d
        ld      a,(ix+00h)
        cp      (ix+0ah)
l0b3d:  ret     c

        sub     a
        ld      a,06h
        ret

l0b42:  push    de
        ld      c,0ah
        ld      hl,2710h
        di
l0b49:  in      a,(c)
l0b4b:  in      a,(c)
        jp      m,l0b5f
        dec     l
        jr      nz,l0b4b                ; (-08h)
        in      a,(c)
        jp      m,l0b5f
        dec     h
        jr      nz,l0b4b                ; (-10h)
        ei
        pop     de
        inc     a
        ret

l0b5f:  in      a,(09h)
        cp      9eh
        jr      nz,l0b49                ; (-1ch)
        dec     c
        in      b,(c)
        in      c,(c)
        in      a,(09h)
        sub     b
        sub     c
        jr      nz,l0b49                ; (-27h)
        ei
        ld      hl,qTRKS
        ld      (hl),b
        pop     de
l0b76:  ld      hl,qTRKS
        ld      a,(hl)
        ld      (hl),d
        cp      0feh
        ret     nc

        ld      b,a
        ld      hl,4d00h
        cp      h
        jr      c,l0b8b                 ; (+06h)
        neg
        add     a,99h
        ld      b,a
        inc     l
l0b8b:  ld      a,d
        cp      h
        jr      c,l0b96                 ; (+07h)
        neg
        add     a,99h
        ld      d,a
        set     7,l
l0b96:  ld      a,l
        or      a
        jr      z,l0bb2                 ; (+18h)
        cp      81h
        jr      z,l0bb2                 ; (+14h)
        ld      a,(qDISK)
        ld      h,a
        ld      a,80h
l0ba4:  rlca
        dec     h
        jr      nz,l0ba4                ; (-04h)
        res     0,l
        or      l
        out     (0ah),a
        ld      l,05h
        call    l0beb
l0bb2:  ld      a,b
        sub     d
        ld      b,a
        ret     z

        ld      c,00h
        jr      nc,l0bbf                ; (+05h)
        ld      c,40h
        neg
        ld      b,a
l0bbf:  ld      a,c
        or      a
        jr      nz,l0bc9                ; (+06h)
        in      a,(0ah)
        and     10h
        jr      nz,l0be6                ; (+1dh)
l0bc9:  ld      a,20h
        or      c
        out     (0bh),a
        ld      a,c
        out     (0bh),a
        ld      l,30h
        call    l0beb
        in      a,(0ah)
        and     02h
        jr      nz,l0be1                ; (+05h)
        ld      l,4dh
        call    l0beb
l0be1:  dec     b
        jr      nz,l0bbf                ; (-25h)
        inc     b
        ret

l0be6:  ld      bc,0340h
        jr      l0bc9                   ; (-22h)
l0beb:  in      a,(09h)
        nop
        in      a,(09h)
        dec     l
        in      a,(09h)
        ret     z

        in      a,(09h)
        jr      l0beb                   ; (-0dh)
l0bf8:  ld      hl,qERC
        ld      (hl),0ah
l0bfd:  ei
        ld      e,(ix+00h)
        ld      d,(ix+01h)
        ld      a,(ix+0eh)
        ld      b,(ix+10h)
        dec     b
        cpl
        inc     a
        ld      l,a
        ld      h,0ffh
        ex      de,hl
        ld      a,b
l0c12:  add     hl,de
        inc     a
        jr      c,l0c12                 ; (-04h)
        ld      d,a
        ld      a,l
        sub     e
        ld      e,a
        call    l0b42
        ld      hl,qTRKS
        ld      d,(hl)
        jr      z,l0c52                 ; (+2fh)
l0c23:  ld      l,46h
        call    l0beb
        ld      hl,l8000
        ld      c,0ah
l0c2d:  dec     l
        jr      z,l0c3b                 ; (+0bh)
        in      b,(c)
        jp      p,l0c2d
        in      a,(09h)
        sub     9bh
        jr      z,l0c52                 ; (+17h)
l0c3b:  dec     h
        jr      nz,l0c2d                ; (-11h)
        ld      hl,qERC
        dec     (hl)
        ld      bc,0100h
        jr      z,l0c81                 ; (+3ah)
        in      a,(0ah)
        and     10h
        jr      nz,l0c81                ; (+34h)
        call    l0bbf
        jr      l0c23                   ; (-2fh)
l0c52:  ld      a,e
        ld      l,(ix+0eh)
        cp      l
        jr      nc,l0bfd                ; (-5ch)
        ld      hl,l0800
        ld      c,0ah
l0c5e:  di
        in      a,(0ah)
l0c61:  in      a,(c)
        jp      p,l0c61
        in      a,(09h)
        cp      9eh
        jr      nz,l0c7b                ; (+0fh)
        in      a,(09h)
        cp      d
        jr      nz,l0c84                ; (+13h)
        in      a,(09h)
        cp      e
        jr      nz,l0c7b                ; (+05h)
        in      a,(09h)
        sub     e
        sub     d
        ret     z

l0c7b:  ei
        dec     hl
        ld      a,l
        or      h
        jr      nz,l0c5e                ; (-23h)
l0c81:  sub     a
        inc     a
        ret

l0c84:  ld      c,a
        in      a,(09h)
        ld      b,a
        in      a,(09h)
        sub     c
        sub     b
        ld      b,c
        ld      c,0ah
        jr      nz,l0c5e                ; (-33h)
        in      a,(09h)
        cp      10h
        jr      nz,l0c5e                ; (-39h)
        ld      a,b
        ld      (qTRKS),a
        ld      hl,qERC
        dec     (hl)
        jr      z,l0c81                 ; (-20h)
        jp      l0bfd
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;					;
;	CLOSE				;
;					;
;	HL = ADDR OF FILE DESCRIPTION   ;
;					;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
l0ca4:  ld      bc,000ah		;CLOSE
        ld      d,h
        ld      e,l
        add     hl,bc
        ex      de,hl
        ld      a,(hl)
        ld      (hl),00h
        ld      (de),a
        inc     hl
        inc     de
        ld      a,(hl)
        ld      (hl),00h
        ld      (de),a
        inc     de
        inc     de
        inc     de
        inc     de
        ld      a,(de)
        ld      (40adh),a
        call    l0fd9
        ld      (de),a
        ld      de,0002h
        ld      bc,qINDEX
        ld      (bc),a
        inc     bc
        ld      (bc),a
        dec     bc
        ld      a,08h
        push    hl
        inc     hl
        call    l0809
        pop     hl
        jr      nz,l0cde                ; (+09h)
        dec     hl
        ld      a,01h
        ld      de,0014h
        call    z,l0803
l0cde:  ld      bc,0dc1h
        ret
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;					;
;	LOADER - LOAD PROGRAM INTO RAM	;
;					;
;	FILE DESCRIPTION AT 40D0-40E7	;
;	FILE NAME AT 40D2		;
;					;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
l0ce2:  ld      hl,l1400		;LOADER
        ld      a,(hl)
        or      a
        call    z,l1401
        ld      hl,40d0h
        call    l0830
        ret     nz

        ld      b,03h
l0cf3:  ld      a,(40dah)
        ld      c,a
        ld      a,b
        cp      c
        jr      nc,l0d31                ; (+36h)
        ld      hl,40d0h
        ld      (hl),b
        add     a,04h
        ld      b,a
        ld      de,00ffh
        push    bc
        ld      bc,40d0h
        ld      hl,4200h
        ld      a,01h
        call    l0800
        pop     hl
        ret     nz

        push    hl
        ld      hl,42ffh
        ld      (hl),00h
        inc     l
l0d1a:  pop     bc
        ld      a,(hl)
        or      a
        jr      z,l0cf3                 ; (-2ch)
        push    bc
        inc     hl
        ld      e,(hl)
        inc     hl
        ld      d,(hl)
        inc     hl
        ld      c,(hl)
        inc     c
        dec     c
        inc     hl
        jr      z,l0d1a                 ; (-11h)
        ld      b,00h
        ldir
        jr      l0d1a                   ; (-17h)
l0d31:  ld      a,03h
        and     b
        dec     a
        cp      0ffh
        ret     z

        ld      b,a
        jr      l0cf3                   ; (-48h)
l0d3b:  sub     a
        out     (0bh),a
        ld      (qDISK),a
        out     (0ah),a
        call    l0d56
        jp      z,l1400
        call    l0d5e
        jp      z,l1015
        ret

        ld      c,l			;"MUX"
        ld      d,l
        ld      e,b

        ld      c,c			;"IWS"
        ld      d,a
        ld      d,e

l0d56:  ld      hl,0d50h
        ld      de,17fah
        jr      l0d64                   ; (+06h)
l0d5e:  ld      hl,0d53h
        ld      de,13fah
l0d64:  ld      b,03h
l0d66:  ld      a,(de)
        cp      (hl)
        ret     nz

        inc     hl
        inc     de
        djnz    l0d66                   ; (-07h)
        ret

l0d6e:  push    bc
        push    af
        call    l0d3b			;CLKDSK routine
        ld      hl,0dcfh
        ld      c,01h
        call    l0027
        pop     af
        cp      04h
        jr      z,l0db5                 ; (+35h)
        cp      09h
        jp      m,l0d87
        ld      a,09h
l0d87:  ld      hl,0dceh
        rlca
        ld      e,a
        ld      d,00h
        add     hl,de
        ld      e,(hl)
        inc     hl
        ld      d,(hl)
        inc     hl
        ld      a,(hl)
        sub     e
        ld      c,a
        ex      de,hl
        call    l0027
        ld      c,04h
        ld      hl,0dcbh
        call    l0027
        ld      c,08h
        pop     hl
        inc     hl
        inc     hl
        call    l0027
        call    l0030
        ld      c,01h
        ld      hl,0dcfh
        jp      l0027
l0db5:  ld      hl,(qTHERE)
        ld      a,(qSNRT)
        ld      c,a
        call    l0027
        ld      a,04h
        jr      l0d87                   ; (-3ch)

        ld      c,c			;"INDEX
        ld      c,(hl)
        ld      b,h
        ld      b,l
        ld      e,b

        jr      nz,l0dea                ;"  " (+20h)

        jr      nz,l0dec                ;"  " (+20h)

        ld      c,a			;"ON"
        ld      c,(hl)

        jr      nz,l0ddd                ; (+0dh)
        call    po,lf00d
        dec     c
        jp      m,l050d
        ld      c,0fh
        ld      c,1bh
        ld      c,2dh
l0ddd:  ld      c,3ch
        ld      c,4bh
        ld      c,58h
        ld      c,46h
        ld      c,a
        ld      d,d
        ld      c,l
        ld      b,c
        ld      d,h
l0dea:  jr      nz,l0e31                "ERROR"(+45h)
l0dec:  ld      d,d
        ld      d,d
        ld      c,a
        ld      d,d
        ld      d,d
        ld      b,l
        ld      b,c
        ld      b,h
        jr      nz,l0e3b                ; (+45h)
        ld      d,d
        ld      d,d
        ld      c,a
        ld      d,d
        ld      d,a
        ld      d,d
        ld      c,c
        ld      d,h
        ld      b,l
        jr      nz,l0e46                ; (+45h)
        ld      d,d
        ld      d,d
        ld      c,a
        ld      d,d
        jr      nz,l0e55                ; (+4eh)
        ld      c,a
        ld      d,h
        jr      nz,l0e51                ; (+46h)
        ld      c,a
        ld      d,l
        ld      c,(hl)
        ld      b,h
        ld      b,h
        ld      c,c
        ld      d,e
        ld      c,e
        jr      nz,l0e62                ; (+4dh)
        ld      c,c
        ld      d,e
        ld      d,e
        ld      c,c
        ld      c,(hl)
        ld      b,a
        ld      d,b
        ld      b,c
        ld      d,e
        ld      d,e
        ld      b,l
        ld      b,h
        jr      nz,l0e68                ; (+45h)
        ld      c,(hl)
        ld      b,h
        jr      nz,l0e76                ; (+4fh)
        ld      b,(hl)
        jr      nz,l0e70                ; (+46h)
        ld      c,c
        ld      c,h
        ld      b,l
        ld      d,b
        ld      d,d
        ld      c,a
        ld      d,h
l0e31:  ld      b,l
        ld      b,e
        ld      d,h
        ld      b,l
        ld      b,h
        jr      nz,l0e8f                ; (+57h)
        ld      d,d
        ld      c,c
        ld      d,h
l0e3b:  ld      b,l
        ld      b,h
        ld      b,c
        ld      d,h
        ld      b,c
        jr      nz,l0e8e                ; (+4ch)
        ld      c,c
        ld      c,(hl)
        ld      c,e
        jr      nz,l0e8c                ; (+45h)
        ld      d,d
        ld      d,d
        ld      c,a
        ld      d,d
        ld      d,a
        ld      b,l
        ld      c,c
        ld      d,d
        ld      b,h
        jr      nz,l0e97                ; (+45h)
        ld      d,d
        ld      d,d
        ld      c,a
l0e55:  ld      d,d
        jr      nz,l0e7b                ; (+23h)
;
;	check disk # selected,
;
l0e58:  push    bc			       ;get file des addr
        pop     ix			       ;into ix reg
        ex      af,af'			   ;save af in alt regs
        ld      a,(ix+0fh)	 	 ;get drive # from file descriptor
        cp      07h			       ;test if 1-6 range [8" or 5-1/4] floppy disk
        jr      c,l0e69        ; (+06h) if 1-6, goto 10e69
        ld      a,(l1000)		;else, test if [1000h is not ffh - ROM at 1000h]
        inc     a			;by inc'ing data there
        jr      nz,l0e6e                ; (+05h) goto l0e6e if ROM there
l0e69:  ex      (sp),hl			;no ROM there, so pop return addr into hl
        inc     hl			;and skip instruction after return
        inc     hl			;by inc'ing addr in hl by 3
        inc     hl
        ex      (sp),hl			;put it back on stack
l0e6e:  ex      af,af'			;restore af regs
        ret     			;and return
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;					;
;	KEY[SEARCH]			;
;					;
;	A  = KEY LENGTH			;
;	BC = FILE DESCRIPTION ADDR	;
;	DE = POSITION OF KEY IN RECORD	;
;	HL = ADDR OF KEY		;
;					;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
l0e70:  call    l0e58			;KEY[SEARCH] routine
        jp      l1009			;goto 1009h [hard disk or IWS EPROM] if disk 7 or 8 selected
l0e76:  push    hl
        push    de
        call    l0ac1
l0e7b:  pop     de
        pop     hl
        ret     nz

        ld      (424ah),hl
        ld      a,(ix+0ah)
        or      (ix+0bh)
l0e87:  jp      z,l0fb9
        ld      a,(qSNRT)
        or      a
l0e8e:  jr      z,l0e87                 ; (-09h)
        ld      c,a
        ld      b,00h
        add     hl,bc
        ld      (4220h),hl
l0e97:  ld      b,a
        ld      a,9bh
l0e9a:  dec     hl
        add     a,(hl)
        djnz    l0e9a                   ; (-04h)
        ex      af,af'
        push    bc
        pop     hl
        add     hl,de
        ld      a,(ix+0ch)
        sub     l
        ld      l,a
        ld      a,(ix+0dh)
        sbc     a,h
        jp      c,l0fb9
        ex      af,af'
        ld      h,a
        ld      (4250h),hl
        ex      af,af'
        ld      h,a
        or      l
        dec     hl
        ld      a,h
        ld      hl,0f7ch
        jr      z,l0ec6                 ; (+09h)
        or      a
        ld      hl,0f76h
        jr      z,l0ec6                 ; (+03h)
        ld      hl,0f71h
l0ec6:  push    hl
        pop     iy
        ld      h,e
        ld      l,0ah
        ld      (4252h),hl
        ld      h,c
        dec     l
        ld      (424ch),hl
        ld      a,d
        or      e
        ld      hl,0f54h
        jr      z,l0ee6                 ; (+0bh)
        dec     de
        ld      a,d
        or      a
        ld      hl,l0f4e
        jr      z,l0ee6                 ; (+03h)
        ld      hl,l0f49
l0ee6:  ld      (424eh),hl
        ld      hl,0f67h
        ld      (4254h),hl
        call    l0fcb
        ld      l,(ix+00h)
        ld      h,(ix+01h)
        ld      (4248h),hl
        ld      e,0ffh
l0efd:  ld      a,24h
        ld      (qERC),a
l0f02:  call    l0c52
        jr      nz,l0f32                ; (+2bh)
        push    de
        ld      d,00h
        ld      (qTRKS+1),sp
        ld      sp,424ah
        pop     hl
        pop     bc
        exx
        pop     hl
        pop     de
        ld      a,d
        ex      af,af'
        pop     bc
        in      a,(c)
l0f1b:  in      a,(c)
        jp      p,l0f1b
        dec     c
        in      a,(c)
        cp      9bh
        jr      nz,l0f29                ; (+02h)
        ex      af,af'
        jp      (hl)
l0f29:  ld      sp,(qTRKS+1)
        ld      a,02h
        pop     de
        jr      l0f36                   ; (+04h)
l0f32:  ld      e,0ffh
        ld      a,01h
l0f36:  ld      hl,qERC
        dec     (hl)
        jr      nz,l0f02                ; (-3ah)
        ld      hl,(4248h)
        ld      (ix+00h),l
        ld      (ix+01h),h
        or      a
        jp      l0947
l0f49:  in      d,(c)
        add     a,d
        djnz    l0f49                   ; (-05h)
l0f4e:  in      d,(c)
        add     a,d
        djnz    l0f4e                   ; (-05h)
        ld      d,a
        ld      b,e
        exx
l0f56:  in      a,(09h)
        sub     (hl)
        ret     nz

        inc     hl
        djnz    l0f56                   ; (-07h)
        exx
        in      a,(09h)
        jp      (iy)
l0f62:  in      d,(c)
        inc     hl
        sub     (hl)
        add     a,d
        djnz    l0f62                   ; (-07h)
        ld      b,a
        in      a,(09h)
        exx
        jp      (iy)
l0f6f:  in      d,(c)
        add     a,d
        djnz    l0f6f                   ; (-05h)
l0f74:  in      d,(c)
        add     a,d
        djnz    l0f74                   ; (-05h)
        ld      d,a
        in      a,(09h)
        sub     d
        exx
        sub     b
        jr      nz,l0f29                ; (-58h)
        in      a,(09h)
        cp      10h
        jr      nz,l0f29                ; (-5eh)
        ex      de,hl
        ld      hl,(4220h)
        sbc     hl,de
        ld      hl,(qTRKS+1)
        ld      sp,hl
        pop     de
        jp      nz,l0f98
        sub     a
        jr      l0fc8                   ; (+30h)
l0f98:  inc     e
        inc     (ix+00h)
        jp      nz,l0fa2
        inc     (ix+01h)
l0fa2:  call    l0b2e
        call    z,l0fcf
        ld      hl,(4248h)
        ld      a,l
        cp      (ix+00h)
        jp      nz,l0efd
        ld      a,h
        sub     (ix+01h)
        jp      nz,l0efd
l0fb9:  ld      a,(ix+0ah)
        ld      (ix+00h),a
        ld      a,(ix+0bh)
        ld      (ix+01h),a
        ld      a,04h
        or      a
l0fc8:  jp      l0947
l0fcb:  call    l0b2e
        ret     nz

l0fcf:  sub     a
        ld      (ix+00h),a
        ld      (ix+01h),a
        ld      e,0ffh
        ret

l0fd9:  exx
        ld      hl,0082h
        ld      (40a8h),hl
        ld      a,l
        ld      (40ach),a
        ld      hl,0028h
        ld      (40aah),hl
        sub     a
l0feb:  ld      (0012h),a
        exx
        ret

        dec     l
        in      a,(09h)
l0ff3:  ret     z

        in      a,(09h)
        jr      l0feb                   ; (-0dh)
        ld      hl,qERC
        ld      (hl),0ah
        ei
        rst     38h			;unprogrammed location [ffh]
        rst     38h			;unprogrammed location [ffh]
l1000:  call    l10f6
l1003:  call    l10f6
l1006:  call    l10f6
l1009:  call    l10f6
l100c:  call    l10ee
        jp      l12cd
        call    l10ee
l1015:  jp      l1324
        ret

        push    af
        jr      z,l104f                 ; (+33h)
l101c:  ld      hl,1060h
        cp      09h
        jp      m,l1026
        ld      a,09h
l1026:  rlca
        ld      e,a
        ld      d,00h
        add     hl,de
        ld      e,(hl)
        inc     hl
        ld      d,(hl)
        ex      de,hl
        ld      c,12h
l1031:  call    l0027
        ld      c,04h
        ld      hl,105dh
        call    l0027
        ld      c,08h
        pop     hl
        inc     hl
        inc     hl
        call    l0027
        call    l0030
        ld      c,01h
        ld      hl,1061h
        jp      l0027
l104f:  ld      hl,(qTHERE)
        ld      a,(qPART1)
l1055:  ld      c,a
        call    l0027
        ld      a,04h
        jr      l101c                   ; (-41h)
        jr      nz,l10ae                ; (+4fh)
        ld      c,(hl)
        jr      nz,l106f                ; (+0dh)
        ld      (hl),h
        djnz    l0fe6                   ; (-7fh)
        djnz    l0ff3                   ; (-74h)
        djnz    l1001                   ; (-68h)
        djnz    l100e                   ; (-5dh)
        djnz    l101d                   ; (-50h)
        djnz    l1031                   ; (-3eh)
l106f:  djnz    l1043                   ; (-2eh)
        djnz    l1055                   ; (-1eh)
        djnz    l10bb                   ; (+46h)
        ld      c,a
        ld      d,d
        ld      c,l
        ld      b,c
        ld      d,h
        jr      nz,l10c1                ; (+45h)
        ld      d,d
        ld      d,d
        ld      c,a
        ld      d,d
        nop
        ld      d,d
        ld      b,l
        ld      b,c
        ld      b,h
        jr      nz,l10cc                ; (+45h)
        ld      d,d
        ld      d,d
        ld      c,a
        ld      d,d
        nop
        ld      d,a
        ld      d,d
        ld      c,c
        ld      d,h
        ld      b,l
        jr      nz,l10d8                ; (+45h)
        ld      d,d
        ld      d,d
        ld      c,a
        ld      d,d
        nop
        jr      nz,l10e8                ; (+4eh)
        ld      c,a
        ld      d,h
        jr      nz,l10e4                ; (+46h)
        ld      c,a
        ld      d,l
        ld      c,(hl)
        ld      b,h
        nop
        ld      b,h
        ld      c,c
        ld      d,e
        ld      c,e
        jr      nz,l10f6                ; (+4dh)
        ld      c,c
        ld      d,e
        ld      d,e
        ld      c,c
        ld      c,(hl)
l10ae:  ld      b,a
        nop
        ld      d,b
        ld      b,c
        ld      d,e
        ld      d,e
        ld      b,l
        ld      b,h
        jr      nz,l10fd                ; (+45h)
        ld      c,(hl)
        ld      b,h
        jr      nz,l110b                ; (+4fh)
        ld      b,(hl)
        jr      nz,l1105                ; (+46h)
        ld      c,c
        ld      c,h
l10c1:  ld      b,l
        ld      d,b
        ld      d,d
        ld      c,a
        ld      d,h
        ld      b,l
        ld      b,e
        ld      d,h
        ld      b,l
        ld      b,h
        jr      nz,l1124                ; (+57h)
        ld      d,d
        ld      c,c
        ld      d,h
        ld      b,l
        nop
        ld      b,h
        ld      b,c
        ld      d,h
        ld      b,c
        jr      nz,l1124                ; (+4ch)
l10d8:  ld      c,c
        ld      c,(hl)
        ld      c,e
        jr      nz,l1122                ; (+45h)
        ld      d,d
        ld      d,d
        ld      c,a
        ld      d,d
        nop
        ld      b,d
        ld      b,c
l10e4:  ld      b,h
        jr      nz,l112c                ; (+45h)
        ld      d,d
l10e8:  ld      d,d
        ld      c,a
        ld      d,d
        jr      nz,l1110                ; (+23h)
        nop
l10ee:  push    hl
        pop     bc
        ld      a,(qAD)
        ld      de,0008h
l10f6:  ld      (qTHERE),hl
        ex      de,hl
        ld      (qPART1),hl
l10fd:  push    bc
        pop     hl
        ld      (qTRKS+1),hl
        ld      (qSNRT),a
l1105:  ld      (qNRT),a
        pop     hl
        ld      a,l
        sub     03h
        ld      (qPART2),a
        ld      a,20h
        ld      (4262h),a
l1114:  sub     a
        out     (10h),a
        ld      a,0a7h
        out     (11h),a
        ld      hl,(qTRKS+1)
        ld      de,0018h
        sub     a
l1122:  call    l12c3
        push    af
        ld      a,(qNRT)
        ld      (4248h),a
l112c:  ld      hl,qPART1
        ld      de,4249h
        ld      bc,0003h
        ldir
        pop     af
        ld      hl,4248h
        ld      de,0004h
        call    l12c3
        neg
        ld      (hl),a
        ld      a,0ah
        ld      (qERC),a
l1149:  ld      b,05h
l114b:  ld      a,04h
        out     (10h),a
        in      a,(11h)
        bit     6,a
        jr      z,l1149                 ; (-0ch)
        djnz    l114b                   ; (-0ch)
l1157:  ld      hl,(qTRKS+1)
        ld      de,0018h
        call    l134b
        ld      hl,4248h
        ld      de,0005h
        call    l134b
        ld      de,0001h
        ld      hl,40bah
        sub     a
        ld      (qTRKS+4),a
        call    l1396
        ld      a,(qTRKS+4)
        or      a
        call    nz,l127f
        jr      nz,l1157                ; (-28h)
        ld      a,(40bah)
        cp      50h
        call    nz,l127f
        jr      nz,l1157                ; (-32h)
        ld      a,(qPART2)
        cp      0ch
        jr      z,l11f2                 ; (+62h)
        cp      12h
        jr      z,l11f2                 ; (+5eh)
        cp      09h
        ld      hl,0001h
        jr      z,l119e                 ; (+03h)
        ld      hl,(qPART1)
l119e:  ex      de,hl
        ld      a,(qSNRT)
        ld      b,a
        ld      hl,0000h
l11a6:  add     hl,de
        djnz    l11a6                   ; (-03h)
        ld      (qPART1),hl
        ld      a,(qPART2)
        or      a
        jr      z,l11f2                 ; (+40h)
        ex      de,hl
        ld      hl,(qTHERE)
        sub     a
        call    l12c3
        neg
        ld      (40b9h),a
l11bf:  ld      hl,(qPART1)
        ex      de,hl
        ld      hl,(qTHERE)
        call    l134b
        ld      hl,40b9h
        ld      de,0001h
        call    l134b
        ld      de,0001h
        ld      hl,40bah
        sub     a
        ld      (qTRKS+4),a
        call    l1396
        ld      a,(qTRKS+4)
        or      a
        call    nz,l127f
        jr      nz,l11bf                ; (-29h)
        ld      a,(40bah)
        cp      50h
        call    nz,l127f
        jr      nz,l11bf                ; (-33h)
l11f2:  ei
        ld      hl,4248h
        ld      de,001ah
        sub     a
        ld      (qTRKS+4),a
        call    l1396
        ld      a,(qTRKS+4)
        or      a
        call    nz,l127f
        jr      nz,l11f2                ; (-17h)
        ld      hl,4248h
        sub     a
        ld      de,001ah
        call    l12c3
        ld      (40bah),a
        call    l1341
        ld      a,(40bah)
        or      a
        call    nz,l127f
        jr      nz,l11f2                ; (-30h)
        ld      hl,(qTRKS+1)
        ex      de,hl
        ld      hl,4248h
        ld      bc,0018h
        ldir
        ld      a,(qPART2)
        cp      0fdh
        jr      z,l1236                 ; (+01h)
        or      a
l1236:  ld      a,(hl)
        ld      (qSNRT),a
        jr      nz,l129c                ; (+60h)
l123c:  ld      hl,(qPART1)
        ex      de,hl
        ld      hl,(qTHERE)
        sub     a
        ld      (qTRKS+4),a
        call    l1396
        ld      hl,40b9h
        ld      de,0001h
        call    l1396
        ld      a,(qTRKS+4)
        or      a
        call    nz,l127f
        jr      nz,l123c                ; (-20h)
        ld      hl,(qPART1)
        ex      de,hl
        ld      hl,(qTHERE)
        sub     a
        call    l12c3
        ld      hl,40b9h
        add     a,(hl)
        ld      (40bah),a
        call    l1341
        ld      a,(40bah)
        or      a
        call    nz,l127f
        jr      nz,l123c                ; (-3eh)
        ld      a,(qSNRT)
        jr      l129c                   ; (+1dh)
l127f:  ld      hl,qERC
        dec     (hl)
        ret     nz

l1284:  pop     hl
        call    l1324
        ld      b,00h
l128a:  ld      hl,4262h
        djnz    l128a                   ; (-05h)
        dec     (hl)
        jr      z,l129a                 ; (+08h)
        ld      a,(qPART2)
        cp      0fdh
        jp      nz,l1114
l129a:  ld      a,08h
l129c:  ld      hl,(qTRKS+1)
        ld      d,a
        ld      a,(qPART2)
        cp      0ch
        jr      z,l12a9                 ; (+02h)
        cp      12h
l12a9:  ld      a,d
        jr      nz,l12b4                ; (+08h)
        inc     hl
        inc     hl
        ld      (qTHERE),hl
        ld      hl,1337h
l12b4:  push    hl
        call    l1324
        pop     bc
        ld      a,(qPART1)
        ld      (qSNRT),a
        ld      a,d
        or      a
        ei
        ret

l12c3:  add     a,(hl)
        inc     hl
        dec     de
        ld      c,a
        ld      a,e
        or      d
        ld      a,c
        jr      nz,l12c3                ; (-09h)
        ret

l12cd:  ld      a,(l1400)
        or      a
        call    z,l1401
        ld      hl,40d0h
        call    l100c
        ret     nz

        ld      a,(40dah)
        ld      c,a
        ld      b,0fh
l12e1:  ld      a,b
        cp      c
        jr      nc,l131a                ; (+35h)
        ld      hl,40d0h
        ld      (hl),a
        add     a,10h
        ld      b,a
        ld      de,00ffh
        push    bc
        ld      bc,40d0h
        ld      hl,4201h
        ld      a,01h
        call    l1000
        pop     hl
        ret     nz

        push    hl
        ld      hl,4200h
        ld      (hl),00h
        inc     l
l1304:  pop     bc
        ld      a,(hl)
        or      a
        jr      z,l12e1                 ; (-28h)
        push    bc
        inc     hl
        ld      e,(hl)
        inc     hl
        ld      d,(hl)
        inc     hl
        ld      c,(hl)
        inc     c
l1311:  inc     l
        dec     c
        jr      z,l1304                 ; (-11h)
        ld      a,(hl)
        ld      (de),a
        inc     de
        jr      l1311                   ; (-09h)
l131a:  ld      a,0fh
        and     b
        dec     a
        cp      0ffh
        ret     z

        ld      b,a
        jr      l12e1                   ; (-43h)
l1324:  ld      a,0eah
        out     (10h),a
        sub     a
        out     (10h),a
        ld      a,0a5h
        out     (11h),a
        ld      a,02h
        out     (10h),a
        sub     a
        out     (11h),a
        ret

        ld      d,b
        ld      c,a
        ld      c,c
        ld      c,(hl)
        ld      b,h
        ld      b,l
        ld      e,b
        jr      nz,l1360                ; (+20h)
        jr      nz,l1363                ; (+21h)
        scf
        inc     de
        or      a
        jr      z,l1348                 ; (+01h)
        inc     hl
l1348:  ld      de,0001h
l134b:  ld      b,0ffh
l134d:  call    l13f3
        bit     6,a
        jr      nz,l1359                ; (+05h)
        djnz    l134d                   ; (-09h)
l1356:  jp      l1284
l1359:  di
        sub     a
        out     (10h),a
        ld      a,0a5h
        out     (11h),a
l1361:  call    l13f3
        bit     6,a
        jr      nz,l1361                ; (-07h)
        sub     a
        out     (10h),a
        ld      a,0a7h
        out     (11h),a
        ld      c,11h
        ld      b,0ffh
l1373:  call    l13f3
        bit     6,a
        jr      nz,l137e                ; (+04h)
        djnz    l1373                   ; (-09h)
        jr      l1356                   ; (-28h)
l137e:  ld      a,04h
        out     (10h),a
        in      a,(11h)
        bit     0,a
        jr      z,l137e                 ; (-0ah)
        ex      (sp),hl
        ex      (sp),hl
        ld      a,06h
        out     (10h),a
        outi
        dec     de
        ld      a,d
        or      e
        jr      nz,l137e                ; (-17h)
        ret

l1396:  ld      a,06h
        out     (10h),a
        in      a,(11h)
        sub     a
        out     (10h),a
        ld      a,0e7h
        out     (11h),a
        ld      b,0ffh
l13a5:  call    l13f3
        bit     5,a
        jr      nz,l13c5                ; (+19h)
        bit     6,a
        jr      nz,l13a5                ; (-0bh)
        di
        sub     a
        out     (10h),a
        ld      a,0e5h
        out     (11h),a
        ld      b,0ffh
l13ba:  call    l13f3
        bit     6,a
        jr      nz,l13c9                ; (+08h)
        djnz    l13ba                   ; (-09h)
        jr      l1356                   ; (-6fh)
l13c5:  djnz    l13a5                   ; (-22h)
        jr      l1356                   ; (-73h)
l13c9:  sub     a
        out     (10h),a
        ld      a,0a7h
        out     (11h),a
        ld      c,11h
l13d2:  ld      b,28h
l13d4:  ld      a,04h
        out     (10h),a
        in      a,(11h)
        bit     1,a
        jr      nz,l13e6                ; (+08h)
        djnz    l13d4                   ; (-0ch)
        ld      a,01h
        ld      (qTRKS+4),a
        ret

l13e6:  ld      a,06h
        out     (10h),a
        ini
        dec     de
        ld      a,e
        or      d
        jr      nz,l13d2                ; (-1fh)
        ei
        ret

l13f3:  ld      a,04h
        out     (10h),a
        in      a,(11h)
        ret

        ld      c,c
        ld      d,a
        ld      d,e
        call    l10f6
