#!/bin/sh
declare -a foo1=("element1" "element2" "element3")
declare -a foo2=("eaa a" "bbb b" "element3")

for i in "${!foo1[@]}"; do 
    printf "%s\t%s\t%s\n" "$i" "${foo1[$i]}" "${foo2[$i]}"
done
