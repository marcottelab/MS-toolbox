import os
import sys

def get_mstb_home():
    return os.path.join(sys.path[0],'..')

def get_cwd():
    return os.getcwd()

def check_conf_term(tmp_conf, tmp_term):
    if( not tmp_conf.has_key(tmp_term) ):
        sys.stderr.write('%s is not set. Set it on mstb.conf\n'%tmp_term)
        sys.exit(1)
    
def check_conf_file(tmp_conf, tmp_term):
    check_conf_term(tmp_conf, tmp_term)
    if( not os.access(tmp_conf[tmp_term], os.R_OK) ):
        sys.stderr.write('%s %s is not available.\n'%(tmp_term, tmp_conf[tmp_term]))
        sys.exit(1)

def read_conf(filename):
    rv = dict()
    if( not os.access(filename,os.R_OK) ):
        sys.stderr.write('%s is not available.\nRun mstb-setup.py first.\n'%(filename))
        return rv

    f = open(filename,'r')
    for line in f:
        if( line.startswith('#') ):
            continue
        tokens = line.strip().split()
        if( len(tokens) > 1 ):
            rv[ tokens[0] ] = tokens[1]
    f.close()
    return rv

def get_mgf_list():
    rv = []
    for line in os.listdir('mgf'):
        if( line.endswith('.mgf') ):
            rv.append( line.strip() )
    return rv

def get_mzxml_list():
    rv = []
    for line in os.listdir('mzXML'):
        if( line.endswith('.mzXML.gz') ):
            rv.append( line.strip() )
    return rv
