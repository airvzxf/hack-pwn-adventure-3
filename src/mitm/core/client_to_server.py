#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Manage the connection from the Client to the Server.

This code is partially taken bye LiveOverflow/PwnAdventure3 (https://github.com/LiveOverflow/PwnAdventure3) under the
GPL-3.0 License
"""
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread

from core.package import Package


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
        self.package = None
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
        self.package.terminate()

    def run(self) -> None:
        """
        Start the execution of the proxy.
        Run in a new thread.

        :rtype: None
        """
        self.package = Package(False, self.client, self.server, self.port)
        self.package.start()
