"""Module to specify a list of loadable programs"""

# New abstraction to make it possible to load different roms and/or
# custom code snippets into memory with a user defined start address

import progs.jdc
import progs.misc
import progs.peeldk

proglist = {
        "peeldk"   : progs.peeldk.peeldk,
        "iws"      : progs.peeldk.iws,
        "jdc"      : progs.jdc.jdc,
        "dummy"    : progs.misc.dummy,
        "loop"     : progs.misc.loop,
        "todec"    : progs.misc.todec,
        "emucrash" : progs.misc.emucrash
    }
