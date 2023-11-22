import socket
import struct
from datetime import datetime

HOST = ""  # no host means listen on all interfaces
PORT = 12345
QUEUE_MAX = 1


def parse_data(line):
    """
        Takes in a line from the Excel, checks to see if its valid data, then processes it into a more readable format.

    :param line: raw line string from read-in Excel.
    :return:
    """
    fields = line.strip().split(',')  # split read in line by comma (delimiter used by excel)

    if len(fields) != 10 and all(fields):  # ensure this is not a header line and all data is available
        return None

    # check to ensure that the longitude field has legit data. If not, we know this line is not data, so skip.
    try:
        float(fields[1])
    except ValueError:
        return None

    timestamp = datetime.strptime(fields[0], '%Y%m%d%H%M%S')
    formatted_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    return {
        'time': formatted_time,
        'longitude': fields[1],
        'latitude': fields[2],
        'wsr_id': fields[3],
        'cell_id': fields[4],
        'range': fields[5],
        'azimuth': fields[6],
        'sevprob': fields[7],
        'prob': fields[8],
        'maxsize': fields[9]
    }


def pack_message(data):
    """
        Packs the data into a TCP connection ready message.
        Includes a header that is the length of the message for reconstruction @ the client.

        This is the core of the custom protocol:
            [HEADER] [DATA]

    :param data: data being snet
    :return: data with header.
    """
    header = struct.pack('!I', len(data))
    return header + data.encode()


def start_server(file_name):
    """
        Starts a TCP connection on HOST, PORT. waits for a client to connect before sending processed data
        from file located at 'file_name'. This file is expected to be an Excel and have 10 elements of data.

    :param file_name: filename of the data to be sent
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))

        s.listen(QUEUE_MAX)  # allowing incoming connections with a queue of QUEUE_MAX
        print("Server listening on port 12345...")
        client_socket, client_address = s.accept()  # blocking statement waiting for a client connection
        print(f"Connection established with {client_address}")

        with open(file_name, 'r') as file:  # open file name in readonly mode.
            for line in file:  # for every line in the file
                processed_data = parse_data(line)  # parse excel line and process it to send
                if processed_data:
                    client_socket.sendall(pack_message(str(processed_data)))  # encode data and send to client

        client_socket.sendall(pack_message('EOD'))  # once all data has been processed, this end of data line will be sent
        print("All data has been sent to client.")


if __name__ == "__main__":
    import sys

    # get command line arguments, pass file name to start_server func
    if len(sys.argv) != 2:
        print("Usage: python server.py <file_name>")
        sys.exit(1)

    start_server(sys.argv[1])
