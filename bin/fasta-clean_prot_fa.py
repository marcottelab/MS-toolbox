#!/usr/bin/env python
import os
import sys
import re

filename_fa = sys.argv[1]

seq_list = dict()
seq_h = ''
f_fa = open(filename_fa,'r')
for line in f_fa:
    if( line.startswith('>') ):
        seq_h = line.strip()
        seq_list[seq_h] = []
    else:
        seq_list[seq_h].append( line.strip() )
f_fa.close()

sys.stderr.write('Write .clean_log and .clean_fa for %s ... '%filename_fa)
f_log = open('%s.clean_log'%filename_fa,'w')
f_out = open('%s.clean_fa'%filename_fa,'w')
for seq_h in sorted(seq_list.keys()):
    tmp_seq = ''.join(seq_list[seq_h])
    if( re.search(r'[BJOUXZ]',tmp_seq) != None ):
        f_log.write('%s,%s\n'%(seq_h, ','.join(re.findall(r'[BJOUXZ]',tmp_seq))))
    else:
        f_out.write('%s\n%s\n'%(seq_h,tmp_seq))
f_log.close()
f_out.close()
sys.stderr.write('Done\n')
