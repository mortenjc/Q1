# New abstraction to make it possible to load different roms and/or
# custom code snippets into memory with a user defined start address

import progs_jdc, progs_peeldk, progs_misc

proglist = {
        "peeldk"   : progs_peeldk.peeldk,
        "iws"      : progs_peeldk.iws,
        "jdc"      : progs_jdc.jdc,
        "dummy"    : progs_misc.dummy,
        "loop"     : progs_misc.loop,
        "todec"    : progs_misc.todec,
        "emucrash" : progs_misc.emucrash
    }
