#!/usr/bin/python
import os
import sys
import stat
import mstb_helper as helper

usage_mesg = 'Usage: prepare-MSGFDB.py'

dirname = 'MSGFDB'

MSTB_HOME = helper.get_mstb_home()
CWD = helper.get_cwd()

conf = helper.read_conf( os.path.join(CWD,'mstb.conf') )
if( len(conf) == 0 ):
    sys.exit(1)

helper.check_conf_file(conf,'DB_FASTA')
helper.check_conf_file(conf,'PATH_MSGFDB_JAR')

path_dir = os.path.join(CWD,dirname)
if( not os.access(path_dir,os.R_OK) ):
    sys.stderr.write("Create %s.\n"%(path_dir))
    os.mkdir(path_dir)

if( not os.path.isdir(path_dir) ):
    sys.stderr.write('\n%s is not a directory.\n'%path_dir)
    sys.stderr.write('Rename it and make %s directory.\n\n'%path_dir)
    sys.exit(1)

filename_cmd_tmpl = os.path.join(MSTB_HOME,'tmpl','MSGFDB.cmd')
f_cmd_tmpl = open(filename_cmd_tmpl,'r')
cmd_tmpl = ''.join( f_cmd_tmpl.readlines() )
f_cmd_tmpl.close()

filename_sh = os.path.join(CWD,'scripts','run-MSGFDB.sh')
f_sh = open(filename_sh,'w')
f_sh.write('#!/bin/bash\n')
for basename_mzXML in helper.get_mzxml_list():
    filename_base = basename_mzXML.replace('.mzXML','')
    sys.stderr.write('%s\n'%basename_mzXML)

    in_params = dict()
    in_params['PATH_MSGFDB_JAR'] = conf['PATH_MSGFDB_JAR']
    in_params['DB_FASTA'] = conf['DB_FASTA']
    in_params['FILENAME_MZXML'] = os.path.join(CWD,'mzXML',basename_mzXML)
    in_params['FILENAME_OUT'] = os.path.join(CWD,dirname,'%s.MSGFDB_out'%filename_base)
    f_sh.write( cmd_tmpl.format(**in_params) )
f_sh.close()

os.chmod(filename_sh,stat.S_IRWXU)
sys.stderr.write('\nMSGFDB is ready. Run %s.\n\n'%(filename_sh))
