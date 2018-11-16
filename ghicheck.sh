#!/bin/bash

#TS=`date "+%FT%T"`
tape=$1
dirtapes=/ghi/MPCDF/HPSS/GHI1/FilesystemLists/2018/02/cleanFiles/tapes
dirout=/ghi/MPCDF/HPSS/GHI1/FilesystemLists/2018/02/cleanFiles/output_files
nfiles=`ls $dirout/$tape/ |wc -l`

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
    if [ $nfiles -lt

        if [ $dirout/$tape/nonB_files.$counter.txt ]
#       then
                cpath=$dirtapes/$tape/$agg
                ghi_ls -f $cpath | grep "^H" | sed -e 's,.*/ghi/p_old/MPIN,/ghi/p_old/MPIN,' > $dirout/$tape/nonB_files.$counter.txt
                ghi_ls -f $cpath | grep "^B" | wc > $dirout/$tape/B_files.$counter.txt
                if [ -s $dirout/$tape/nonB_files.$counter.txt ]
                then
                        echo "staging remaining files in $counter"
                        ghi_stage -f $dirout/$tape/nonB_files.$counter.txt >> $dirout/$tape.outputghi2.txt 2> $dirout/$tape.outputghi2.txt &
                        echo "all files in $tape staged" > $dirout/$tape\_staged.txt
                else
                        echo "files in $agg already staged"
                fi
#       fi
        ((counter++))
echo "$counter"
done
wait
echo "all files in $tape staged"
#done
#echo "all files staged without while"

