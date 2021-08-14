#!/bin/bash

for i in $(ps aux | grep netcheck.sh | grep -v grep | awk '{print $2}');
do
    sudo kill $i
done

ps aux | grep netcheck.sh


