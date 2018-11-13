#!/bin/bash
TS=`date "+%FT%T"`
tape=$1
dirout=/ghi/MPCDF/HPSS/GHI1/FilesystemLists/2018/02/cleanFiles/output_files
cd $dirout
while [ ! -f $tape.backup_done ]
do
    echo "waiting for the backup of $tape" >> ghistage.log
    sleep 30
done