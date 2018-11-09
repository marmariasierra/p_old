#!/bin/bash
TS=`date "+%FT%T"`
tape=$1
dir=/ghi/MPCDF/HPSS/GHI1/FilesystemLists/2018/02/cleanFiles/tapes
while [ ! -f $tape.tostage.txt ]
do
    ls $dir/$tape > $tape.tostage.txt
    for agg in $(cat $tape.tostage.txt)
    do
        cpath=$dir/$tape/$agg
        #nohup ghi_stage -f $cpath 2> $dir/output_files/$tape\_ghi.txt &
        #ghi_stage -f $cpath 2> $dir/output_files/$tage.ghi.txt &
        echo "ghi_stage -f $cpath 2> $dir/output_files/$tage\_ghi.txt &"
        echo "$TS staging files from $tape" >>  $dir/output_files/ghistage.log
     done
     wait
echo "$TS all files from $tape staged" >> $dir/output_files/ghistage.log
done
