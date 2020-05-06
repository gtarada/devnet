# -*- coding: utf-8 -*-

from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
# from nornir.core.filter import F
from pprint import pp
from draw_topology import draw_topology

with InitNornir(config_file='config.yaml') as nr:
    lldp_nei = nr.run(
        netmiko_send_command, command_string='show lldp neighbors detail', use_genie=True)
    topology_dict = {}
    for device, response in lldp_nei.items():
        # print(device)
        # pp(response[0].result)
        try:
            for interface in response[0].result['interfaces'].keys():
                # pp(interface)
                # pp(response[0].result['interfaces'][interface]['port_id'])
                for nei_interface in response[0].result['interfaces'][interface]['port_id'].keys():
                    # pp(nei_interface)
                    # pp(response[0].result['interfaces'][interface]['port_id'][nei_interface]['neighbors'])
                    for nei_hostname in response[0].result['interfaces'][interface]['port_id'][nei_interface]['neighbors'].keys():
                        try:
                            if topology_dict[(nei_hostname, nei_interface)]:
                                pass
                        except KeyError:
                            topology_dict[(device, interface)] = (nei_hostname, nei_interface)
        except TypeError:
            pass

    draw_topology(topology_dict)
