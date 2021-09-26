#!/bin/bash
first_date=1632637915
date_now=`date +%s`
interval_day=$((date_now-first_date))
if (($interval_day > 1728000 ))
then
    echo "yes" #换成需要执行的语句
    sed -i "s/^first_date=.*/first_date=$date_now/g" repeat_day.sh
fi
