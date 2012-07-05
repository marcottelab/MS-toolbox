#!/usr/bin/env python
import os
import sys

usage_mesg = 'Usage: pepxml-setdb.py <db fasta file>'

if( len(sys.argv) != 2 ):
    sys.stderr.write('%s\n'%usage_mesg)
    sys.exit(1)

filename_fasta = sys.argv[1] 
if( not os.access(filename_fasta,os.R_OK) ):
    sys.stderr.write('%s is not available.\n'%filename_fasta)
    sys.stderr.write('%s\n'%usage_mesg)
    sys.exit(1)
filename_fasta = os.path.abspath(filename_fasta)

for basename_pepxml in os.listdir('.'):
    if( not basename_pepxml.endswith('.pepxml') ):
        continue

    basename_pepxml_old = '__old__%s'%basename_pepxml
    os.rename(basename_pepxml, basename_pepxml_old)

    sys.stderr.write('Process %s ... '%basename_pepxml)
    f_old = open(basename_pepxml_old,'r')
    f_new = open(basename_pepxml,'w')
    for line in f_old:
        line = line.strip()
        if( line.startswith('<search_database local_path="') ):
            f_new.write('<search_database local_path="%s" type="AA"/>\n'%filename_fasta)
        elif( line.startswith('<parameter name="list path, sequence source #1" value"') ):
            f_new.write('<parameter name="list path, sequence source #1" value="%s"/>\n'%filename_fasta)
        elif( line.startswith('<parameter name="first_database_name" value"') ):
            f_new.write('<parameter name="first_database_name" value="%s"/>\n'%filename_fasta)
        else:
            f_new.write('%s\n'%line)
    f_new.close()
    f_old.close()
    sys.stderr.write('Done\n')
