import datetime, requests, time, json
from urllib3.exceptions import InsecureRequestWarning

def backup_f5(device,backup_path,logging):
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    session = requests.Session()
    session.timeout = '30'
    session.headers.update({'Content-Type': 'application/json'})
    session.auth = (device['username'], device['password'])
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    ucs_file = f"{device['host']}_{timestamp}.ucs"
    backup = f"{backup_path}/{ucs_file}"
    try:
        # create a job for ucs archive
        url_ucs = f"https://{device['host']}/mgmt/tm/task/sys/ucs"
        payload = {
            'name': f"/var/local/ucs/{ucs_file}",
            "command": "save"
        }
        create_ucs = session.post(url_ucs, json.dumps(payload), verify=False).json()
        taskId = create_ucs['_taskId']
        # validate the task to run job
        url_task = f"https://{device['host']}/mgmt/tm/task/sys/ucs/{taskId}"
        payload = {"_taskState":"VALIDATING"}
        session.put(url_task, json.dumps(payload), verify=False)
        task_state = ''
        while task_state != 'COMPLETED':
            time.sleep(10)
            resp = session.get(url_task, verify=False).json()
            task_state = resp['_taskState']
            if task_state == 'COMPLETED':
                break
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as error:
        with open(logging, 'a') as f:
            f.write(f"---\n\nFailed to run configuration backup on {device['host']}\n\n")
            f.write(f"{error}\n\n")
        pass
    else:
        url_download = f"https://{device['host']}/mgmt/shared/file-transfer/ucs-downloads/{ucs_file}"
        chunk_size = 512 * 1024
        headers = {
            'Content-Type': 'application/octet-stream',
        }
        with open(backup, 'wb') as f:
            start = 0
            end = chunk_size - 1
            size = 0
            current_bytes = 0
    
            while True:
                content_range = "%s-%s/%s" % (start, end, size)
                headers['Content-Range'] = content_range

                resp = requests.get(url_download,
                                    auth=(device['username'], device['password']),
                                    headers=headers,
                                    verify=False,
                                    stream=True)
    
                if resp.status_code == 200:
                    if size > 0:
                        current_bytes += chunk_size
                        for chunk in resp.iter_content(chunk_size):
                            f.write(chunk)
                    if end == size:
                        break

                crange = resp.headers['Content-Range']

                # Determine the total number of bytes to read
                if size == 0:
                    size = int(crange.split('/')[-1]) - 1
                    if chunk_size > size:
                        end = size
    
                    # ...and pass on the rest of the code
                    continue
    
                start += chunk_size
    
                if (current_bytes + chunk_size) > size:
                    end = size
                else:
                    end = start + chunk_size - 1

        # delete ucs file
        url_file = f"https://{device['host']}/mgmt/tm/sys/ucs/{ucs_file}"
        session.delete(url_file, verify=False)
        
        with open(logging, 'a') as f:
            f.write(f"---\n\nSuccessfully run configuration backup on {device['host']}\n\n")
