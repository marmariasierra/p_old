#!/bin/bash
TS=`date "+%FT%T"`
tape=$1
dirtapes=/ghi/MPCDF/HPSS/GHI1/FilesystemLists/2018/02/cleanFiles/tapes
dirout=/ghi/MPCDF/HPSS/GHI1/FilesystemLists/2018/02/cleanFiles/output_files

#if [ ! -f $dirout/$tape.tostage.txt ]
if [ ! -f $dirout/$tape.staged.txt ]
then
        ls $dirtapes/$tape > $dirout/$tape.tostage.txt
        for agg in $(cat $dirout/$tape.tostage.txt)
        do
                cpath=$dirtapes/$tape/$agg
                #nohup ghi_stage -f $cpath 2> $dir/output_files/$tape\_ghi.txt &
                #ghi_stage -f $cpath >> $dirout/$tape.ghi.txt 2> $dirout/$tape.ghistage.txt &
                ghi_stage -f $cpath >> $dirout/$tape.ghistage.txt 2> $dirout/$tape.ghistage.txt &
                #echo -e "ghi_stage -f $cpath 2 >> $dirout/$tage\_ghi.txt &"
                echo -e "`date "+%FT%T"` staging files from $agg in $tape\r" >>  $dirout/ghistage.log
        done
        wait
        touch $dirout/$tape.staged.txt
fi
echo -e "`date "+%FT%T"` all files from $tape staged"
echo -e "`date "+%FT%T"` all files from $tape staged" >> $dirout/ghistage.log
