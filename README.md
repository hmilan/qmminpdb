# qmminpdb

Converts output of some ab intio QM programs into a file in the PDB format.
Currently understands GAMESS & Gaussian (limited tests with g09, g16) as input.  It produces PDB
file by default but one can specify also xyz format, mainly for more
accuracy, because PDB has only 3 digits after decimal point.

For a QM minimization file it produces a file which is ready for the animation
in the VMD program!

Running the program without any parameters gives a short usage.

The following produces some more info

qmminpdb.py --help 



