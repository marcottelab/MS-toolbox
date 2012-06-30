#!/usr/bin/python
import os
import sys
import time

import mstb_helper as helper

DIR_LIST = ['DB','RAW','mzXML','tmp','scripts']
#ENGINE_LIST = ['sequest','inspect','tandem','tandemK','omssa','myrimatch','MSGFDB']

MSTB_HOME = helper.get_mstb_home()
CWD = helper.get_cwd()

for tmp_dir in DIR_LIST:
    tmp_path = os.path.join(CWD,tmp_dir)
    if( os.access(tmp_path, os.R_OK) ):
        sys.stderr.write("Skip %s. Already exists.\n"%(tmp_path))
    else:
        sys.stderr.write("Create %s.\n"%(tmp_path))
        os.mkdir(tmp_path)
sys.stderr.write("\n")

cparams = dict()

cparams['DB_NAME'] = os.path.join(CWD,'DB','your_db')
cparams['DB_FASTA'] = os.path.join(CWD,'DB','your_db.fa')
cparams['DB_FASTAPRO'] = os.path.join(CWD,'DB','your_db.fa.pro')
cparams['DB_TRIE'] = os.path.join(CWD,'DB','your_db.fa.trie')
cparams['DB_BLASTDB'] = os.path.join(CWD,'DB','your_db.fa')
cparams['DB_DECOY_PREFIX'] = 'rv_'

cparams['PATH_TPP'] = '/usr/local/tpp'
cparams['PATH_XINTERACT'] = '/usr/local/tpp/bin/xinteract'
cparams['PATH_MSCONVERT'] = '/usr/local/bin/msconvert'

cparams['PATH_TANDEMK_EXE'] = '/usr/local/tpp/bin/tandem.exe'
cparams['PATH_TANDEM2XML'] = '/usr/local/tpp/bin/Tandem2XML'
cparams['PATH_TANDEMK_DEFAULT_PARAM'] = '/usr/local/tpp/bin/isb_default_input_kscore.xml'

cparams['PATH_OMSSACL'] = '/usr/local/bin/omssacl'
cparams['PATH_INSPECT'] = '/usr/local/bin/inspect'
cparams['PATH_MSGFDB_JAR'] = '/usr/local/src/MSGFDB/current.jar'
cparams['PATH_CRUX'] = '/usr/local/bin/crux'
cparams['PATH_TIDE'] = '/usr/local/bin/tide'

for filename_db in os.listdir( os.path.join(CWD,'DB') ):
    if( filename_db.endswith('.fa') or filename_db.endswith('.fasta') ):
        cparams['DB_FASTA'] = os.path.join(CWD,'DB',filename_db)
        cparams['DB_NAME'] = filename_db.replace('.fa','').replace('.fasta','')
        sys.stderr.write('DB name = %s\n'%cparams['DB_NAME'])

    if( filename_db.endswith('.pro') ):
        cparams['DB_FASTAPRO'] = os.path.join(CWD,'DB',filename_db)

    if( filename_db.endswith('.pin') ):
        cparams['DB_BLASTDB'] = os.path.join(CWD,'DB',filename_db.replace('.pin',''))
    if( filename_db.endswith('.trie') ):
        cparams['DB_TRIE'] = os.path.join(CWD,'DB',filename_db)

filename_conf_src = os.path.join(MSTB_HOME,'tmpl','mstb.conf')
filename_conf_dest = os.path.join(CWD,'mstb.conf') 

if( os.access(filename_conf_dest, os.F_OK) ):
    filename_conf_dest_old = os.path.join(CWD,'mstb.conf.%s'%(time.strftime("%Y%b%d_%H%M%S")))
    sys.stderr.write('%s exists.\n===> %s\n\n'%(filename_conf_dest, filename_conf_dest_old))
    os.rename(filename_conf_dest, filename_conf_dest_old)
    f_conf_dest_old = open(filename_conf_dest_old,'r')
    for line in f_conf_dest_old:
        tokens = line.strip().split()
        if( len(tokens) > 1 ):
            cparams[tokens[0]] = tokens[1]
    f_conf_dest_old.close()

f_conf_src = open(filename_conf_src,'r')
conf_tmpl = ''.join( f_conf_src.readlines() )
f_conf_src.close()

sys.stderr.write('Write %s.\n\n'%filename_conf_dest)
f_conf_dest = open(filename_conf_dest,'w')
f_conf_dest.write(conf_tmpl.format(**cparams))
f_conf_dest.close()
