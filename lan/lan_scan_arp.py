#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import subprocess
import ipaddress
import sys
import re
from mac_vendor_lookup import MacLookup

def get_hardware_info(host_address):

    '''
    Отправка широковещательного arp запроса и поиск производителя оборудования
    Модуль mac-vendor-lookup ищет информацию в файле ~/.cache/mac-vendors.txt
    '''
    # Отправка arp запроса
    arping_result = subprocess.run(['arping', '-c', '3', '-f', host_address], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, encoding="utf-8")
    # arping_result = subprocess.run(['arping', '-c', '3', '-f', '-I', 'wlan0', host_address], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, encoding="utf-8")
    if arping_result.returncode == 0:
        try:
            # Поиск производителя оборудования
            mac_address = re.findall(r'\w{2}\:\w{2}\:\w{2}\:\w{2}\:\w{2}\:\w{2}', arping_result.stdout, re.MULTILINE)
            vendor_name = MacLookup().lookup(mac_address[0])
            if 'not registered' in vendor_name:
                vendor_name='not found'
            else:
                vendor_name = MacLookup().lookup(mac_address[0])
        except Exception:
                vendor_name = 'not found'

        print('Host: {:15} available    МАС address: {} Vendor: {}'.format(
            host_address, mac_address[0], vendor_name))
    else:
        print('Host: {:15} unavailable'.format(host_address))


def main():

    # Обновление списка производителей, занимает некоторое время
    # MacLookup().update_vendors()

    try:
        host_address = sys.argv[1]
    except Exception:
        print('Usage: {} IP address or {} IP address/mask'.format(sys.argv[0], sys.argv[0]))
        print('For example: {} 192.168.0.1 or {} 192.168.0.0/24'.format(sys.argv[0], sys.argv[0]))
        sys.exit(1)

    # Если в качестве аргумента передается адрес сети/маска
    if host_address.find('/') > 0:
        try:
            ipaddress.ip_network(host_address)
        except ValueError:
            print('Invalid network address')
            sys.exit(1)

        subnet = ipaddress.ip_network(host_address)

        # Перебираются только адреса хостов, без адреса сети и широковещательного адреса
        for ip in range(1, (subnet.num_addresses - 1)):
            get_hardware_info(str(subnet[ip]))

    # Если в качестве аргумента передается одиночный IP-адрес
    else:
        try:
            ipaddress.ip_address(host_address)
        except ValueError:
            print('Invalid IP address')
            sys.exit(1)

        get_hardware_info(host_address)


if __name__ == '__main__':

    # Обработка <Ctrl>+<C>
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
