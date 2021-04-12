#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Manage the connection from the Server to the Client.

This code is partially taken bye LiveOverflow/PwnAdventure3 (https://github.com/LiveOverflow/PwnAdventure3) under the
GPL-3.0 License
"""
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from core.package import Package


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
        self.package = None

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
        self.package = Package(True, self.server, self.client, self.port)
        self.package.start()
