#!/bin/bash
str=$"\n"
cd /home/root/myess
nohup /home/${USER}/anaconda3/bin/python myess/manage.py runserver 0.0.0.0:8088 > /home/${USER}/myess/ESS.log 2>&1 &
sstr=$(echo -e $str)
echo $sstr