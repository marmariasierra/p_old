#!/bin/bash
TS=`date "+%FT%T"`
tape=$1
dirtapes=/ghi/MPCDF/HPSS/GHI1/FilesystemLists/2018/02/cleanFiles/tapes
dirout=/ghi/MPCDF/HPSS/GHI1/FilesystemLists/2018/02/cleanFiles/output_files

while [ ! -f $dirout/$tape.tostage.txt ]
do
        ls $dirtapes/$tape > $dirout/$tape.tostage.txt
        for agg in $(cat $dirout/$tape.tostage.txt)
        do
                cpath=$dirtapes/$tape/$agg
                #nohup ghi_stage -f $cpath 2> $dir/output_files/$tape\_ghi.txt &
                ghi_stage -f $cpath >> $dirout/$tage.ghi.txt 2> $dirout/$tape.errorghi.txt &
                #echo "ghi_stage -f $cpath 2 >> $dirout/$tage\_ghi.txt &"
                echo "$TS staging files from $agg in $tape" >>  $dirout/ghistage.log
        done
        wait
echo "$TS all files from $tape staged" >> $dirout/ghistage.log
done
echo "$TS all files from $tape staged"