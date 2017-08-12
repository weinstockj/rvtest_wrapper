#!/bin/bash
directory=$1
pheno=$2

# https://stackoverflow.com/questions/24641948/merging-csv-files-appending-instead-of-merging/24643455
OutFileName="${directory}${pheno}.singleFirth.assoc"                       # Fix the output name

i=0                                       # Reset a counter
for filename in ${directory}*.assoc; do 
   if [ "$filename"  != "$OutFileName" ] ;      # Avoid recursion 
       then 
       if [[ $i -eq 0 ]] ; then 
               head -1  $filename > $OutFileName # Copy header if it is the first file
       fi
               tail -n +2  $filename >> $OutFileName # Append from the 2nd line each file
       i=$(( $i + 1 ))                        # Increase the counter
   fi
done

touch ${directory}rvtests.OK
