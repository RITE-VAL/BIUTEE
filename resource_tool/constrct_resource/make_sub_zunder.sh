#!/bin/sh

f=$1
a=$2

if [ -z ${a} ]; then
    while read LINE
    do 
        id=`echo ${LINE} | cut -d " " -f 1`
        t1=`echo ${LINE} | cut -d " " -f 2`
        t2=`echo ${LINE} | cut -d " " -f 3`
        ans=`echo ${LINE} | cut -d " " -f 4`
        echo "#" ${id} ${t1} ${t2} ${ans}
        echo "${t1}" | zunda
        echo "%%"
        echo "${t2}" | zunda
        echo
    done < ${f}
else
    while read LINE
    do 
        id=`echo ${LINE} | cut -d " "  -f 1`
        t2=`echo ${LINE} | cut -d " " -f 2`
        ans=`echo ${LINE} | cut -d " " -f 3`
        echo "#" ${id} ${t2} ${ans}
        echo "${t2}" | zunda
        echo
    done < ${f}
fi
