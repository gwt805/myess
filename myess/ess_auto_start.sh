#!/bin/bash
str=$"\n"
cd /home/weitao/myess
nohup /home/weitao/anaconda3/bin/python myess/manage.py runserver 0.0.0.0:8088 > /home/weitao/myess/ESS.log 2>&1 &
sstr=$(echo -e $str)
echo $sstr

nohup /home/weitao/anaconda3/bin/python myess/manage.py listenkfk --start_listen_kafka > /home/weitao/myess/ess_kafka.log 2>&1 &
sstr=$(echo -e $str)
echo $sstr