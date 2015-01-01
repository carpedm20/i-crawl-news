#!/bin/sh
while read line
do
  name=$line
  for i in {2010..2014}
  do
    for j in {1..12}
    do
      echo "$name $i $j"
      scrapy crawl news -a month=$j -a year=$i -a query=$name -o "$name-$i-$j".json
    done
  done
done < $1
