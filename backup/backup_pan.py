import datetime, requests, xmltodict
from urllib3.exceptions import InsecureRequestWarning

def backup_pan(device,backup_path,logging):
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    url_key = f"https://{device['host']}/api/?type=keygen&user={device['username']}&password={device['password']}"
    try:
        # get API key from PAN
        resp = requests.request("GET", url_key, verify=False)
        resp.raise_for_status()
        respDict = xmltodict.parse(resp.content)
        apiKey = respDict['response']['result']['key']
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as error:
        with open(logging, 'a') as f:
            f.write(f"---\n\nFailed to run configuration backup on {device['host']}\n\n")
            f.write(f"{error}\n\n")
        pass
    else:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        backup = f"{backup_path}/device-state_{device['host']}_{timestamp}.tgz"
        # export device-state from PAN
        url_api = f"https://{device['host']}/api/?type=export&category=device-state&key={apiKey}"
        resp = requests.request("GET", url_api, stream=True, verify=False)
        if resp.status_code == 200:
            with open(backup, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            with open(logging, 'a') as f:
                f.write(f"---\n\nSuccessfully run configuration backup on {device['host']}\n\n")
        else:
            with open(logging, 'a') as f:
                f.write(f"---\n\nFailed to run configuration backup on {device['host']}\n\n")
