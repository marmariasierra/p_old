#!/bin/bash
TS=`date "+%FT%T"`

while [ ! -f $tape.tostage.txt ]
do
    ls $tape >  $tape.tostage.txt
done
while read agg
do ghi_stage -f $agg & &> $agg.txt
done < $tape.tostage.txt
echo "$TS all files staged" >> ghistage.log

