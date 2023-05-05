import socket
import exactTime

TIME_REQUEST = b"time"
HOST = '127.0.0.1'
PORT = 123
BUF_LEN = 1024


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print("Starting up server on % s port % s" % (HOST, PORT))

        while True:
            print("Waiting to receive message from client")

            try:
                data, address = s.recvfrom(BUF_LEN)

                print("received %s bytes from % s" % (len(data), address))

                if data == TIME_REQUEST:
                    print("Data: TIME_REQUEST")
                    res = exactTime.get_exact_time()
                    sent = s.sendto(res, address)
                    print("sent %s bytes back to % s" % (sent, address))
            except KeyboardInterrupt:
                s.close()
                print("closing server")
                break


if __name__ == "__main__":
    main()
