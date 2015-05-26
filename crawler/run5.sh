#!/bin/sh

#name="GOOGL"
#name="interstellar movie" #2014,2015
#name="the dark knight" #2008,2009
#name="inception movie" #2010,2011

#name="The Avengers movie" #2012,2013
#name="Frozen movie" #2012,2013

#name="the departed movie" #2006,2007
#name="the intouchables movie" #2012,2013

#declare -a foo1=("the dark knight" "inception movie" "the avengers movie" "frozen movie" "skyfall movie")
declare -a foo1=("NASDAQ:GOOG" "NASDAQ:FB")
declare -a foo2=("2008" "2010" "2012" "2013" "2012")
declare -a foo3=("2009" "2011" "2012" "2014" "2013")

#declare -a foo1=("interstellar movie")
#declare -a foo2=("2014")
#declare -a foo3=("2015")

for i in "${!foo1[@]}";
do
  name=${foo1[$i]}
  syear=${foo2[$i]}
  eyear=${foo3[$i]}
    
  for i in $(seq $syear $eyear);
  do
    for j in $(seq 1 12);
    do
      file="./backup/$name-$i-$j.json" 
      if [ ! -f "$file" ]; then
        #echo "File $file not found!"
        echo "$name $i $j"
        scrapy crawl news -a month="$j" -a year=$i -a query="$name" -o "$file"
      else
        echo "File $file exist!"
        minimumsize=100
        actualsize=$(wc -c "$file" | cut -f 1 -d ' ')
        if [ $actualsize -ge $minimumsize ]; then
          echo " ==> skip"
        else
          echo " ==> need crawl"
          rm "$file"
          echo scrapy crawl news -a month=$j -a year=$i -a query="$name" -o "$file"
          scrapy crawl news -a month=$j -a year=$i -a query="$name" -o "$file"
          echo size is under $minimumsize bytes
        fi
      fi
    done
  done
done
