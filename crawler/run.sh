#!/bin/sh

while read line
do
  name=$line
  for i in $(seq 2010 2014);
  do
    for j in $(seq 1 12);
    do
      echo "$name $i $j"
      echo scrapy crawl news -a month=$j -a year=$i -a query="$name" -o "$name-$i-$j.json"
      #scrapy crawl news -a month=$j -a year=$i -a query="$name" -o "$name-$i-$j.json"
      scrapy crawl news -a month=$j -a year=$i -a query="$name" -o "./new_articles/$name-$i-$j.json"
    done
  done
done < $1
