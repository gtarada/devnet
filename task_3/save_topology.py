# -*- coding: utf-8 -*-

import csv

from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command

from draw_topology import draw_topology


def search_lldp_topology():
    """
    Функция возвращает словарь с информацией о физических соединениях, найденных с помощью LLDP
    """
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
    our_topology = search_lldp_topology()
    # Информация о соединениях записывается в csv файл
    with open('topology.csv', 'w') as f:
        writer = csv.writer(f)
        for row in our_topology.keys():
            writer.writerow(row + our_topology[row])
    # Информация о топологии в графичском виде записывается в svg файл
    draw_topology(our_topology)
