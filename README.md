# Automate Network Configuration Backup
The collection of scripts to automatically backup network configurations for various vendors, 
including PAN, Fortigate, F5 BIG-IP, Cisco, and HPE/Aruba.
## Key Features
  - Use dotenv to store sensitive parameters
  - Use Netmiko for Cisco and HPE/Aruba
  - Use REST API for PAN, Fortigate, and F5 BIG-IP
  - Send a notification email after completing
  - Log success/failures

Set up a cron job which runs "python run_backup.py" to backup network configurations regularly.

## Directory Structure
<pre>
backup
|── devices.yaml
|── .env
|── logs
|── backups
    |── cisco
    |── fgt
    |── hpe
    |── pan
    |── f5
</pre>
