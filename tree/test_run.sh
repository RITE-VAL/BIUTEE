#!/bin/sh

PYTHON=python

for file in `ls test/test_*.py`
do
    echo testing ${file}
    ${PYTHON} $file
    echo testing ${file} Done.
done

