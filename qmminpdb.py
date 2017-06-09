#! /usr/bin/python3

import argparse,sys,os,textwrap

'''

to make 3.5 version use try on parser.parse_args() and then spit usage

As of February 7, 2017 this is good for Gaussian (g09) & GAMESS
It recognizes the format of the individual programs automatically
No need for extra input format command line flags! For now - what about future??

What about the rest - do they need the input format flags ?
NWChem, QChem, TurboMole, jaguar, ... ???

QChem:
1. ??
2. is it different when in CHARMM/QChem ?

jaguar:
1. Do we need this one ??

TurbMole:
1. ??

NWChem:
1. This one is next.... for version 4.0

GAMESS:
1. internal minimization -
   (problem with molden when big numbers: 123.0000-2222.500)
2. CHARMM/GAMESS runs OK with this program:
   molden always takes the first frame only from QM/MM gamess output

G09:
1. basic stuff seems OK
2. not every possible g09 output is tested yet
3. what about g16 ?

'''

# functions:

def wpdb(outf,natom,a,x,y,z):
    for i in range(natom):
        outf.write('HETATM{0:5d} {1:4s} LIG L   1    '.format(i+1,a[i]))
        outf.write('{0:8.3f}{1:8.3f}{2:8.3f}  1.00  0.00           {3:s}\n'
            .format(x[i],y[i],z[i],a[i][0]))
    outf.write('END\n')

def wxyz(outf,natom,a,x,y,z):
    for i in range(natom):
        outf.write('{0:4s} {1:18.10f}{2:18.10f}{3:18.10f}\n'.format(
            a[i],x[i],y[i],z[i]))


# parsing the command line
# do some more error checking here !!! If there are no paramters for example!
# in the no parameter case try to spit usage! = version 3.5

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent('''
        Converts output of QM (GAMESS/Gaussian/...) programs into a file in PDB format.
        For QM minimization file it makes a pdb file
        ready for animation in VMD'''))
parser.add_argument(
    'input_file',  help='Specify QM output file as input here',
    #nargs='?',
    default=sys.stdin,
    type=argparse.FileType(mode='rt',encoding='utf-8'))
parser.add_argument(
    'output_file',  help='Name of a coordinate file (PDB[default], XYZ,...)', nargs='?',
    default=sys.stdout,type=argparse.FileType(mode='wt',encoding='utf-8'))
parser.add_argument(
    '-x','--xyz', help='write XYZ format instead of PDB', action='store_true')
parser.add_argument(
    '-v','--version', help='print a version number', action='version',
    version='%(prog)s 3.0 (February 12, 2017)')
parser.add_argument(
    '-l','--license', help='print a license', action='store_true')
parser.add_argument(
    '--todo', help='print TODO items', action='store_true')
args = parser.parse_args()
if args.license:
    print("This program is licensed as GPL version 2 or later")
    exit(0)
if args.todo:
    print("Make more input formats: NWChem is next")
    print("What about: QChem, TurboMole, ")
    exit(0)


# END parsing command line; start reading input file

inpf = args.input_file ; outf = args.output_file
pdb = not args.xyz

a=[] ; ff=False ; ffchk=False ; gms=False
for line in inpf:
    if line.find('Z-Matrix taken from the checkpoint file:') > 0 : ffchk = True
    if line.find('Symbolic Z-matrix:') > 0 :
        ff = True
        line=inpf.readline()
        line=inpf.readline()
        while line.find('Charge = ') > 0 : line=inpf.readline()
    # adding stuff for GAMESS here:
    if line.find('COORDINATES (BOHR)') > 0 :
        line=inpf.readline();line=inpf.readline()
        ff=True ; gms=True
    # end of GAMESS addition
    if len(line.split()) > 0 : kw=line.split()[0]
    if (kw == 'Variables:') or (kw == 'Recover') : break
    if (len(line.split()) == 0) and ff : break
    if (not (line.find(',') > 0) ) and ffchk : continue
    xp=kw.find('(')
    if xp > 0 : kw = kw[:xp]
    if ff: a.append(kw.upper())
    if ffchk: a.append(kw.split(',')[0].upper())


natom=len(a) ; frame=0 ; noene = True
x=natom*[0.0] ; y=natom*[0.0] ; z=natom*[0.0]

# DEBUG section:
#print('G09 or GAMESS');print('natom=',natom);print('names=',a)
#exit(0)

# the following 3 lines keep the 'for loop' below good for both G09 & GAMESS
lskip=4 ; loffset=0 ; au = 1.0 ; angs=False
if gms :
    lskip=1;loffset=1;au=0.529177249

for line in inpf:
    if (line.find('Z-Matrix orientation:') > 0 ) \
       or (line.find('Input orientation:') > 0 ) \
       or (line.find('Standard orientation:') > 0 ) \
       or (line.find('COORDINATES (BOHR)') > 0 ) \
       or (line.find('(ANGS)') > 0 ) :
        if (line.find('(ANGS)') > 0 ) :  # For GAMESS minimizations...
            angs=True ; inpf.readline()
        for i in range(lskip): inpf.readline()
        for i in range(natom):
            line=inpf.readline()
            # if not opt=z-matrix, remove 'X's
            if line[1:5] == '----' :
                for j in range(natom-i): a.remove('X')
                natom = i ; break
            if angs :
                x[i]=float(line[16:31])  # good for GAMESS with big numbers
                y[i]=float(line[31:46])
                z[i]=float(line[46:61])
            else :
                x[i]=float(line.split()[3-loffset])*au
                y[i]=float(line.split()[4-loffset])*au
                z[i]=float(line.split()[5-loffset])*au

    if (line.find('Done') > 0) or (line.find('FINAL') > 0) :
        e=float(line.split()[4])
        if pdb: 
            outf.write('REMARK ENERGY={0:20.10f} FRAME={1:d}\n'.format(e,frame))
        else:
            outf.write('{0:10d}\n'.format(natom))
            outf.write('Energy={0:20.10f} Frame={1:d}\n'.format(e,frame))
        frame += 1 ; noene = False
        if pdb:
            wpdb(outf,natom,a,x,y,z)
        else:
            wxyz(outf,natom,a,x,y,z)


if noene:
    if pdb:
        wpdb(outf,natom,a,x,y,z)
    else:
        wxyz(outf,natom,a,x,y,z)
