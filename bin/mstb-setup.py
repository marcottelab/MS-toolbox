#!/usr/bin/python
import os
import sys
import time

DIR_LIST = ['DB','RAW','mzXML','mgf','tmp','scripts']
ENGINE_LIST = ['sequest','inspect','tandem','tandemK','omssa','myrimatch','MSGFDB']

MSTB_HOME = os.path.join(sys.path[0],'..')
CWD = os.getcwd()

for tmp_dir in DIR_LIST:
    tmp_path = os.path.join(CWD,tmp_dir)
    if( os.access(tmp_path, os.R_OK) ):
        sys.stderr.write("Skip %s. Already exists.\n"%(tmp_path))
    else:
        sys.stderr.write("Create %s.\n"%(tmp_path))
        os.mkdir(tmp_path)

cparams = dict()
cparams['PATH_TPP'] = '/usr/local/tpp'
cparams['PATH_MSCONVERT'] = '/usr/local/bin/msconvert'
cparams['PATH_INSPECT'] = '/usr/local/src/inspect/current/'
cparams['PATH_MSGFDB_JAR'] = '/usr/local/src/MSGFDB/current.jar'
cparams['PATH_FASTAPRO_EXE'] = '/usr/local/bin/fastapro.exe'

cparams['DB_FASTA'] = os.path.join(CWD,'DB','your_db.fa')
cparams['DB_FASTAPRO'] = os.path.join(CWD,'DB','your_db.fa.pro')
cparams['DB_TRIE'] = os.path.join(CWD,'DB','your_db.fa.trie')
cparams['DB_FORMATDB'] = os.path.join(CWD,'DB','your_db.fa')

for filename_db in os.listdir( os.path.join(CWD,'DB') ):
    if( filename_db.endswith('.pro') ):
        cparams['DB_FASTAPRO'] = os.path.join(CWD,'DB',filename_db)
    if( filename_db.endswith('.fa') or filename_db.endswith('.fasta') ):
        cparams['DB_FASTA'] = os.path.join(CWD,'DB',filename_db)
    if( filename_db.endswith('.psq') ):
        cparams['DB_FORMATDB'] = os.path.join(CWD,'DB',filename_db.replace('.psq',''))
    if( filename_db.endswith('.trie') ):
        cparams['DB_TRIE'] = os.path.join(CWD,'DB',filename_db)

filename_conf_src = os.path.join(MSTB_HOME,'tmpl','mstb.conf')
filename_conf_dest = os.path.join(CWD,'mstb.conf') 

if( os.access(filename_conf_dest, os.F_OK) ):
    filename_conf_dest_old = os.path.join(CWD,'mstb.conf.%s'%(time.strftime("%Y%b%d_%H%M%S")))
    sys.stderr.write('%s exists.\n===> %s\n'%(filename_conf_dest, filename_conf_dest_old))
    os.rename(filename_conf_dest, filename_conf_dest_old)
    f_conf_dest_old = open(filename_conf_dest_old,'r')
    for line in f_conf_dest_old:
        tokens = line.strip().split()
        if( len(tokens) > 2 ):
            cparams[tokens[0]] = tokens[1]
    f_conf_dest_old.close()

f_conf_src = open(filename_conf_src,'r')
conf_tmpl = ''.join( f_conf_src.readlines() )
f_conf_src.close()

f_conf_dest = open(filename_conf_dest,'w')
f_conf_dest.write(conf_tmpl.format(**cparams))
f_conf_dest.close()
