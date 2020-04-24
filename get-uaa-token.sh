#!/bin/bash

if [ -z $OPSMAN_IP ] || [ -z $OPSMAN_USER ]; then
  echo "Tanzu ops manager informations are missing."
  echo "Be sure OPSMAN_IP and OPSMAN_USER variables are set."
  exit 1
fi

if [ -z $SSH_USER ]; then
  SSH_USER=ubuntu
fi

KNOW_HOST=`grep $OPSMAN_IP /root/.ssh/known_hosts`
if [ -z $KNOW_HOST ]; then
  ssh-keyscan $OPSMAN_IP > /root/.ssh/known_hosts
fi

if [ ! -f /root/.ssh/id_rsa ]; then
  echo $SSH_KEY > /root/.ssh/id_rsa
  sed -i 's/\\n/\n/g' /root/.ssh/id_rsa
  chmod 600 /root/.ssh/id_rsa
fi

echo $OPSMAN_USER > opsman_user
scp opsman_user $SSH_USER@$OPSMAN_IP:~/opsman_user

ssh -l $SSH_USER $OPSMAN_IP 'bash -s' << 'ENDSSH'
        uaac target http://localhost:8080/uaa > /dev/null
        opsman_user=`cat ~/opsman_user`
        sec=`sudo grep "opsman.admin" /home/tempest-web/ramdisk/uaa/config/uaa.yml | grep $opsman_user | grep "OpsMan" | grep "Admin" | awk -F "|" '{print $2}'`
        rm -f ~/opsman_user
        uaac token owner get opsman $opsman_user -s "" -p $sec > /dev/null
        token=$(uaac context | grep access_token | awk '{print $2}')
        echo $token | tr -d '\n'
ENDSSH


