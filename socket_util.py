import socket


def connect_socket(host, port):
    """ create socket and connect to adb server """
    client = socket.socket()
    client.connect((host, port))
    return client


def adb_encode_data(data, encoding):
    byte_data = data.encode(encoding)
    byte_length = "{0:04X}".format(len(byte_data)).encode(encoding)
    return byte_length + byte_data


def read_all_content(target_socket):
    result = b''
    while True:
        buf = target_socket.recv(1024)
        if not len(buf):
            return result
        result += buf
