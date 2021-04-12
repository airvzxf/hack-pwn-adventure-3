#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Handle the package coming from the source and send to the destination. In the middle of this task the packages
can modify as you wish.

This code is partially taken bye LiveOverflow/PwnAdventure3 (https://github.com/LiveOverflow/PwnAdventure3) under the
GPL-3.0 License
"""
from importlib import reload
from logging import debug
from socket import socket

import core.parser
from core.queue import Queue


class Package:
    """
    Manage the packages. It could be receive, send and inject.
    """

    def __init__(self, is_server: bool, source: socket, destination: socket, port: int) -> None:
        """
        Constructor which init the class.

        :type is_server: bool
        :param is_server: True means that it is sending packages from the Client to the Server. Otherwise it is false.

        :type source: socket
        :param source: Object with the source connection.

        :type destination: socket
        :param destination: Object with the destination connection.

        :type port: int
        :param port: The number of the port for the communication.

        :rtype: Package
        :return: The object instanced of this class.
        """
        self.running = True
        self.is_server = is_server
        self.source = source
        self.destination = destination
        self.port = port

    def terminate(self) -> None:
        """
        Stop the execution.

        :rtype: None
        """
        self.running = False

    def start(self) -> None:
        """
        Handle the packages.

        :rtype: None
        """
        if self.is_server:
            destination = 'client'
            queue = Queue.CLIENT_QUEUE
        else:
            destination = 'server'
            queue = Queue.SERVER_QUEUE

        while self.running:
            data: bytes = self.source.recv(4096)
            if data:
                try:
                    reload(core.parser)
                    parse = core.parser.Parse(data)
                    if len(queue) > 0:
                        packet: bytes = queue.pop()
                        print(f'--*-- Send to {destination}: {packet.hex()}')
                        self.destination.sendall(packet)
                    parse.server(self.port)
                except Exception as e:
                    print(f'ERROR: server[{self.port}]: {e}')
                    print(f'       -> {data.hex()}')
                    debug(f'ERROR: server[{self.port}]: {e}')
                    debug(f'       -> {data.hex()}')
                self.destination.sendall(data)
        self.source.close()
