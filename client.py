import socket
import struct


def start_client(server_ip):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, 12345))

        while True:
            data = s.recv(1024).decode()
            if data == "EOD":  # if empty data or EOD is sent, terminate connection.
                break

            print(data)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python client.py <server_ip>")
        sys.exit(1)

    start_client(sys.argv[1])
