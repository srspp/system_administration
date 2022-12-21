import re
import sys

'''
Поиск в файле dhcpd.leases активных аренд.
'''


def main():
    try:
        filename = sys.argv[1]
    except IndexError:
        print('The filename was not specified.\nUsage: dhcp_leases_show.py path/to/file/dhcpd.leases')
        sys.exit(1)

    try:
        with open(filename, 'r') as leases:
            content = leases.read()

            '''
            lease ([0-9.]+) { -- подстрока с IP-адресом.
            [^}]+(active) -- в начале строки нет символа "}" и есть подстрока "active".
            [^}]+hardware ethernet ([:a-f0-9]+); -- в начале строки нет символа "}" и
            есть подстрока "hardware ethernet" за которой следует МАС-дрес.
            '''
            matches = re.findall("lease ([0-9.]+) {[^}]+(active)[^}]+hardware ethernet ([:a-f0-9]+);", content)

            for i in range(len(matches)):
                print('IP address: {:14} MAC address:{:>18}'.format(matches[i][0], matches[i][2]))

    except FileNotFoundError:
        print('File not found')
        sys.exit(2)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
