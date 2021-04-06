#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Parse the raw data. It is an intent of analyze the patterns for print useful information.
The patterns which are not discovered yet, will show the raw data in hexadecimal.

This code is partially taken bye LiveOverflow/PwnAdventure3 (https://github.com/LiveOverflow/PwnAdventure3) under the
GPL-3.0 License
"""
import logging
import struct


class Parse:
    """
    Parse the data and find patterns to display a useful information.
    """

    def __init__(self, data: bytes, port: int, origin: str) -> None:
        """
        Constructor which init the class.

        :type data: bytes
        :param data: Raw data.

        :type port: int
        :param port: The number of the port of the communication.

        :type origin: str
        :param origin: If the data comes from client or server.

        :rtype: Parse
        :return: The object instanced of this class.
        """
        logging.basicConfig(filename='./debug.log', filemode='a', level=logging.DEBUG, format='%(message)s')
        self.message = ''
        self._parse(data, port, origin)

    def _noop(self, data: bytes) -> bytes:
        """
        It does nothing with the data.

        :type data: bytes
        :param data: Raw data.

        :rtype: bytes
        :return: The bytes of data which is not able to process.
        """
        self.message += f'noop ---> data: {data.hex()} ---> '
        return data

    def _position(self, data: bytes) -> bytes:
        """
        Get the position with AXIS (x,y,z) and the camera view.
        x: float
        y: float
        z: float
        view: long long

        :type data: bytes
        :param data: Raw data.

        :rtype: bytes
        :return: The bytes of data which is not able to process.
        """
        position_size = 4 * 3
        position_padding = 18
        x, y, z = struct.unpack('<fff', data[0:position_size])

        last_size = position_size
        view_size = 8
        view_padding = 15
        view, = struct.unpack('<Q', data[last_size:last_size + view_size])

        last_size += view_size
        self.message += f'position ---> x: {x:<{position_padding}} | y: {y:<{position_padding}} | z: {z:<{position_padding}} | view: {view:<{view_padding}} ---> '

        return data[last_size:]

    def _shoot(self, data: bytes) -> bytes:
        """
        Get the information when the character shoots.

        :type data: bytes
        :param data: Raw data.

        :rtype: bytes
        :return: The bytes of data which is not able to process.
        """
        # position_size = 4 * 3
        # position_padding = 18
        # x, y, z = struct.unpack('fff', data[last_size:last_size + position_size])
        #
        # last_size = position_size
        # view_size = 8
        # view_padding = 30
        # view = str(struct.unpack('d', data[last_size:last_size + view_size]))
        #
        # last_size += view_size
        # self.message += f'shoot ---> x: {x:<{position_padding}} | y: {y:<{position_padding}} | z: {z:<{position_padding}} | view: {view:<{view_padding}} ---> '
        #
        # return data[last_size:]
        return data

    def _jump(self, data: bytes) -> bytes:
        """
        Get the information when the character jumps.

        :type data: bytes
        :param data: Raw data.

        :rtype: bytes
        :return: The bytes of data which is not able to process.
        """
        is_on_floor_size = 1
        is_on_floor_padding = 5
        is_on_floor = str(struct.unpack('?', data[0:is_on_floor_size])[0])

        last_size = is_on_floor_size
        self.message += f'jump ---> is_on_floor: {is_on_floor:<{is_on_floor_padding}} ---> '

        return data[last_size:]

    def _parse(self, data: bytes, port: int, origin: str) -> None:
        """
        Start to parse the data.

        :type data: bytes
        :param data: Raw data.

        :type port: int
        :param port: The number of the port of the communication.

        :type origin: str
        :param origin: If the data comes from client or server.

        :rtype: None
        :return: Nothing.
        """
        if port == 3333:
            return

        if origin == 'server':
            return

        ids = {
            0x6d76: self._position,
            0x6a70: self._jump,
            # 0x2a69: self._shoot
        }

        if len(data) == 2 and data.hex() == '0000':
            return

        original_data = data
        self.message += f'[{origin}({port})] '
        is_unknown = False
        unknown_data = bytearray()

        while len(data) > 1:
            packet_id = struct.unpack('>H', data[0:2])[0]

            if packet_id not in ids:
                is_unknown = True
                unknown_data += data[0:1]
                if len(data) == 2:
                    unknown_data += data[1:]
                data = data[1:]
                continue

            if is_unknown:
                self.message += f'unknown ---> data: {unknown_data.hex()} ---> '
                is_unknown = False
                unknown_data = bytearray()

            data = ids.get(packet_id, self._noop)(data[2:])

        if is_unknown:
            self.message += f'unknown ---> data: {unknown_data.hex()} ---> '

        self.message += f'original ---> {original_data.hex()} |'
        print(self.message)
        logging.debug(self.message)
