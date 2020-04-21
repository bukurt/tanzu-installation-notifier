# Tanzu (Pivotal) Installation Notifier
When a new update or upgrade process is started in Tanzu Application Service (TAS / PAS / PCF) or VMware Enterprise PKS, people usually tracks progress in Ops Manager UI. But it is usually difficult. With this repo you can simply build/run docker image and get installation notification from your slack app.

Hit the apply button and get slack notifications.

# Installation

Clone repo to your local.
    $ git clone https://github.com/kurtburak/tanzu-installation-notifier.git
    $ cd tanzu-installation-notifier/
Edit variables.
    $ vi tanzu.env
Run!
    $ docker-compose up -d

Optioanaly you can build image localy. Edit docker-compose.yaml and run!
    $ docker build . -t tanzu-install-watcher:local
    $ sed -i 's/bkurt\/tanzu-install-watcher:0.1/tanzu-install-watcher:local/g' docker-compose.yml
    $ docker-compose up -d
    
# Configuration Reference

Required configuration parameters are defined in table.

| Variable Name  |Definition                     |Example                      |Required|
|----------------|-------------------------------|-----------------------------|----------
|OPSMAN_IP    |IP address of Ops Manager VM.         |OPSMAN_IP=10.0.0.10      |Yes
|OPSMAN_USER     |Login user for Ops Manager.           |OPSMAN_USER=admin          |Yes
|OPSMAN_PASSWORD      |Base64 coded password of ospman login user |OPSMAN_PASSWORD=MTIzNDU2|Yes
|SLACK_URL|Slack API endpoint to push notification messages.| SLACK_URL=https://hooks.slack.com/services/TL2BSJFTZ/BL73TSGJDS/hTfKSTYfksdKHGStdfıasg|Yes
|SSH_USER  |Ssh user for accessing to OpsManager vm. Default is ubuntu |SSH_USER=ubuntu|No
|SSH_KEY  |Ssh key for accessing to OpsManager vm. |SSH_KEY=-----BEGIN RSA PRIVATE KEY-----\nJSKLJnsd....\n...YASGDklbj\n-----END RSA PRIVATE KEY----- |Yes
|HTTP_PROXY|If you are in corporate, it’s necessary to call slack API. It uses global format http://user:pass@10.0.0.50:8080  |HTTP_PROXY=http://10.0.0.50:8080|No
|HTTPS_PROXY|If you are in corporate, it’s necessary to call slack API. It uses global format http://user:pass@10.0.0.50:8080  |HTTPS_PROXY=http://10.0.0.50:8080|No
|NO_PROXY|If your OpsManager vm cannot be reached over proxy, set this to OpsManager IP address|NO_PROXY=10.0.0.10|No
|API_REQUEST_CYCLE| Request cycle time to call OpsManager API in seconds| API_REQUEST_CYCLE=60|Yes
|RUNNING_INFORM_PERIOD|Notification sending cycle in the same state. This parameter is multplied with API_REQUEST_CYCLE. Setting API_REQUEST_CYCLE and RUNNING_INFORM_PERIOD to 60 means that Installation status is checked in every 60 seconds, if status changed notification is sent immediately, if status is still same notification is sent in every 1 hour.| RUNNING_INFORM_PERIOD=60 |Yes
|SMTP_SERVER | Depreciated! |SMTP_SERVER=|No|
|EMAIL_SENDER | Depreciated! |EMAIL_SENDER=|No|
|EMAIL_RECEIVERS |Depreciated!|EMAIL_RECEIVERS=|No|

