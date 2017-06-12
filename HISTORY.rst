* Write about 

- similar programs (test them...)

a) molden works & shows the history of ab initio calculations but at
   some point it didn't work for me and I started this little script
   to convert g09 output into PDB file format to be shown by VMD
   
b) openbabel
   works but does not keep atom names, and only one structure is in
   the file
   
- why this program exist

a) simplicity
   because of the past molden problems and because python script was
   easy to make

b) control
   if some new need shows up I can just simply add it to the script
   
c) se below for special features

- special fetures

a) support for QM/MM output files
   this scripts supports the gamess output file produced by
   CHARMM/GAMESS interface (http://charmm.org)
   molden only shows the first structure and not all of them that are
   in the file.

