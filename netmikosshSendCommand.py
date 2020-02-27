from netmiko import Netmiko
from getpass import getpass

net_connect = Netmiko(
    "172.16.11.3",
    username="administrador",
    password="perprotegir",
    device_type="linux",
)

print(net_connect.find_prompt())

command = "ls"
output = net_connect.send_command(command)

net_connect.disconnect()
print(output)
