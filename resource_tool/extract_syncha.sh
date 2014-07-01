#!/bin/sh

PARALLEL=/home/mai-om/local/bin/parallel

OUTDIR=FV/my/syncha
TARGET=`ls [SF]V/my/*.raw`
LOG=log.$$


for filename in `ls [SF]V/my/*.raw`
do
    echo $filename >> ${LOG}
    COL_NUM=`head -n 1 FV/my/RITE2_JA_dev_examsearch.xml.raw | awk '{print NF}'`
    
done
