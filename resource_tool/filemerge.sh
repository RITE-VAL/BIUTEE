#!/bin/sh

dir=$1

if [ -d $dir ]; then
    for file in `ls ${dir}*.bz2`
    do
        base_file_name=`echo $file | sed -e 's/.cab.bz2//g'`
        bunzip2 -dc $file | python make_vocab.py $file
        cat ${base_file_name}.freq >> $dir/all.freq
        cat ${base_file_name}.vocab >> $dir/all.vocab
    done
    python merge_small.py $dir
    mv -f $dir/all.freq.t $dir/all.freq
fi
