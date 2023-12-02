#!/bin/sh

echo Part 1:
cat input.dat \
    | tr -d \[:alpha:\] \
    | sed -E "s/([0-9])[0-9]+([0-9])/\1\2/;s/^([0-9])\$/\1\1/" \
    | awk '{sum+=$1;} END {print sum;}'

echo Part 2:
cat input.dat \
    | sed -E "s/(one)/\11\1/g;s/(two)/\12\1/g;s/(three)/\13\1/g;s/(four)/\14\1/g;s/(five)/\15\1/g;s/(six)/\16\1/g;s/(seven)/\17\1/g;s/(eight)/\18\1/g;s/(nine)/\19\1/g" \
    | tr -d \[:alpha:\] \
    | sed -E "s/([0-9])[0-9]+([0-9])/\1\2/;s/^([0-9])\$/\1\1/" \
    | awk '{sum+=$1;} END {print sum;}'
