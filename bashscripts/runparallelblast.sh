#!/bin/bash

fastafile=$1
blocksize=$2
blastAlgorithm=$3
evalue=$4
outfmt=$5
db=$6

cat $1 | parallel --block $2 --recstart '>' --pipe $3 -evalue $4 -outfmt $5 -db $6 -query - > "$1.res"
