from pathlib import Path
from dotenv import load_dotenv
import os, yaml, datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

from backup_f5 import backup_f5  
from backup_pan import backup_pan
from backup_hp import backup_hp
from backup_cisco import backup_cisco
from backup_fgt import backup_fgt

def load_devices(dev_file):
    with open(dev_file, "r") as f:
        return yaml.safe_load(f)

def runner():
    dev_file = Path.home() / 'devices.yaml'
    env_file = Path.home() / '.env'
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
    logging = Path.home() / 'logs' / f'log_{timestamp}.txt'
    
    devices = load_devices(dev_file)
    
    load_dotenv(env_file)
    username = os.getenv(devices['global_settings']['username'])
    password = os.getenv(devices['global_settings']['password'])

    tftp_server = "192.168.19.100"
    
    for vendor in devices['devices']:
        backup_path = f"{Path.home()}/backup/{devices['devices'][vendor]['backup_path']}"
        if vendor == 'PAN':
            for host in devices['devices'][vendor]['hosts']:
                if not host["enabled"]:
                    continue
                device = {
                    'host': host['host'],
                    'username': username,
                    'password': password
                }
                backup_pan(device,backup_path,logging)
        elif vendor == 'F5_BIGIP':
            for host in devices['devices'][vendor]['hosts']:
                if not host["enabled"]:
                    continue
                device = {
                    'host': host['host'],
                    'username': username,
                    'password': password
                }
                backup_f5(device,backup_path,logging)
        elif vendor == 'HPE_Aruba':
            for host in devices['devices'][vendor]['hosts']:
                if not host["enabled"]:
                    continue
                device = {
                    'host': host['host'],
                    'username': username,
                    'password': password,
                    'device_type': host['device_type']
                }
                backup_hp(device,backup_path,logging,tftp_server)
        elif vendor == 'Cisco':
            for host in devices['devices'][vendor]['hosts']:
                if not host["enabled"]:
                    continue
                device = {
                    'host': host['host'],
                    'username': username,
                    'password': password,
                    'device_type': host['device_type']
                }
                backup_cisco(device,backup_path,logging,tftp_server)
        elif vendor == 'Fortigate':
            for host in devices['devices'][vendor]['hosts']:
                if not host["enabled"]:
                    continue
                device = {
                    'host': host['host'],
                    'apiKey': os.getenv(host['apiKey'])
                }
                backup_fgt(device,backup_path,logging)
    # Send email
    sender_email = 'do-not-reply@example.com'
    receiver_email = 'it@example.com'
    subject = "Scheduled configuration backup"
    msg = MIMEMultipart()
    message = f"""\
        Scheduled job completed! Please check the results in the below log file,
    
          /Users/backup/logs/log_{timestamp}.txt

        Configuration backups are stored in the below location,
          
          /Users/backup/backups
          
    """
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.attach(MIMEText(message, 'plain'))
    with smtplib.SMTP(host='192.168.19.161', port='25') as server:
        server.send_message(msg)

if __name__ == "__main__":
    runner()
