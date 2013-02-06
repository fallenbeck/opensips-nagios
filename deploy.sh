#!/bin/sh
host="192.168.14.128"


echo "Deploying files to host $host..."

echo "asmonia -> root@192.168.14.128:/usr/lib/nagios/plugins/"
scp asmonia root@192.168.14.128:/usr/lib/nagios/plugins/

echo "asmonia.cfg -> root@192.168.14.128:/etc/nagios-plugins/config/"
scp asmonia.cfg root@192.168.14.128:/etc/nagios-plugins/config/

echo "asmonia -> root@192.168.14.128:/etc/nagios3/conf.d/"
scp asmonia_nagios3.cfg root@192.168.14.128:/etc/nagios3/conf.d/

echo "opensipsctl_dummy -> fallenbeck@192.168.14.128:~"
scp opensipsctl_dummy fallenbeck@192.168.14.128:~