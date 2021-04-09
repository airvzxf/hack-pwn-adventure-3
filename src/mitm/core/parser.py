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

    def __init__(self, data: bytes) -> None:
        """
        Constructor which init the class.

        :type data: bytes
        :param data: Raw data.

        :rtype: Parse
        :return: The object instanced of this class.
        """
        logging.basicConfig(filename='./debug.log', filemode='a', level=logging.DEBUG, format='%(message)s')
        self.message = ''
        self.should_display_message = False
        self.data = data

    def _noop(self, data: bytes) -> bytes:
        """
        It does nothing with the data.

        :type data: bytes
        :param data: Raw data.

        :rtype: bytes
        :return: The bytes of data which is not able to process.
        """
        self.should_display_message = True
        self.message += f'  |-> Noop ---> Hex: {data.hex()} |\n'
        self.message += f'  |-> Noop ---> Raw: {data} |\n'
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
        position_padding = 20
        x, y, z = struct.unpack('<fff', data[:position_size])

        last_size = position_size
        view_size = 8
        view_padding = 20
        view, = struct.unpack('<Q', data[last_size:last_size + view_size])

        last_size += view_size
        self.message += f'  |-> Position --->' \
                        f' X: {x:<{position_padding}} | Y: {y:<{position_padding}} | Z: {z:<{position_padding}} |' \
                        f' View: {view:<{view_padding}} |\n'

        return data[last_size:]

    def _shoot(self, data: bytes) -> bytes:
        """
        Get the information when the character shoots.

        :type data: bytes
        :param data: Raw data.

        :rtype: bytes
        :return: The bytes of data which is not able to process.
        """
        length_size = 2
        length = int(struct.unpack('<h', data[:length_size])[0])

        name_padding = 20
        name_size = length
        name = str(data[length_size:length_size + name_size], 'UTF-8')
        self.message += f'  |-> Shoot ---> Name: {name:<{name_padding}} |\n'

        last_size = length_size + name_size
        target_size = 4 * 3
        target_padding = 18
        x, y, z = struct.unpack('<fff', data[last_size:last_size + target_size])
        self.message += f'  |-> Shoot ---> Target --->' \
                        f' X: {x:<{target_padding}} | Y: {y:<{target_padding}} | Z: {z:<{target_padding}} |\n'

        last_size += target_size

        return data[last_size:]

    def _shooting(self, data: bytes) -> bytes:
        """
        Get the information when the character is shooting.

        :type data: bytes
        :param data: Raw data.

        :rtype: bytes
        :return: The bytes of data which is not able to process.
        """
        value_size = 1
        value_padding = 2
        value = str(struct.unpack('<b', data[:value_size])[0])
        self.message += f'  |-> Shooting ---> Is not started?: {value:<{value_padding}} |\n'

        last_size = value_size
        return data[last_size:]

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
        is_on_floor = str(struct.unpack('<?', data[:is_on_floor_size])[0])

        last_size = is_on_floor_size
        self.message += f'  |-> Jump ---> Is on the floor?: {is_on_floor:<{is_on_floor_padding}} |\n'

        return data[last_size:]

    def _item(self, data: bytes) -> bytes:
        """
        Get the information when the items.

        :type data: bytes
        :param data: Raw data.

        :rtype: bytes
        :return: The bytes of data which is not able to process.
        """
        self.should_display_message = True
        item_size = 4
        item_padding = 5
        item = str(struct.unpack('<i', data[:item_size])[0])

        last_size = item_size
        self.message += f'  |-> Item ---> {item:<{item_padding}} |\n'

        return data[last_size:]

    def _weapon_slot(self, data: bytes) -> bytes:
        """
        Get the information when the weapon is changed.

        :type data: bytes
        :param data: Raw data.

        :rtype: bytes
        :return: The bytes of data which is not able to process.
        """
        weapon_size = 1
        weapon_padding = 2
        weapon_slot = str(struct.unpack('<B', data[:weapon_size])[0])

        last_size = weapon_size
        self.message += f'  |-> Weapon slot ---> {weapon_slot:<{weapon_padding}} |\n'

        return data[last_size:]

    def _weapon_reload(self, data: bytes) -> bytes:
        """
        Get the information when the weapon is reloaded.

        :type data: bytes
        :param data: Raw data.

        :rtype: bytes
        :return: The bytes of data which is not able to process.
        """
        self.message += f'  |-> Weapon reloaded ---> Yes |\n'

        return data

    def _quest_change(self, data: bytes) -> bytes:
        """
        Get the information when the quest is changed.

        :type data: bytes
        :param data: Raw data.

        :rtype: bytes
        :return: The bytes of data which is not able to process.
        """
        length_size = 2
        length = int(struct.unpack('<h', data[:length_size])[0])

        last_size = length_size
        name_size = length
        name_padding = 20
        name = str(data[last_size:last_size + name_size], 'UTF-8')
        self.message += f'  |-> Available Quest ---> Change to: {name:<{name_padding}} |\n'

        last_size += name_size

        return data[last_size:]

    def _monster_position(self, data: bytes) -> bytes:
        """
        Get the position of the monster.

        :type data: bytes
        :param data: Raw data.

        :rtype: bytes
        :return: The bytes of data which is not able to process.
        """
        self.message += f'  |-> Monster Position |\n'

        idx_size = 4
        idx_padding = 50
        idx = struct.unpack('<i', data[:idx_size])[0]
        last_size = idx_size
        self.message += f'    |-> ID: {idx:<{idx_padding}} |\n'

        position_size = 4 * 3
        position_padding = 50
        x, y, z = struct.unpack('<fff', data[last_size:last_size + position_size])
        last_size += position_size
        self.message += f'    |-> Position -> X:{x:<{position_padding}} | Y:{y:<{position_padding}} |' \
                        f' Z:{z:<{position_padding}} |\n'

        unknown1_size = 2
        unknown1_padding = 50
        unknown1 = struct.unpack('<h', data[last_size:last_size + unknown1_size])[0]
        last_size += unknown1_size
        self.message += f'    |-> Unknown #1: {unknown1:<{unknown1_padding}} |\n'

        unknown2_size = 8
        unknown2_padding = 50
        unknown2, unknown3 = struct.unpack('<ii', data[last_size:last_size + unknown2_size])
        last_size += unknown2_size
        self.message += f'    |-> Unknown #2: {unknown2:<{unknown2_padding}} |\n'
        self.message += f'    |-> Unknown #3: {unknown3:<{unknown2_padding}} |\n'

        unknown4_size = 2
        unknown4_padding = 50
        unknown4 = struct.unpack('<h', data[last_size:last_size + unknown4_size])[0]
        last_size += unknown4_size
        self.message += f'    |-> Unknown #4: {unknown4:<{unknown4_padding}} |\n'

        return data[last_size:]

    def parse(self, port: int, origin: str) -> bytes:
        """
        Start to parse the data.

        :type port: int
        :param port: The number of the port of the communication.

        :type origin: str
        :param origin: If the data comes from client or server.

        :rtype: bytes
        :return: Return the data with or without modifications.
        """
        if len(self.data) == 2 and self.data.hex() == '0000':
            return self.data

        if origin == 'client':
            return self.data

        if port == 3333:
            return self.data

        if origin == 'server':
            return self.data

        ids = {
            15729: self._quest_change,
            15731: self._weapon_slot,
            25957: self._item,
            26922: self._shoot,
            27762: self._weapon_reload,
            28778: self._jump,
            29286: self._shooting,
            29552: self._monster_position,
            30317: self._position,
        }

        self.message += f'[{origin}({port})]\n'
        self.message += f'|-> Hex: {self.data.hex()} |\n'
        self.message += f'|-> Raw: {self.data} |\n'
        is_unknown = False
        unknown_data = bytearray()

        data = self.data
        if origin == 'server':
            packet_id = struct.unpack('<H', data[:2])[0]
            if packet_id == 29552:
                data = data[:-2]

        while len(data) > 1:
            packet_id = struct.unpack('<H', data[:2])[0]

            if packet_id not in ids:
                is_unknown = True
                self.should_display_message = True
                unknown_data += data[:1]
                if len(data) == 2:
                    unknown_data += data[1:]
                data = data[1:]
                continue

            if is_unknown:
                self.message += f'  |-> Unknown ---> Hex: {unknown_data.hex()} |\n'
                self.message += f'  |-> Unknown ---> Raw: {unknown_data} |\n'
                is_unknown = False
                unknown_data = bytearray()

            data = ids.get(packet_id, self._noop)(data[2:])

        if is_unknown:
            self.message += f'  |-> Unknown ---> Hex: {unknown_data.hex()} |\n'
            self.message += f'  |-> Unknown ---> Raw: {unknown_data} |\n'

        if self.should_display_message:
            print(self.message)
            logging.debug(self.message)

        return self.data
