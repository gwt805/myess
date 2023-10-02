#!/bin/bash

str=$"\n"

cd /home/weitao/myess
nohup /home/weitao/anaconda3/bin/python myess/manage.py runserver 0.0.0.0:8088 > /dev/null 2>&1 &
sstr=$(echo -e $str)
echo $sstr