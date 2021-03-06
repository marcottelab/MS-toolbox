#!/usr/bin/env python
import os
import sys
import stat
import mstb_helper as helper

usage_mesg = 'Usage: prepare-mzxml_gz2mgf.py'

MSTB_HOME = helper.get_mstb_home()
CWD = helper.get_cwd()

conf = helper.read_conf( os.path.join(CWD,'mstb.conf') )
if( len(conf) == 0 ):
    sys.exit(1)

helper.check_conf_file(conf,'PATH_MSCONVERT')

filename_sh = os.path.join(CWD,'scripts','run-mzxml_gz2mgf.sh')
f_sh = open(filename_sh,'w')
f_sh.write('#!/bin/bash\n')
for basename_mzxml in helper.get_mzxml_list():
    filename_base = basename_mzxml.replace('.mzXML.gz','')
    filename_mzxml = os.path.join(CWD,'mzXML',basename_mzxml)
    f_sh.write('%s %s -z -o mgf\n'%(conf['PATH_MSCONVERT'],filename_mzxml))
f_sh.close()

os.chmod(filename_sh,stat.S_IRWXU)
sys.stderr.write('\nmzXML.gz-to-mgf is ready. Run %s.\n\n'%(filename_sh))
