# qmminpdb

Converts output of some ab intio QM programs into a file in PDB format
Currently understands GAMESS & Gaussian as input.  It produces PDB
file by default but one can specify also xyz format, mainly for more
accuracy, because PDB has only 3 digits after decimal point.

For QM minimization file it makes a file which is ready for animation
in VMD program!

Running the program without any parameters gives a short usage.

The following produces some more info

qmminpdb.py --help 



