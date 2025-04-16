import datetime, requests
from urllib3.exceptions import InsecureRequestWarning

def backup_fgt(device,backup_path,logging):
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    api_url = f"https://{device['host']}:8443/api/v2/monitor/system/config/backup?scope=global&destination=file"
    headers = {
        'Authorization': f"Bearer {device['apiKey']}"
    }
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup = f"{backup_path}/{device['host']}_{timestamp}.conf"
    try:
        resp = requests.request('GET', api_url, headers=headers, verify=False)
        with open(backup, 'wb') as f:
            f.write(resp.content)
        with open(logging, 'a') as f:
            f.write(f"---\n\nSuccessfully run configuration backup on {device['host']}\n\n")
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as error:
        with open(logging, 'a') as f:
            f.write(f"---\n\nFailed to run configuration backup on {device['host']}\n\n")
            f.write(f"{error}\n\n")
        pass
