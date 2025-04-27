The collection of scripts to automatically backup network configurations on various network vendor devices, 
including PAN, Fortigate, F5 BIG-IP, Cisco, and HPE/Aruba.

  - Use dotenv to store sensitive parameters
  - Use Netmiko for Cisco and HPE/Aruba
  - Use API for PAN, Fortigate, and F5 BIG-IP

Here is directory for network configuration backup,

~/backup\n
 |- devices.yaml\n
 |- logs\n
 |- .env\n
 |- backups\n
     |- pan\n
     |- fgt\n
     |- cisco\n
     |- hpe\n
