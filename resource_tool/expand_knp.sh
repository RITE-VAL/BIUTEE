#!/bin/sh

# How to use

# あらかじめ該当ディレクトリをexpand_knp.shのあるディレクトリにコピーし，そのディレクトリに移動する
# ./expand_knp.sh
# を実行するとそれぞれのディレクトリに *.cab.bz2という解析済みデータができる

LOG_FILE=log.txt

touch ${LOG_FILE}
echo `date` start >> ${LOG_FILE}
for dir in `ls`
do
    if [ -d $dir ]; then
        cd $dir
        for file in `ls *.bz2`
        do
            base_file_name=`echo $file | sed -e 's/.knp.bz2//g'`
            bzip2 -dc $file | nkf -w | python ../expand_knp_file.py | cabocha -f1 | bzip2 > $base_file_name.cab.bz2
            echo $dir/$file "done." >> ../${LOG_FILE}
        done
        cd ../
    fi
done
echo `date` end >> ${LOG_FILE}
