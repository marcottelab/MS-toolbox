#!/usr/bin/python
import os
import sys
import stat
import mstb_helper as helper

usage_mesg = 'Usage: prepare-tandemK.py'

dirname = 'tandemK'
filename_taxon_xml = 'tandem-taxonomy.xml'

MSTB_HOME = helper.get_mstb_home()
CWD = helper.get_cwd()

conf = helper.read_conf( os.path.join(CWD,'mstb.conf') )
if( len(conf) == 0 ):
    sys.exit(1)

helper.check_conf_term(conf,'DB_NAME')
helper.check_conf_file(conf,'DB_FASTAPRO')
helper.check_conf_file(conf,'PATH_TANDEMK_EXE')
helper.check_conf_file(conf,'PATH_TANDEM2XML')
helper.check_conf_file(conf,'PATH_TANDEMK_DEFAULT_PARAM')

path_dir = os.path.join(CWD,dirname)
if( not os.access(path_dir,os.R_OK) ):
    sys.stderr.write("Create %s.\n"%(path_dir))
    os.mkdir(path_dir)

if( not os.path.isdir(path_dir) ):
    sys.stderr.write('\n%s is not a directory.\n'%path_dir)
    sys.stderr.write('Rename it and make %s directory.\n\n'%path_dir)
    sys.exit(1)

filename_taxon_tmpl = os.path.join(MSTB_HOME,'tmpl',filename_taxon_xml)
f_taxon_tmpl = open(filename_taxon_tmpl,'r')
taxon_tmpl = ''.join( f_taxon_tmpl.readlines() )
f_taxon_tmpl.close()

filename_taxon = os.path.join(CWD,dirname,filename_taxon_xml)
sys.stderr.write('Write %s.\n'%filename_taxon)
f_taxon = open(filename_taxon,'w')
f_taxon.write( taxon_tmpl.format(DB_FASTAPRO=conf['DB_FASTAPRO'], DB_NAME=conf['DB_NAME']) )
f_taxon.close()

filename_in_tmpl = os.path.join(MSTB_HOME,'tmpl','tandemK.xml')
f_in_tmpl = open(filename_in_tmpl,'r')
in_tmpl = ''.join( f_in_tmpl.readlines() )
f_in_tmpl.close()

filename_sh = os.path.join(CWD,'scripts','run-tandemK.sh')
f_sh = open(filename_sh,'w')
f_sh.write('#!/bin/bash\n')
for basename_mzxml in helper.get_mzxml_list():
    filename_base = basename_mzxml.replace('.mzXML','')
    filename_in = os.path.join(CWD,dirname,'%s.tandemK.xml'%filename_base)

    in_params = dict()
    in_params['DB_NAME'] = conf['DB_NAME']
    in_params['TANDEMK_DEFAULT_PARAM'] = conf['PATH_TANDEMK_DEFAULT_PARAM']
    in_params['FILENAME_TAXON'] = filename_taxon
    in_params['FILENAME_MZXML'] = os.path.join(CWD,'mzXML',basename_mzxml)
    filename_out = os.path.join(CWD,dirname,'%s.tandemK.out'%filename_base)
    in_params['FILENAME_OUT'] = filename_out
    in_params['FILENAME_LOG'] = os.path.join(CWD,dirname,'%s.tandemK.log'%filename_base)

    filename_pepxml = os.path.join(CWD,dirname,'%s.tandemK.pepxml'%filename_base)
    
    sys.stderr.write('Write %s.\n'%filename_in)
    f_in = open(filename_in,'w')
    f_in.write( in_tmpl.format(**in_params) )
    f_in.close()
    
    f_sh.write("%s %s\n"%(conf['PATH_TANDEMK_EXE'], filename_in))
    f_sh.write('%s %s %s\n'%(conf['PATH_TANDEM2XML'], filename_out, filename_pepxml))
    f_sh.write('gzip %s\n'%(filename_out))
f_sh.close()

os.chmod(filename_sh,stat.S_IRWXU)
sys.stderr.write('\nTandemK is ready. Run %s.\n\n'%(filename_sh))
