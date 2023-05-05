import socket

TIME_REQUEST = "time"
HOST = '127.0.0.1'
PORT = 123
BUF_LEN = 1024


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.sendto(TIME_REQUEST.encode('utf-8'), (HOST, PORT))

            data, server = s.recvfrom(BUF_LEN)
            print(f"Response received from: %s:%s" % (server[0], server[1]))
            print(data.decode("utf-8"))
        finally:
            s.close()


if __name__ == "__main__":
    main()
