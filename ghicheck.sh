#!/bin/bash
TS=`date "+%FT%T"`
tape=$1
dir=/ghi/MPCDF/HPSS/GHI1/FilesystemLists/2018/02/cleanFiles/tapes
cd $dir
counter=1
for agg in $(cat $tape.tostage.txt)
do
        cpath=$dir/$tape/$agg
        cd $dir/output_files
        echo "$PWD"
        ghi_ls -f $cpath | grep "^H" | sed -e 's,.*/ghi/p_old/MPIN,/ghi/p_old/MPIN,' > nonB_files.txt
        if [ -s nonB_files.txt ]
        then
            echo "staging remaining files"
            ghi_stage -f nonB_files.txt &> $dir/output_files/$tage.ghi.txt &
            echo "all files in $tape staged" > $tape\_staged.txt
       else
            echo "all files in $tape staged" > $tape\_staged.txt
            echo "all files in agg $counter of $tape"
        fi
        ((counter++))
done
