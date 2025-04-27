# Automate Network Configuration Backup
The collection of scripts to automatically backup network configurations on various network vendor devices, 
including PAN, Fortigate, F5 BIG-IP, Cisco, and HPE/Aruba.
  - Use dotenv to store sensitive parameters
  - Use Netmiko for Cisco and HPE/Aruba
  - Use API for PAN, Fortigate, and F5 BIG-IP
  - Send a notification email after completing

Set up a cron job which runs "python run_backup.py" to create network configuration backup regularly.

# Directory hierarchy for network configuration backup,

backup  
|── devices.yaml  
|── .env  
|── logs  
|── backups  
    |── cisco  
    |── fgt  
    |── hpe  
    |── pan  
