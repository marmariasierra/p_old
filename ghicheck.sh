#!/bin/bash
TS=`date "+%FT%T"`
tape=$1
while [ ! -f $tape.tostage.txt ]
do
    ls $tape >  $tape.tostage.txt
done
while read agg
do ghi_ls -f $agg | grep "^H" > nonB_files.txt
#create nonBfile.txt that can be sent to ghi_stage
if [(wc nonB_files.txt !=0]
then ghi_stage -f nonB_files.txt
fi
echo "$TS all files checked" >> ghicheck.log