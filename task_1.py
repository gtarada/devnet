# -*- coding: utf-8 -*-

import re
import time

import yaml
from netmiko import (ConnectHandler, NetMikoAuthenticationException,
                     NetMikoTimeoutException)


def get_config_backup(device, hostname):

    result = device.send_command('sh run')

    with open('./backup/' + hostname + '_' + time.strftime("%Y-%m-%d") + '.ios', 'w') as backup_file:
        backup_file.write(result)

    return None


def check_cdp(device):

    result = device.send_command('show cdp neighbors')
    if re.search(r'CDP is not enabled', result, re.MULTILINE):
        cdp = 'CDP is OFF'
        peers = ''
    else:
        cdp = 'CDP is ON'
        matches_count = len([x for x in re.finditer(
            r'\S+\s+\S+ \S+\s+\d+', result, re.MULTILINE)])
        peers = ', ' + str(matches_count) + ' peers'

    return [cdp + peers]


def check_software_version(device):

    result = device.send_command('show version')

    regex = r'Cisco.*?\((\S+)\), Version|isco (\S+).*?processor'

    for match in re.finditer(regex, result, re.MULTILINE):
        if match.group(1):
            software_version = match.group(1)
        if match.group(2):
            platform = match.group(2)
    if software_version.find('NPE') > -1:
        pe = 'NPE'
    else:
        pe = 'PE'

    return [platform, software_version, pe]


def configure_ntp(device):

    config_lines = [
        'clock timezone GMT 0 0',
        'ntp server 192.168.100.4'
    ]

    clock = 'Clock not sync'

    result = device.send_command('ping 192.168.100.4')
    if re.search(r'Success rate is 100', result, re.MULTILINE):
        result = device.send_config_set(config_lines)
        if not re.search(r'Invalid input detected', result, re.MULTILINE):
            result = device.send_command('wr')
            result = device.send_command('show ntp status')
            match = re.search(r'Clock is (\S+), stratum', result, re.MULTILINE)
            if match:
                if match.group(1) == 'synchronized':
                    clock = 'Clock in sync'

    return [clock]


def check_devices(devices):

    for device_params in devices:
        try:
            with ConnectHandler(**device_params) as ssh:
                ssh.enable()
                hostname = ssh.find_prompt()[:-1]
                get_config_backup(ssh, hostname)
                output = [hostname]
                output += check_software_version(ssh)
                output += check_cdp(ssh)
                output += configure_ntp(ssh)
                print('|'.join(output))
        except (NetMikoAuthenticationException, NetMikoTimeoutException) as error_message:
            print(error_message)

    return None


if __name__ == '__main__':
    with open("devices.yaml") as devices_file:
        check_devices(yaml.safe_load(devices_file))
