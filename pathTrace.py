"""
Path Trace Student Work File
APIC-EM Workshop
October 15, 2017
"""
import json      
import requests
import tabulate
import time

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

# Get service ticket number using imported function
ticket = get_ticket()
# Create headers for requests to the API
#headers = { "content-type": "application/json" }
headers = {"content-type": "application/json", "X-Auth-Token": ticket}


# ============================
# Section 3. Get the source and destination IP addresses for the Path Trace
# ============================

while True:
    #+++++++++++Add Values+++++++++++++++
    # Request user input for source IP address, e.g. "Please enter the source
    # IP address"
    s_ip = "10.2.1.22"
    d_ip = "10.1.12.20"
    #++++++++++++++++++++++++++++++++++++
    # Various error traps could be completed here - POSSIBLE CHALLENGE

    if s_ip != "" or d_ip != "":
        # this creates a python dictionary that will be converted to a JSON
        # object and posted
        path_data = {
            "sourceIP": s_ip,
            "destIP": d_ip
        }
        # Optional: Add statements that display the source and destination IP
        # addresses that will be used. And asks user to verify. Loop if not
        # verified by user.
        break  # Exit loop if values supplied
    else:
        print("\n\nYOU MUST ENTER IP ADDRESSES TO CONTINUE.\nUSE CTRL-C TO QUIT\n")
        continue  # Return to beginning of loop and repeat

#============================
# Section 4. Initiate the Path Trace and get the flowAnalysisId
#============================

#+++++++++++Add Values+++++++++++++++
# Post request to initiate Path Trace
# Make the request. Construct the post request to the API
#resp = requests.post(api_url + "flow-analysis", "{\"sourceIP\":\"10.1.15.117\",\"destIP\": \"10.1.12.20\"}", headers, verify=False)
print(path_data)
print(headers)
resp = requests.post(api_url + "flow-analysis", json.dumps(path_data), headers=headers, verify=False)
#resp = requests.post(api_url_ticket, json.dumps(body_json), headers=headers, verify=False)

# Inspect the return, get the Flow Analysis ID, put it into a variable
resp_json = resp.json()
print(resp_json)
flowAnalysisId = resp_json["response"]["flowAnalysisId"]
print("FLOW ANALYSIS ID: ", flowAnalysisId)

#============================
# Section 5. Check status of Path Trace request, output results when COMPLETED
#============================

#+++++++++++Add Values+++++++++++++++
# Add Flow Analysis ID to the endpoint URL in order to check the status of
# this specific path trace (e.g. https://a.b.c.d/api/v1/flow-analysis/2a014833-a99f-4067-8461-5dff58b2e1f2)
check_url = api_url +  "flow-analysis/" + flowAnalysisId
print(check_url)
#++++++++++++++++++++++++++++++++++++

# initialize variable to hold the status of the path trace
status = ""
checks = 1  # variable to increment within the while loop. Will trigger exit from loop after x iterations
while status != "COMPLETED":
    r = requests.get(check_url, headers=headers, verify=False)
    response_json = r.json()
    #+++++++++++Add Values+++++++++++++++
    status = response_json["response"]["request"]["status"] # Assign the value of the status of the path trace request from response_json
    #++++++++++++++++++++++++++++++++++++
    print("REQUEST STATUS: ", status)  # Print the status as the loop runs
    # wait one second before trying again
    time.sleep(1)
    if checks == 15:  # number of iterations before exit of loop; change depending on conditions
        # break the execution
        raise Exception("Number of status checks exceeds limit. Possible problem with Path Trace.!")
    elif status == "FAILED":
        # break the execution
        checks += 1
    

#============================
# Section 6. Display results
#============================

# Create required variables
#+++++++++++Add Values+++++++++++++++
# the source address for the trace, printed below
path_source = response_json["response"]["request"]["sourceIP"]
# the destination address for the trace, printed below
path_dest = response_json["response"]["request"]["destIP"]
# Assign the list of all network element dictionaries from response_json
print(response_json)
networkElementsInfo = response_json["response"]["networkElementsInfo"]
#+++++++++++++++++++++++++++++++++++++

all_devices = []     # A list variable to store the hosts and devices
device_no = 1  # this variable is an ordinal number for each device, incremented in the loop

# Iterate through returned Path Trace JSON and populate list of path
# information
for networkElement in networkElementsInfo:
    # test if the devices DOES NOT have a "name", absence of "name" identifies
    # an end host
    if "name" not in networkElement:  # assigns values to the variables for the hosts
        name = "Unnamed Host"
        ip = networkElement["ip"]
        egressInterfaceName = "UNKNOWN"
        ingressInterfaceName = "UNKNOWN"
    # if there is the "name" key, then it is an intermediary device
    else:  # assigns values to the variables for the intermediary devices
        name = networkElement["name"]
        ip = networkElement["ip"]
        if "egressInterface" in networkElement:  # not all intermediary devices have ingress and egress interfaces
            egressInterfaceName = networkElement["egressInterface"]["physicalInterface"]["name"]
        else:
            egressInterfaceName = "UNKNOWN"

        if "ingressInterface" in networkElement:
            ingressInterfaceName = networkElement["ingressInterface"]["physicalInterface"]["name"]
        else:
            ingressInterfaceName = "UNKNOWN"
    
    # create the list of info to be displayed
    device = [
                device_no,
                name,
                ip,
                ingressInterfaceName,
                egressInterfaceName
             ]
    # add this list of info for the device as a new line in this variable
    all_devices.append(device)
    device_no += 1  # increments the ordinal variable for the device in the list

# print the source and destination IPs for the trace
print("Path trace: \n Source: ", path_source, "\n Destination: ", path_dest)  
# print the table of devices in the path trace
print("List of devices on path:")
table_header = [
                "Item",
                "Name",
                "IP",
                "Ingress Int",
                "Egress Int"
               ]
print( tabulate.tabulate(all_devices, table_header) )  
