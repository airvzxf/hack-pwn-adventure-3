#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Create a Proxy which intercept the network sockets with specific IP's and Port's. This proxy working for client and the
server. Also it is running in threads to improve the performance and catch all the requests and responses.

This code is partially taken bye LiveOverflow/PwnAdventure3 (https://github.com/LiveOverflow/PwnAdventure3) under the
GPL-3.0 License
"""
from importlib import reload
from logging import debug, basicConfig, DEBUG
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread

import core.parser
from core.queue import Queue


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
        self.name = f'Server -> Client [{port}]'
        self._running = True
        self.client = None
        self.port = port
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.connect((host, port))

    def terminate(self) -> None:
        """
        Stop the execution of the current thread proxy.

        :rtype: None
        """
        self._running = False

    def run(self) -> None:
        """
        Start the execution of the proxy.
        Run in a new thread.

        :rtype: None
        """
        while self._running:
            data: bytes = self.server.recv(4096)
            if data:
                try:
                    reload(core.parser)
                    parse = core.parser.Parse(data)
                    if len(Queue.CLIENT_QUEUE) > 0:
                        packet: bytes = Queue.CLIENT_QUEUE.pop()
                        print(f'--*-- Send to client: {packet.hex()}')
                        self.client.sendall(packet)
                    new_data = parse.server(self.port)
                except Exception as e:
                    new_data = data
                    print(f'ERROR: server[{self.port}]: {e}')
                    print(f'       -> {data.hex()}')
                    debug(f'ERROR: server[{self.port}]: {e}')
                    debug(f'       -> {data.hex()}')
                self.client.sendall(new_data)
        self.server.close()


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
        self.name = f'Client -> Server [{port}]'
        self._running = True
        self.server = None
        self.port = port
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        # Waiting for a connection
        self.client, addr = sock.accept()

    def terminate(self) -> None:
        """
        Stop the execution of the current thread proxy.

        :rtype: None
        """
        self._running = False

    def run(self) -> None:
        """
        Start the execution of the proxy.
        Run in a new thread.

        :rtype: None
        """
        while self._running:
            data = self.client.recv(4096)
            if data:
                try:
                    reload(core.parser)
                    parse = core.parser.Parse(data)
                    if len(Queue.SERVER_QUEUE) > 0:
                        packet: bytes = Queue.SERVER_QUEUE.pop()
                        print(f'--*-- Send to server: {packet.hex()}')
                        self.server.sendall(packet)
                    new_data = parse.client(self.port)
                except Exception as e:
                    new_data = data
                    print(f'ERROR: client[{self.port}]: {e}')
                    print(f'       -> {data.hex()}')
                    debug(f'ERROR: client[{self.port}]: {e}')
                    debug(f'       -> {data.hex()}')
                self.server.sendall(new_data)
        self.client.close()


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
        self.name = f'Proxy [{port}]'
        self.from_host = from_host
        self.to_host = to_host
        self.port = port
        self.running = False
        self._running = True
        basicConfig(filename='./debug.log', filemode='w', level=DEBUG, format='%(message)s')

    def run(self) -> None:
        """
        Start the execution of the proxy.
        Run in a new thread.

        :rtype: None
        """
        connection_thread = []
        while self._running:
            print(f'Proxy [{self.port}]: Setting up')
            client_to_server = ClientToServer(self.from_host, self.port)
            server_to_client = ServerToClient(self.to_host, self.port)

            print(f'Proxy [{self.port}]: Connection established')
            client_to_server.server = server_to_client.server
            server_to_client.client = client_to_server.client
            self.running = True

            if connection_thread:
                client_thread, server_thread = connection_thread.pop()
                client_thread.terminate()
                server_thread.terminate()

            client_to_server.start()
            server_to_client.start()
            connection_thread.append((client_to_server, server_to_client))

        if connection_thread:
            client_thread, server_thread = connection_thread.pop()
            client_thread.terminate()
            server_thread.terminate()
