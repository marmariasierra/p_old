#!/bin/bash

tape=$1
dirtapes=/ghi/MPCDF/HPSS/GHI1/FilesystemLists/2018/02/cleanFiles/tapes
dirout=/ghi/MPCDF/HPSS/GHI1/FilesystemLists/2018/02/cleanFiles/output_files
#nfiles=`ls $dirout/$tape/ |wc -l`

if [ ! -d $dirout/$tape ]
then mkdir $dirout/$tape
fi

if [ ! -f $dirout/$tape.staged.txt ]
then
    /ghi/MPCDF/HPSS/GHI1/FilesystemLists/2018/02/cleanFiles/ghistage.sh $tape
fi

counter=1
for agg in $(cat $dirout/$tape.tostage.txt)
do
#    if [ $nfiles -lt 0 ]
     if [ ! -f $dirout/$tape/nonB_files.$counter.txt ]
     then
        cpath=$dirtapes/$tape/$agg
        ghi_ls -f $cpath | grep "^H" | sed -e 's,.*/ghi/p_old/MPIN,/ghi/p_old/MPIN,' > $dirout/$tape/nonB_files.$counter.txt
        ghi_ls -f $cpath | grep "^B" | wc > $dirout/$tape/B_files.$counter.txt
     fi
     if [ -s $dirout/$tape/nonB_files.$counter.txt ]
     then
            echo "staging remaining files in $counter"
            ghi_stage -f $dirout/$tape/nonB_files.$counter.txt >> $dirout/$tape.outputghi.txt 2> $dirout/$tape.outputghi.txt &
            wait
            ghi_ls -f $dirout/$tape/nonB_files.$counter.txt | grep "^H" | sed -e 's,.*/ghi/p_old/MPIN,/ghi/p_old/MPIN,' >> $dirout/$tape/problematic_files.txt
            if [ -s $dirout/$tape/problematic_files.txt ]
            then
                echo -e "`date "+%FT%T"` files in $dirout/$tape/problematic_files.txt could not be staged" >> $dirout/ghistage.log
            else
                echo "all files in $tape staged" > $dirout/$tape\_staged.txt
                echo -e "`date "+%FT%T"` all files in $tape staged" >> $dirout/ghistage.log
            fi
     elif [ ! -s $dirout/$tape/nonB_files.$counter.txt ]
     then
        echo "files in $agg already staged"
     fi
    ((counter++))
done
wait