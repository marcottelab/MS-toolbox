#!/usr/bin/python
import os
import sys
import shutil

DIR_LIST = ['DB','RAW','mzXML','mgf','tmp']
ENGINE_LIST = ['sequest','inspect','tandem','tandemK','omssa','myrimatch','MSGFDB']

MSTB_HOME = sys.path[0]
CWD = os.getcwd()

for tmp_dir in DIR_LIST:
    tmp_path = os.path.join(CWD,tmp_dir)
    if( os.access(tmp_path, os.R_OK) ):
        sys.stderr.write("%s exists. Skip.\n"%(tmp_path))
    else:
        sys.stderr.write("%s does not exist. Create.\n"%(tmp_path))
        os.mkdir(tmp_path)

shutil.copy( os.path.join(MSTB_HOME,'..','tmpl','mstb.conf'), os.path.join(CWD,'mstb.conf') )
