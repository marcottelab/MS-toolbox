#!/usr/bin/env python 
import os
import sys
import stat
import mstb_helper as helper

usage_mesg = 'Usage: prepare-sequest-TPP.py'

dirname = 'sequest'

MSTB_HOME = helper.get_mstb_home()
CWD = helper.get_cwd()

conf = helper.read_conf( os.path.join(CWD,'mstb.conf') )
if( len(conf) == 0 ):
    sys.exit(1)

helper.check_conf_file(conf,'PATH_XINTERACT')
helper.check_conf_term(conf,'DB_DECOY_PREFIX')

sample_list = dict()
for basename_pepxml in os.listdir(dirname):
    if( not basename_pepxml.endswith('.pepxml') ):
        continue
    sample_name = '_'.join( basename_pepxml.split('_')[1:3])
    if( not sample_list.has_key(sample_name) ):
        sample_list[sample_name] = []
    sample_list[sample_name].append( os.path.join(CWD,dirname,basename_pepxml) )

filename_sh = os.path.join(CWD,'scripts','run-sequest-TPP.sh')
f_sh = open(filename_sh,'w')
f_sh.write('#!/bin/bash\n')

dirname_tmp = os.path.join(CWD,'tmp')
f_sh.write('rm %s\n'%( os.path.join(dirname_tmp,'*') ))
for sample_name in sample_list.keys():
    f_sh.write('echo "Process Sample %s"\n'%(sample_name))
    for filename_pepxml in sample_list[sample_name]:
        f_sh.write('cp %s %s\n'%(filename_pepxml,dirname_tmp))

    filename_xinteract = os.path.join(CWD,dirname,'%s.xinteract.xml'%sample_name)
    f_sh.write('%s -N%s -Op -d%s tmp/*.pepxml\n'%(conf['PATH_XINTERACT'],filename_xinteract,conf['DB_DECOY_PREFIX']))
    f_sh.write('rm %s\n'%( os.path.join(dirname_tmp,'*') ))
f_sh.close()

os.chmod(filename_sh,stat.S_IRWXU)
sys.stderr.write('\nTandemK-TPP is ready. Run %s.\n\n'%(filename_sh))
