# New abstraction to make it possible to load different roms and/or
# custom code snippets into memory with a user defined start address

import progs.jdc, progs.peeldk, progs.misc

proglist = {
        "peeldk"   : progs.peeldk.peeldk,
        "iws"      : progs.peeldk.iws,
        "jdc"      : progs.jdc.jdc,
        "dummy"    : progs.misc.dummy,
        "loop"     : progs.misc.loop,
        "todec"    : progs.misc.todec,
        "emucrash" : progs.misc.emucrash
    }
