import socket
import re

from dnslib import DNSRecord

HOST = '127.0.0.1'
PORT = 53
BUF_LEN = 1024


def main():
    # 5.255.255.242
    line = input()
    q_type = 'A'
    if bool(re.match(re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'), line)):
        q_type = 'PTR'
        lines = line.split('.')
        # преобразование в обратный DNS-запрос
        # 5.255.255.242 -> 242.255.255.5.in-addr.arpa
        line = lines[3] + '.' + lines[2] + '.' + lines[1] + '.' + lines[0] + '.in-addr.arpa'

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.settimeout(5)
            # создаем пакет DNS запроса
            data = DNSRecord.question(line, q_type).pack()
            s.sendto(data, (HOST, PORT))

            data, address = s.recvfrom(BUF_LEN)
            print(f"Ответ получен от: %s:%s" % (address[0], address[1]))
            print(data.decode('utf-8'))
        finally:
            s.close()


if __name__ == "__main__":
    main()
