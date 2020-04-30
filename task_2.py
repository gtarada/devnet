# -*- coding: utf-8 -*-

from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.core.filter import F
from pprint import pprint

with InitNornir(config_file='config.yaml') as nr:
    switches = nr.filter(F(name__contains="SW"))
    interf_switchp = switches.run(netmiko_send_command, command_string='show interfaces switchport', use_genie=True)
    access_interfaces = {}
    for device, response in interf_switchp.items():
        access_interfaces[device] = []
        for interface in response[0].result.keys():
            if response[0].result[interface]['operational_mode'] == 'static access':
                access_interfaces[device].append(interface)
    mac_addr_table = switches.run(netmiko_send_command, command_string='show mac address-table', use_genie=True)
    for device, response in mac_addr_table.items():
        for vlan in response[0].result['mac_table']['vlans']:
            for mac_address in response[0].result['mac_table']['vlans'][vlan]['mac_addresses'].keys():
                for interface in response[0].result['mac_table']['vlans'][vlan]['mac_addresses'][mac_address]['interfaces'].keys():
                    if interface in access_interfaces[device]:
                        print((device, interface, mac_address))
