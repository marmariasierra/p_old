#!/bin/bash
TS=`date "+%FT%T"`
tape=$1
dir=/ghi/MPCDF/HPSS/GHI1/FilesystemLists/2018/02/cleanFiles/output_files
cd $dir
while [ ! -f $tape.backup_done ]
do
    echo "waiting for the backup of $tape"
    sleep 30
done