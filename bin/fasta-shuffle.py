#!/usr/bin/python 
import sys
import os
import random

usage_mesg = 'Usage: fasta-shuffle.py <fasta file>'

if( len(sys.argv) != 2 ):
    sys.stderr.write('Error! Invalide argument.\n%s\n'%(usage_mesg))
    sys.exit(1)

filename_fasta = sys.argv[1]
if( not os.access(filename_fasta,os.R_OK) ):
    sys.stderr.write("%s is not accessible.\n%s\n"%(filename_fasta,usage_mesg))
    sys.exit(1)

f_fasta = open(filename_fasta,'r')
header = ''
seq = dict()
for line in f_fasta:
    if(line.startswith('>')):
        header = line.strip().lstrip('>').split()[0]
        seq[header] = ''
    else:
        seq[header] += line.strip()
f_fasta.close()

f_target = open("%s.target"%filename_fasta,'w')
f_shuffle = open("%s.shuffle"%filename_fasta,'w')
f_shuffle_inspect = open("%s.shuffle_inspect"%filename_fasta,'w')
for h in seq.keys():
    seq_list = list(seq[h])
    random.shuffle(seq_list)
    random_seq = ''.join(seq_list)

    f_shuffle.write(">xf_%s\n%s\n"%(h,random_seq))
    f_shuffle_inspect.write(">XXX.%s\n%s\n"%(h,random_seq))
    f_target.write(">%s\n%s\n"%(h,seq[h]))
f_shuffle_inspect.close()
f_shuffle.close()
f_target.close()
