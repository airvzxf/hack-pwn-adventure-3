#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Create a Proxy which intercept the network sockets with specific IP's and Port's. This proxy working for client and the
server. Also it is running in threads to improve the performance and catch all the requests and responses.

This code is partially taken bye LiveOverflow/PwnAdventure3 (https://github.com/LiveOverflow/PwnAdventure3) under the
GPL-3.0 License
"""
import logging
import socket
from threading import Thread

from core.parser import Parse


class ServerToClient(Thread):
    """
    Get, analyze and modify the data from server and send to the client.
    """

    def __init__(self, host: str, port: int) -> None:
        """
        Constructor which init the class.

        :type host: str
        :param host: The server's IP.

        :type port: int
        :param port: The number of the port for the communication.

        :rtype: ServerToClient
        :return: The object instanced of this class.
        """
        super(ServerToClient, self).__init__()
        self.client = None
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))

    def run(self) -> None:
        """
        Start the execution of the proxy.
        Run in a new thread.

        :rtype: None
        """
        while True:
            data: bytes = self.server.recv(4096)
            if data:
                try:
                    Parse(data, self.port, 'server')
                except Exception as e:
                    print(f'ERROR: server[{self.port}]: {e}')
                    print(f'ERROR: server[{self.port}]: {data.hex()}')
                    logging.debug(f'ERROR: server[{self.port}]: {e}')
                    logging.debug(f'ERROR: server[{self.port}]: {data.hex()}')
                self.client.sendall(data)


class ClientToServer(Thread):
    """
    Get, analyze and modify the data from client and send to the server.
    """

    def __init__(self, host: str, port: int) -> None:
        """
        Constructor which init the class.

        :type host: str
        :param host: The client's IP.

        :type port: int
        :param port: The number of the port for the communication.

        :rtype: ClientToServer
        :return: The object instanced of this class.
        """
        super(ClientToServer, self).__init__()
        self.server = None
        self.port = port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        # Waiting for a connection
        self.client, addr = sock.accept()

    def run(self) -> None:
        """
        Start the execution of the proxy.
        Run in a new thread.

        :rtype: None
        """
        while True:
            data = self.client.recv(4096)
            if data:
                try:
                    Parse(data, self.port, 'client')
                except Exception as e:
                    print(f'ERROR: client[{self.port}]: {e}')
                    print(f'ERROR: client[{self.port}]: {data.hex()}')
                    logging.debug(f'ERROR: client[{self.port}]: {e}')
                    logging.debug(f'ERROR: client[{self.port}]: {data.hex()}')
                self.server.sendall(data)


class Proxy(Thread):
    """
    Start the communication between both, the client and server.
    """

    def __init__(self, from_host: str, to_host: str, port: int) -> None:
        """
        Constructor which init the class.

        :type from_host: str
        :param from_host: The IP which is received by the client. Zeros means any IP (0.0.0.0)

        :type to_host: str
        :param to_host: The IP which is send to the Server.

        :type port: int
        :param port: The number of the port for the communication.

        :rtype: Proxy
        :return: The object instanced of this class.
        """
        super(Proxy, self).__init__()
        self.from_host = from_host
        self.to_host = to_host
        self.port = port
        logging.basicConfig(filename='./debug.log', filemode='w', level=logging.DEBUG, format='%(message)s')

    def run(self) -> None:
        """
        Start the execution of the proxy.
        Run in a new thread.

        :rtype: None
        """
        while True:
            print(f'[proxy({self.port})] setting up')
            client_to_server = ClientToServer(self.from_host, self.port)
            server_to_client = ServerToClient(self.to_host, self.port)

            print(f'[proxy({self.port})] connection established')
            client_to_server.server = server_to_client.server
            server_to_client.client = client_to_server.client

            client_to_server.start()
            server_to_client.start()
