if [ ! -f {FILENAME_OUT} ] && [ ! -f {FILENAME_OUT}.inprog ]; then touch {FILENAME_OUT}.inprog; {PATH_INSPECT} -r {DIR_INSPECT} -i {FILENAME_IN} -o {FILENAME_OUT}; fi
