import oci
import sys


# OCI Config file - change to match your environment

configfile = "/your/path/.oci/config"  

def ScaleInstance(instance_ocid, scalecpus, topic_ocid):
    config = oci.config.from_file(configfile)
    databaseClient = oci.database.DatabaseClient(config)
    response = databaseClient.get_autonomous_database(instance_ocid)
    instance = response.data

    notificationClient = oci.ons.NotificationDataPlaneClient(config)

    if (instance.lifecycle_state == "AVAILABLE"):

     if int(scalecpus) == 0:
       response = databaseClient.stop_autonomous_database(autonomous_database_id = instance_ocid)
       bodyMessage = "Your ATP Database has been stopped and CPU count set to 0"
       notificationMessage = {"default": "ScaleMsg", "body": bodyMessage, "title": "ATP Database Notification"}
       print(notificationMessage) # For demo purposes
       notificationClient.publish_message(topic_ocid, notificationMessage)
     else:
       DbSystemDetails = oci.database.models.UpdateAutonomousDatabaseDetails(cpu_core_count = int(scalecpus))
       response = databaseClient.update_autonomous_database(autonomous_database_id = instance_ocid, update_autonomous_database_details = DbSystemDetails)
       bodyMessage = "Your ATP Database is being scaled to CPU count: " +scalecpus
       notificationMessage = {"default": "ScaleMsg", "body": bodyMessage, "title": "ATP Database Notification"}
       print(notificationMessage) # For demo purposes
       notificationClient.publish_message(topic_ocid, notificationMessage)
    elif (instance.lifecycle_state == "STOPPED"):
      response = databaseClient.start_autonomous_data_warehouse(autonomous_data_warehouse_id = instance.id)
      DbSystemDetails = oci.database.models.UpdateAutonomousDatabaseDetails(cpu_core_count = int(scalecpus))
      bodyMessage = "Your ATP Database is down. Scaling it with CPU count: " +scalecpus
      notificationMessage = {"default": "ScaleMsg", "body": bodyMessage, "title": "ATP Database Notification"}
      print(notificationMessage) # For demo purposes
      notificationClient.publish_message(topic_ocid, notificationMessage)


config = oci.config.from_file(configfile)

identity = oci.identity.IdentityClient(config)
user = identity.get_user(config["user"]).data
instance_ocid = "your_atp_ocid"
topic_ocid = "your_notification_topic_ocid"

databaseClient = oci.database.DatabaseClient(config)

ScaleInstance(instance_ocid, sys.argv[1], topic_ocid)
