#!/bin/bash

# Based on https://github.com/mlpack/mlpack-wheels
# Based on https://gitlab.com/jason-rumengan/pyarma

basedir=$(python3 lib/openblas_support.py)
$use_sudo cp -r $basedir/lib/* /usr/local/lib
$use_sudo cp $basedir/include/* /usr/local/include

basedir=$(python3 lib/hdf5_support.py)
$use_sudo cp -r $basedir/lib/* /usr/local/lib
$use_sudo cp $basedir/include/* /usr/local/include
$use_sudo cp $basedir/bin/* /usr/local/bin

export DYLD_FALLBACK_LIBRARY_PATH=/usr/local/lib/
