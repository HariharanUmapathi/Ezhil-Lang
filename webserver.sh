#!/bin/bash -x
#pushd web
# Old Relative path method not working
#python3 ../ezhil/EZWeb.py
# following invocation works with relative paths without switching director
python3 -m ezhil.EZWeb
#popd
