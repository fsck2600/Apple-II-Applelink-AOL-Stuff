#!/usr/bin/env python
import serial
import socket
import sys
import select
﻿
def winreadline(serial_port):
    data = ""
    done = False
    while not done:
        byte = serial_port.read(1)
        sys.stdout.write(byte.decode('utf-8'))
        data += byte.decode('utf-8')
﻿
        if byte == b"\r":
            done = True
﻿
    return data.rstrip("\r")
﻿
def handle_client(client_socket, serial_port):
    print(f"Accepted connection from {client_socket.getpeername()}")
﻿
    try:
        in_pipe = [serial_port, client_socket]
        out_pipe = []
        oob_pipe = []
﻿
        while select.select(in_pipe, out_pipe, oob_pipe, 0)[0]:
            if serial_port in in_pipe:
                data = serial_port.read(1)
                sys.stdout.write(data.decode('utf-8'))
                client_socket.sendall(data)
            if client_socket in in_pipe:
                data = client_socket.recv(1024)
                serial_port.write(data)
﻿
    except serial.SerialException as e:
        print(f"Error reading/writing from/to {ttyUSB0_port}: {e}")
    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        print("Closing connection...")
        client_socket.close()
﻿
if __name__ == "__main__":
    ttyUSB0_port = '/dev/ttyUSB0'
    tcp_ip = "127.0.0.1"
    tcp_port = 12345
﻿
    try:
        # Open the serial port
        serial_port = serial.Serial(ttyUSB0_port, baudrate=9600, timeout=0)
﻿
        # Create a TCP/IP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((tcp_ip, tcp_port))
        server_socket.listen(1)
﻿
        print(f"Listening on {tcp_ip}:{tcp_port} for incoming connections...")
﻿
        while True:
            # Wait for a connection
            print("Waiting for connection...")
            client_socket, client_address = server_socket.accept()
﻿
            # Perform ANSNet protocol
            try:
                in_pipe = [client_socket]
                out_pipe = []
                oob_pipe = []
﻿
                while select.select(in_pipe, out_pipe, oob_pipe, 0)[0]:
                    if client_socket in in_pipe:
                        data = client_socket.recv(1024).decode('utf-8')
                        if "ANSNet" in data:
                            print("ANSNet")
                            print("LOGIN")
                            client_socket.sendall("ANSNet\r\nLOGIN".encode('utf-8'))
                            winreadline(serial_port)
                            client_socket.sendall("\r\nCONNECTED\r\n".encode('utf-8'))
﻿
            except socket.error as e:
                print(f"Socket error: {e}")
            finally:
                handle_client(client_socket, serial_port)
﻿
    except (serial.SerialException, socket.error) as e:
        print(f"Error: {e}")
    finally:
        serial_port.close()
        server_socket.close()```
