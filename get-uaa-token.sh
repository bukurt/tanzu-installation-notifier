#!/bin/bash

if [ -z $OPSMAN_IP ] || [ -z $OPSMAN_USER ] || [ -z $OPSMAN_PASSWORD ]; then
  echo "Tanzu ops manager informations are missing."
  echo "Be sure OPSMAN_IP, OPSMAN_USER and OPSMAN_PASSWORD variables are set."
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

ssh -l $SSH_USER $OPSMAN_IP 'bash -s' << 'ENDSSH'
	uaac target http://localhost:8080/uaa > /dev/null
	sec=`echo $OPSMAN_PASSWORD | base64 --decode`
	uaac token owner get opsman $OPSMAN_USER -s "" -p $sec > /dev/null
	token=$(uaac context | grep access_token | awk '{print $2}')
	echo $token | tr -d '\n'
ENDSSH


