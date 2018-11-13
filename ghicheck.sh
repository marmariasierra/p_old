#!/bin/bash

TS=`date "+%FT%T"`
tape=$1
dirtapes=/ghi/MPCDF/HPSS/GHI1/FilesystemLists/2018/02/cleanFiles/tapes
dirout=/ghi/MPCDF/HPSS/GHI1/FilesystemLists/2018/02/cleanFiles/output_files

if [ ! -d $dirout/$tape ]
then mkdir $dirout/$tape
fi
#ls $dirtapes/$tape > $dirout/$tape.tostage.txt
#if [ ! -f $dirout/$tape.tostage.txt ]
#then /ghi/MPCDF/HPSS/GHI1/FilesystemLists/2018/02/cleanFiles/ghistage.sh $tape
#fi
#while [ ! -f $dirout/$tape\_staged.txt.txt ]
#do
counter=1
for agg in $(cat $dirout/$tape.tostage.txt)
do
        if [ ! -f $dirout/$tape/nonB_files.$counter.txt ]
        then
                cpath=$dirtapes/$tape/$agg
                ghi_ls -f $cpath | grep "^H" | sed -e 's,.*/ghi/p_old/MPIN,/ghi/p_old/MPIN,' > $dirout/$tape/nonB_files.$counter.txt
                ghi_ls -f $cpath | grep "^B" | wc > $dirout/$tape/B_files.$counter.txt
                if [ -s $dirout/$tape/nonB_files.$counter.txt ]
                then
                        echo "staging remaining files in $counter"
                        ghi_stage -f $dirout/$tape/nonB_files.$counter.txt >> $dirout/$tage.ghi.txt 2> $dirout/$tape.outputghi2.txt &
                        echo "all files in $tape staged" > $dirout/$tape\_staged.txt
                else
                        echo "files in $agg already staged"
                fi
        fi
        ((counter++))
done
wait
echo "all files in $tape staged"




