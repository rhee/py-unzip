#!/usr/bin/env python

# copied from http://stackoverflow.com/a/14981125/496899
from __future__ import print_function
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# copied from http://stackoverflow.com/a/12886818/496899
import zipfile,os.path

def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        zf.debug = 3
        if False: ### if sys.version_info >= (2, 7, 4):
            # if python 2.7.4+, safe to use 'extractall'
            zf.extractall(dest_dir)  
        else:
            # iterate to avoid '..' security issue
            for member in zf.infolist():
                # Path traversal defense copied from
                # http://hg.python.org/cpython/file/tip/Lib/http/server.py#l789
                words = member.filename.split('/')
                path = dest_dir
                for word in words[:-1]:
                    drive, word = os.path.splitdrive(word)
                    head, word = os.path.split(word)
                    if word in (os.curdir, os.pardir, ''): continue
                    path = os.path.join(path, word)
                if not member.filename.endswith('/'):
                    eprint(member.filename)
                zf.extract(member, path)

if __name__ == '__main__':
    import sys
    if len(sys.argv)>2:
        unzip(sys.argv[1],sys.argv[2])
    else:
        unzip(sys.argv[1],'')
