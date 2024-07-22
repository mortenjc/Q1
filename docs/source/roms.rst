
.. ROMS:

ROM Images
==========

Three sets of ROM images are currently available

.. list-table:: ROMs
   :header-rows: 1

   * - Name
     - Roms
     - IC Description
   * - JDC
     - IC25 - IC32
     - From danish vendor JDC
   * - IWS
     - IC25 - IC29, IC31, IC32
     - From a model with serial number 820
   * - Hybrid
     - IC25 - IC27, IC31, IC32
     - Mix of ROMs from serial numbers 615 and 580

Since I have mainly worked with the JDC ROMs, these are the only ones
that have annotation data in their **program** structures.

Memory
======

The ROS User's Manual, figure 1 on page 5, shows the memory
layout.


For the JDC ROM image some of this information seems correct,
but the address range 0x1000 to 0x17ff is marked as unused.
However there is assembler code in this region seemingly
related to disk reads.
