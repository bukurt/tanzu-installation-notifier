# tanzu-installation-notifier
Tanzu (Pivoal) Installation Slack Notifier

# Prerequisites

    export VMWARE_PASSWORD='vCenter Password'
    export VMWARE_USER='vCenter Username'
    export VMWARE_HOST='vCenter IP/FQDN'

# Configuration Reference

Required configuration parameters are defined in table.

| Variable Name  |Definition                     |Example                      |
|----------------|-------------------------------|-----------------------------|
|cluster_name    |OpenShift cluster name         |cluster_name: openshift      |
|domain_name     |Base DNS domain.           |domain_name: example.com          |
|datacenter      |vSphere datacenter in which openshift vms will be created | datacenter: TestDC|
|vmware_cluster  |vSphere cluster in which openshift vms will be created | vmware_cluster: TestCLS01|
