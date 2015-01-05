#!/bin/sh



while read line
do
  name=$line
  for i in $(seq 2010 2014);
  do
    for j in $(seq 1 12);
    do
      file="$name-$i-$j-deep.json" 
      if [ ! -f "$file" ]; then
        #echo "File $name-$i-$j-deep.json not found!"
        echo "$name $i $j"
        scrapy crawl deepnews -a month=$j -a year=$i -a query=$name -o "$file"
      else
        echo "File $name-$i-$j-deep.json exist!"
        minimumsize=20000000
        actualsize=$(wc -c "$file" | cut -f 1 -d ' ')
        if [ $actualsize -ge $minimumsize ]; then
          echo " ==> skip"
        else
          echo " ==> need crawl"
          rm "$name-$i-$j-deep.json"
          scrapy crawl deepnews -a month=$j -a year=$i -a query=$name -o "$file"
          #echo size is under $minimumsize bytes
        fi
      fi
    done
  done
done < $1
