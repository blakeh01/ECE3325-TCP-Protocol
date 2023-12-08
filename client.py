import socket
import struct
import hashlib


def unpack_message(s):
    """
        Unpacks message sent from server which should have a 4 byte message length header and 32 byte checksum.

    :param s: client socket connection
    :return: decoded message from server
    """
    header = s.recv(4)  # get 4 byte header which will be length of message
    msg_len = struct.unpack('!I', header)[0]  # ^ unpacks from struct lib
    data = s.recv(msg_len).decode()  # use length to receive message
    checksum = s.recv(32).decode()  # get 32 byte checksum
    return data, checksum  # return the data and checksum


def calculate_checksum(data):
    """
    Uses hashlib to calculate an md5 checksum.

    :param data: data to create checksum for
    :return: checksum
    """
    md5 = hashlib.md5()
    md5.update(data.encode())
    return md5.hexdigest()


def send_acknowledgement(s, message="OK"):
    """
    Sends an acknowledgement message to the server.
    """
    s.sendall(message.encode())


def start_client(server_ip):
    """
        Connects to sys_arg'd server_ip at port 12345 as a TCP connection. Then, starts receiving data from server until
        an EOD message is sent.

    :param server_ip: ip to connect
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, 12345))  #connect to passed in server IP on port 12345

        while True:
            data, checksum = unpack_message(s)  # unpack the message (which also receives message)

            # Verify checksum
            if calculate_checksum(data) == checksum:
                print(data)
                send_acknowledgement(s)
            else:
                print("Checksum mismatch. Data may be corrupted.")

            # If EOD, all data has been sent. break out and close connection.
            if data == "EOD":
                print("EOD received! Terminating connection...")
                break


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python client.py <server_ip>")
        sys.exit(1)

    start_client(sys.argv[1])
