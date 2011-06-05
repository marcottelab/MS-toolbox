#!/usr/bin/python
import os
import sys
import stat
import mstb_helper as helper

usage_mesg = 'Usage: prepare-mgf2ms2.py'

MSTB_HOME = helper.get_mstb_home()
CWD = helper.get_cwd()

conf = helper.read_conf( os.path.join(CWD,'mstb.conf') )
if( len(conf) == 0 ):
    sys.exit(1)

helper.check_conf_file(conf,'PATH_MSCONVERT')

filename_sh = os.path.join(CWD,'scripts','run-mgf2ms2.sh')
f_sh = open(filename_sh,'w')
f_sh.write('#!/bin/bash\n')
for basename_mgf in helper.get_mgf_list():
    filename_base = basename_mgf.replace('.mgf','')
    filename_mgf = os.path.join(CWD,'mgf',basename_mgf)
    filename_ms2 = os.path.join(CWD,'ms2',filename_base+'.ms2')
    f_sh.write('%s --ms2 %s -o ms2\n'%(conf['PATH_MSCONVERT'],filename_mgf))
f_sh.close()

os.chmod(filename_sh,stat.S_IRWXU)
sys.stderr.write('\nMGF-to-MS2 is ready. Run %s.\n\n'%(filename_sh))
