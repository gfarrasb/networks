import json      
import requests
import tabulate

requests.packages.urllib3.disable_warnings()  
api_url = "https://sandboxapicem.cisco.com/api/v1/"

def get_ticket():
    global api_url
    api_url_ticket=api_url + "ticket"
    headers = {
        "content-type": "application/json"
    }
    body_json = {
        "username": "devnetuser",
        "password": "Cisco123!"
    }
    resp = requests.post(api_url_ticket, json.dumps(body_json), headers=headers, verify=False)
    print("Ticket request status: ", resp.status_code)  # display response code
    response_json = resp.json()
    serviceTicket = response_json["response"]["serviceTicket"]
    return serviceTicket

def print_hosts():
    global api_url
    api_url_hosts = api_url + "network-device"

    ticket = get_ticket()
    headers = {"content-type": "application/json", "X-Auth-Token": ticket}

    resp = requests.get(api_url_hosts, headers=headers, verify=False)
    print ("Status of /host request: ", resp.status_code)
    if resp.status_code != 200:
       raise Exception("Status code is not 200/OK. Resp text: " + resp.text)
    response_json = resp.json()
    print(response_json)
   
    host_list=[]
    i=0
    for item in response_json["response"]:
        i+=1
        host = [ i, item["type"], item["managementIpAddress"] ]
        host_list.append( host )
    table_header = [ 'number', 'type', 'host IP' ]
    print( tabulate.tabulate(host_list, table_header) )


print_hosts()



