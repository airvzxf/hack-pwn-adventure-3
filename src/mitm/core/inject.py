#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Inject data in the main package.
"""
from logging import basicConfig, DEBUG, debug

from core.hack import Hack


class Inject:
    """
    Inject data in the current package.
    """

    def __init__(self) -> None:
        """
        Constructor which init the class.

        :rtype: None
        """
        basicConfig(filename='./debug.log', filemode='a', level=DEBUG, format='%(message)s')
        self.data = bytearray()
        self.pending = []

        self.retries = 1
        self.active = False
        self.working = False
        self.validation = bytearray()
        self.idx = ''
        self.destination = ''
        self.current_hack = ''
        self.fixed_position = bytearray()

    def run(self, data: bytes, destination: str) -> bytes:
        """
        Increment validate and update the data.

        :type data: bytes
        :param data: Raw data.

        :type destination: str
        :param destination: It refers to the network target could be client or server.

        :rtype: bytes
        :return: Return injected data.
        """
        self.data = data
        idx = self.data[:2].hex()

        if not self.active:
            return self.data

        if self.retries < 1:
            message = f'*** Injection: Not success {Hack.fire_balls}'
            print(message)
            debug(message)
            self._clean_state()

        if len(self.validation) > 0 and destination != self.destination:
            if self.data.find(self.validation) > -1:
                self._clean_state()
                message = f'*** Injection: Hacked {Hack.fire_balls}'
                print(message)
                debug(message)

        if destination == self.destination and idx == self.idx:
            self.retries -= 1

            if len(self.fixed_position) > 0:
                self.data = self.data[:2] + self.fixed_position + self.data[14:]

            self._execute_hack()
        return self.data

    def get_fire_balls(self, retries: int) -> None:
        """
        Inject package to get the fire balls magic weapon.

        :type retries: int
        :param retries: Number of times that it will send the injected package.

        :rtype: None
        """
        self.retries = retries
        self.active = True
        self.idx = '6d76'
        self.destination = 'server'
        self.fixed_position = b'\x34\x97\x2a\xc7' + b'\xf2\x6a\x5a\xc7' + b'\x66\xbc\xa1\x43'
        validation = '70751c00416368696576656d656e745f477265617442616c6c734f6646697265' \
                     '70751000477265617442616c6c734f6646697265'
        self.validation = bytearray.fromhex(validation)
        self.pending.append(Hack.fire_balls)

    def _clean_state(self) -> None:
        """
        Clean the class variables to return the initial state.

        :rtype: None
        """
        self.retries = 0
        self.active = False
        self.working = False
        self.idx = ''
        self.destination = ''
        self.current_hack = ''
        self.validation = bytearray()
        self.fixed_position = bytearray()

    def _execute_hack(self) -> None:
        """
        Take the first pending hack and execute it.

        :rtype: None
        """
        if not self.working:
            if len(self.pending) == 0:
                return

            self.current_hack = self.pending.pop(0)
            self.working = True

        if self.current_hack == Hack.fire_balls:
            self._hack_fire_balls()

    def _hack_fire_balls(self) -> None:
        """
        Inject data to get the fire balls.

        :rtype: None
        """
        data = bytearray.fromhex('656501000000')
        self.data = data + self.data
        message = f'*** Injection: Hacking {Hack.fire_balls}'
        print(message)
        debug(message)
