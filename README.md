The collection of scripts to automatically backup network configurations on various network vendor devices, 
including PAN, Fortigate, F5 BIG-IP, Cisco, and HPE/Aruba.
  - Use dotenv to store sensitive parameters
  - Use Netmiko for Cisco and HPE/Aruba
  - Use API for PAN, Fortigate, and F5 BIG-IP
  - Send a notification email after completing

Here is the directory for network configuration backup,
"""
├── backup
│   ├── devices.yaml
│   │── .env
│   ├── logs
│   └── backups
│       ├── cisco
│       ├── fgt
│       ├── hpe
│       └── pan
"""
Set up a cron job to run "run_backup.py"
