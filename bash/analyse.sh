#!bin/bash

file=$1
if [ -z $file ]
then 
    files=$(pwd | echo *.log)
    for file in $files
    do
        echo "------------file $file--------------"
        . analyse.sh $file
        echo "------------------------------------"
    done
else

    cwd=$(pwd)

    # общее количество запросов
    echo "total requests count"
    cat $file | grep HTTP | wc -l

    #уникальные методы
    arr=$(cat $file | awk 'length($6)<10{print substr($6,2)}' | sort | uniq)

    for n in $arr
    do
        echo "count of $n:"
        cat $file | grep $n | wc -l
    done

    echo " "
    echo "top 10 biggest total:"
    cat $file | awk '{print $10, $0}' | sort -r -n | cut -d " " -f2- | head -10

    echo " "
    echo "Top 10 requests with client errors by quantity:"
    cat $file | awk 'int($9/100)==4 {print $0}' | awk '{count[$7]++}END{for (url in count) print count[url], url}' | sort -r -n | head -10

    echo " "
    echo "Top 10 requests with server errors by bytes sent:"
    cat $file | awk 'int($9/100)==5 {print $10" requests for ", "url:"$7,"with code:"$9}' | sort -rn | head -10
fi