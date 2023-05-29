#!/bin/bash
str=$"\n"
cd /home/weitao/myess
nohup /home/weitao/anaconda3/bin/python myess/manage.py listenkfk --start_listen_kafka > /home/weitao/myess/ess_kafka.log 2>&1 &
sstr=$(echo -e $str)
echo $sstr