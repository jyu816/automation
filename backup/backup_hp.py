from netmiko import ConnectHandler
from netmiko import NetmikoTimeoutException
from netmiko import NetmikoAuthenticationException
import datetime

def backup_hp(device,backup_path,logging,server):
    try:
        ssh_connect = ConnectHandler(**device)
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        with open(logging, 'a') as f:
            f.write(f"---\n\nFailed to run configuration backup on {device['host']}\n\n")
            f.write(f"{error}\n\n")
        pass
    else:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        if device['device_type'] == 'hp_procurve':
            hostname = ssh_connect.find_prompt().strip('#')
            #ssh_connect.send_command('no page')
            #resp = ssh_connect.send_command('show running-config')
            #ssh_connect.send_command('page')
            resp = ssh_connect.send_command_timing(
                f"copy startup-config tftp {server} {backup_path}/{hostname}_{timestamp}_startup.cfg",
                strip_command=False,
                strip_prompt=False
            )
            ssh_connect.disconnect()
        elif device['device_type'] == 'hp_comware':
            hostname = ssh_connect.find_prompt().strip('<').strip('>')
            #ssh_connect.send_command('screen-length disable')
            #resp = ssh_connect.send_command('display current-configuration')
            #ssh_connect.send_command('undo screen-length disable')
            resp = ssh_connect.send_command_timing(
                f"tftp {server} put flash:/startup.cfg {backup_path}/{hostname}_{timestamp}_startup.cfg",
                strip_command=False,
                strip_prompt=False
            )
            ssh_connect.disconnect()
        if resp:
            #backup = f"{backup_path}/{hostname}_{timestamp}_runing-config.txt"
            #with open(backup, 'w') as f:
                #f.write(resp)
            with open(logging, 'a') as f:
                f.write(f"---\n\nSuccessfully run configuration backup on {hostname}\n\n")
