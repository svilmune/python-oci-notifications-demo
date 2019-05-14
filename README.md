# python-oci-notifications-demo

Basic demo of using OCI notifications service when scaling ATP database up or down. 

You need to modify following variables:

1. configfile with path of your OCI configfile
2. instance_ocid with the OCID of your ATP database
3. topic_ocid with the notification topic OCID where to publish messages

# Usage

Run python atp.py 0 to stop your ATP database
Run python atp.py 1 to scale your ATP database to use one (1) CPU

# To be added

If the requested core is same as current one there is no additional check and script will throw an error.
