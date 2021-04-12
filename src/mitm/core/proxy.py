#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Create a Proxy which intercept the network sockets with specific IP's and Port's. This proxy working for client and the
server. Also it is running in threads to improve the performance and catch all the requests and responses.

This code is partially taken bye LiveOverflow/PwnAdventure3 (https://github.com/LiveOverflow/PwnAdventure3) under the
GPL-3.0 License
"""
from logging import basicConfig, DEBUG
from threading import Thread

from core.client_to_server import ClientToServer
from core.server_to_client import ServerToClient


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
