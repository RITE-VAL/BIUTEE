#!/bin/sh

ls -l . | awk '{print $9}' | grep tsubame | parallel ./filemerge.sh {}

python merge.py
