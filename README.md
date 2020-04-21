# Tanzu (Pivotal) Installation Notifier
When a new update or upgrade process is started in Tanzu Application Service (TAS / PAS / PCF) or VMware Enterprise PKS, people usually tracks progress in Ops Manager UI. But it is usually difficult. With this repo you can simply build/run docker image and get installation notification from your slack app.

Hit the apply button and get slack notifications.

# Prerequisites

    export VMWARE_PASSWORD='vCenter Password'
    export VMWARE_USER='vCenter Username'
    export VMWARE_HOST='vCenter IP/FQDN'

# Configuration Reference

Required configuration parameters are defined in table.

| Variable Name  |Definition                     |Example                      |Required|
|----------------|-------------------------------|-----------------------------|----------
|OPSMAN_IP    |IP address of Ops Manager VM.         |OPSMAN_IP=10.0.0.10      |Yes
|OPSMAN_USER     |Login user for Ops Manager.           |OPSMAN_USER=admin          |Yes
|OPSMAN_PASSWORD      |Base64 coded password of ospman login user |OPSMAN_PASSWORD=MTIzNDU2|Yes
|SSH_USER  |Ssh user for accessing to OpsManager vm. Default is ubuntu |SSH_USER=ubuntu|No
|SSH_KEY  |Ssh key for accessing to OpsManager vm. |SSH_KEY=-----BEGIN RSA PRIVATE KEY-----\n....\n-----END RSA PRIVATE KEY----- |Yes
|HTTP_PROXY|If you are in corporate, it’s necessary to call slack API  |HTTP_PROXY=http://user:password@10.0.0.50:8080 or HTTP_PROXY=http://user@10.0.0.50:8080 or HTTP_PROXY=http://10.0.0.50:8080|No
||||
||||
||||
||||
||||
||||
||||
||||

