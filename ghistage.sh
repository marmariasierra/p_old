#!/bin/bash
TS=`date "+%FT%T"`
tape=$1
dirtapes=/ghi/MPCDF/HPSS/GHI1/FilesystemLists/2018/02/cleanFiles/tapes
dirout=/ghi/MPCDF/HPSS/GHI1/FilesystemLists/2018/02/cleanFiles/output_files

if [ ! -f $dirout/$tape.tostage.txt ]
then
        ls $dirtapes/$tape > $dirout/$tape.tostage.txt
        for agg in $(cat $dirout/$tape.tostage.txt)
        do
                cpath=$dirtapes/$tape/$agg
                #nohup ghi_stage -f $cpath 2> $dir/output_files/$tape\_ghi.txt &
                #ghi_stage -f $cpath >> $dirout/$tape.ghi.txt 2> $dirout/$tape.ghistage.txt &
                ghi_stage -f $cpath >> $dirout/$tape.ghistage.txt 2> $dirout/$tape.ghistage.txt &
                #echo "ghi_stage -f $cpath 2 >> $dirout/$tage\_ghi.txt &"
                echo "$TS staging files from $agg in $tape" >>  $dirout/ghistage.log
        done
        wait
fi
echo "$TS all files from $tape staged"
echo "$TS all files from $tape staged" >> $dirout/ghistage.log
