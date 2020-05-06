# -*- coding: utf-8 -*-

from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command

from draw_topology import draw_topology


def search_lldp_topology():

    topology_dict = {}

    with InitNornir(config_file='config.yaml') as nr:
        lldp_nei = nr.run(
            netmiko_send_command, command_string='show lldp neighbors detail', use_genie=True)
        for device, response in lldp_nei.items():
            try:
                for interface in response[0].result['interfaces'].keys():
                    for nei_interface in response[0].result['interfaces'][interface]['port_id'].keys():
                        for nei_hostname in response[0].result['interfaces'][interface]['port_id'][nei_interface]['neighbors'].keys():
                            try:
                                if topology_dict[(nei_hostname, nei_interface)]:
                                    pass
                            except KeyError:
                                topology_dict[(device, interface)] = (
                                    nei_hostname, nei_interface)
            except TypeError:
                pass

    return topology_dict


if __name__ == '__main__':
    draw_topology(search_lldp_topology())
