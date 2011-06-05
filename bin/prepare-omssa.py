#!/usr/bin/python
import os
import sys
import stat
import mstb_helper as helper

usage_mesg = 'Usage: prepare-omssa.py'

dirname = 'omssa'

MSTB_HOME = helper.get_mstb_home()
CWD = helper.get_cwd()

conf = helper.read_conf( os.path.join(CWD,'mstb.conf') )
if( len(conf) == 0 ):
    sys.exit(1)

helper.check_conf_term(conf,'DB_NAME')
helper.check_conf_file(conf,'PATH_OMSSACL')

path_dir = os.path.join(CWD,dirname)
if( not os.access(path_dir,os.R_OK) ):
    sys.stderr.write("Create %s.\n"%(path_dir))
    os.mkdir(path_dir)

if( not os.path.isdir(path_dir) ):
    sys.stderr.write('\n%s is not a directory.\n'%path_dir)
    sys.stderr.write('Rename it and make %s directory.\n\n'%path_dir)
    sys.exit(1)

filename_cmd_tmpl = os.path.join(MSTB_HOME,'tmpl','omssa.cmd')
f_cmd_tmpl = open(filename_cmd_tmpl,'r')
cmd_tmpl = ''.join( f_cmd_tmpl.readlines() )
f_cmd_tmpl.close()

filename_sh = os.path.join(CWD,'scripts','run-omssa.sh')
f_sh = open(filename_sh,'w')
f_sh.write('#!/bin/bash\n')
for basename_mgf in helper.get_mgf_list():
    filename_base = basename_mgf.replace('.mgf','')

    in_params = dict()
    in_params['PATH_OMSSACL'] = conf['PATH_OMSSACL']
    in_params['DB_BLASTDB'] = conf['DB_BLASTDB']
    in_params['FILENAME_MGF'] = os.path.join(CWD,'mgf',basename_mgf)
    in_params['FILENAME_PEPXML'] = os.path.join(CWD,dirname,'%s.omssa.pepxml'%filename_base)
    f_sh.write( cmd_tmpl.format(**in_params) )
f_sh.close()

os.chmod(filename_sh,stat.S_IRWXU)
sys.stderr.write('\nOMSSA is ready. Run %s.\n\n'%(filename_sh))
