from netmiko import ConnectHandler
from netmiko import NetmikoTimeoutException
from netmiko import NetmikoAuthenticationException
import datetime

def backup_cisco(device,backup_path,logging,server):
    try:
        ssh_connect = ConnectHandler(**device)
        prompter = ssh_connect.find_prompt()
        if '>' in prompter:
            ssh_connect.enable()
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        with open(logging, 'a') as f:
            f.write(f"---\n\nFailed to run configuration backup on {device['host']}\n\n")
            f.write(f"{error}\n\n")
        pass
    else:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        if device['device_type'] == 'cisco_ios':
            hostname = ssh_connect.find_prompt().strip('#')
            ssh_connect.send_command('terminal length 0')
            resp = ssh_connect.send_command('show running-config')
            ssh_connect.send_command('no terminal length 0')
            ssh_connect.send_command('write memory')
            ssh_connect.disconnect()
        elif device['device_type'] == 'cisco_asa':
            hostname = ssh_connect.send_command('show hostname')
            #ssh_connect.send_command('pager 0')
            #resp = ssh_connect.send_command('show running-config')
            #ssh_connect.send_command('no pager 0')
            ssh_connect.send_command('write memory')
            resp = ssh_connect.send_command(
                command_string=f"copy startup-config tftp://{server}/{backup_path}/{hostname}_{timestamp}_startup-config",
                expect_string=r"Address or name of remote host",
                strip_prompt=False,
                strip_command=False
            )
            resp += ssh_connect.send_command(
                command_string="\n",
                expect_string=r"Destination filename",
                strip_prompt=False,
                strip_command=False
            )
            resp += ssh_connect.send_command(
                command_string="\n",
                expect_string=r"#",
                strip_prompt=False,
                strip_command=False
            )
            ssh_connect.disconnect()
        if resp:
            backup = f"{backup_path}/{hostname}_{timestamp}_runing-config.txt"
            with open(backup, 'w') as f:
                f.write(resp)
            with open(logging, 'a') as f:
                f.write(f"---\n\nSuccessfully run configuration backup on {hostname}\n\n")
