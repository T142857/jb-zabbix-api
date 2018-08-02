#!/bin/bash
 
NAME="ZabbixCloudMetrics"
FLASKDIR=/Zabbix_Restfull_Gateway
SOCKFILE=/Zabbix_Restfull_Gateway/sock
USER=root
GROUP=root
NUM_WORKERS=6
 
echo "Starting $NAME"
 
# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR
 
# Start your gunicorn
exec gunicorn flask_restfull:app -b 0.0.0.0:5000 \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE
