import socket
import struct


def unpack_message(s):
    """
        Unpacks message sent from server which should have a 4 byte message length header.

    :param s: client socket connection
    :return: decoded message from server
    """
    header = s.recv(4)  # get the message header (4 bytes)
    msg_len = struct.unpack('!I', header)[0]  # unpack header, convert to integer -> msg_length
    return s.recv(msg_len).decode()  # decode rest of the message until message length.


def start_client(server_ip):
    """
        Connects to sys_arg'd server_ip at port 12345 as a TCP connection. Then, starts receving data from server until
        an EOD message is sent.

    :param server_ip: ip to connect
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, 12345))

        while True:
            data = unpack_message(s)
            if data == "EOD":  # if EOD is sent, terminate connection.
                print("EOD sent! Terminating connection...")
                break

            print(data)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python client.py <server_ip>")
        sys.exit(1)

    start_client(sys.argv[1])
