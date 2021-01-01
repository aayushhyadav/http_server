#!/bin/bash

cmd=''
count=1

while true
do
    if [ $count -eq 1 ]
    then
        python3 server.py &
        last_PID=$!
    fi

    read cmd

    if [ "$cmd" = "Stop" ]
    then
        kill $last_PID
        break
    else
        echo "Enter a valid command"
    fi
    count=`expr $count + 1`
done