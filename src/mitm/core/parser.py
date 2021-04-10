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

        :rtype: None
        """
        logging.basicConfig(filename='./debug.log', filemode='a', level=logging.DEBUG, format='%(message)s')
        self.message = ''
        self.should_display_message = True
        self.show_data = True
        self.data_original: bytes = data
        self.data: bytes = data

    def _noop(self) -> None:
        """
        It does nothing with the data.

        :rtype: None
        """
        return

    def _get_data(self, size: int) -> bytes:
        """
        Split the data in two parts.
        The first one is returned the second is updated in the global data.

        :type size: int
        :param size: Size of data which will split.

        :rtype: bytes
        :return: The split data.
        """
        data = self.data[:size]
        self.data = self.data[size:]
        return data

    def _general_position(self) -> None:
        """
        Get the position with AXIS (x,y,z) and the camera view.

        :rtype: None
        """
        x, y, z, view, view_limit, dy, dx = struct.unpack('<ffffhbb', self._get_data(4 * 5))

        self.message += f'    |-> X: {x:.{2}f} | Y: {y:.{2}f} | Z: {z:.{2}f}\n'
        self.message += f'    |-> Direction X: {dx} | Y: {dy}\n'
        self.message += f'    |-> View: {view:.{2}f}\n'
        self.message += f'    |-> View limit: {view_limit}\n'

    def _client_position(self) -> None:
        """
        Get the position of your player.

        :rtype: None
        """
        self.message += f'  |-> My Position\n'
        self._general_position()

    def _client_shoot(self) -> None:
        """
        Get the information when the your character shoots.

        :rtype: None
        """
        length, = struct.unpack('<h', self._get_data(2))
        name, = struct.unpack('%ds' % length, self._get_data(length))
        name = str(name, 'UTF-8')
        x, y, z = struct.unpack('<fff', self._get_data(4 * 3))

        self.message += f'  |-> Shoot\n'
        self.message += f'    |-> Name: {name}\n'
        self.message += f'    |-> Position: X: {x:{2}f} | Y: {y:{2}f} | Z: {z:{2}f}\n'

    def _client_shooting(self) -> None:
        """
        Get the information when the your character is shooting.

        :rtype: None
        """
        value, = struct.unpack('<?', self._get_data(1))

        self.message += f'  |-> Shooting\n'
        self.message += f'    |-> Automatic: {value}\n'

    def _client_jump(self) -> None:
        """
        Get the information when the your character jumps.

        :rtype: None
        """
        ready, = struct.unpack('<?', self._get_data(1))

        self.message += f'  |-> Jump\n'
        self.message += f'    |-> Ready: {ready}\n'

    def _client_item(self) -> None:
        """
        Get the information when your character pick up the items.

        :rtype: None
        """
        self.should_display_message = True
        print(f'item: {self.data[:4].hex()}')
        idx, = struct.unpack('<i', self._get_data(4))

        self.message += f'  |-> Item\n'
        self.message += f'    |-> ID: {idx}\n'

    def _client_weapon_slot(self) -> None:
        """
        Get the information when the weapon of your character is changed.

        :rtype: None
        """
        weapon_slot, = struct.unpack('<b', self._get_data(1))

        self.message += f'  |-> Weapon\n'
        self.message += f'    |-> Slot: {weapon_slot + 1}\n'

    def _client_weapon_reload(self) -> None:
        """
        Get the information when the weapon of your character is reloaded.

        :rtype: None
        """
        self.message += f'  |-> Weapon Reload\n'

        if self.data[:2].hex() == '6d76':
            return

        weapon_length, = struct.unpack('<h', self._get_data(2))
        weapon = self.data[:weapon_length]
        weapon = str(weapon, 'UTF-8')
        self._get_data(weapon_length)
        ammo_length, = struct.unpack('<h', self._get_data(2))
        ammo = self.data[:ammo_length]
        ammo = str(ammo, 'UTF-8')
        self._get_data(ammo_length)
        bullets, = struct.unpack('<i', self._get_data(4))

        self.message += f'    |-> Name: {weapon}\n'
        self.message += f'    |-> Ammo: {ammo}\n'
        self.message += f'    |-> Bullets: {bullets}\n'

    def _client_quest_selected(self) -> None:
        """
        Get the information when you change the quest.

        :rtype: None
        """
        length, = struct.unpack('<h', self._get_data(2))
        name = self.data[:length]
        name = str(name, 'UTF-8')
        self._get_data(length)

        self.message += f'  |-> Quest Selected\n'
        self.message += f'    |-> Name: {name}\n'

    def _server_monsters_position(self) -> None:
        """
        Get the positions of the monsters.

        :rtype: None
        """
        idx, = struct.unpack('<h', self._get_data(2))

        self.message += f'  |-> Monster Position\n'
        self.message += f'    |-> ID: {idx}\n'
        self._general_position()

    def _server_monsters_list(self) -> None:
        """
        Server send the list of monsters.

        :rtype: None
        """
        idx, = struct.unpack('<i', self._get_data(4))

        self.message += f'  |-> Monster List\n'
        self.message += f'    |-> ID: {idx}\n'

    def _server_gun_shoot(self) -> None:
        """
        Server send the information of the gun shoot.

        :rtype: None
        """
        length, = struct.unpack('<h', self._get_data(2))
        weapon = self.data[:length]
        weapon = str(weapon, 'UTF-8')
        self._get_data(length)
        bullets, = struct.unpack('<i', self._get_data(4))

        self.message += f'  |-> Gun Shoot\n'
        self.message += f'    |-> Name: {weapon}\n'
        self.message += f'    |-> Bullets: {bullets}\n'

    def _server_magic_shoot(self) -> None:
        """
        Server send the information of the magic shoot.

        :rtype: None
        """
        # TODO: WIP - This method is in progress.
        self.message += f'  |-> Magic Shoot\n'
        counter, idx, = struct.unpack('<ih', self._get_data(6))

        # if counter == 96:
        #     self.message += f'    |-> {self.data[:41].hex()}'
        #     self._get_data(41)
        #
        # idx2, = struct.unpack('<h', self._get_data(2))
        # data2 = self.data[:22].hex()
        # self._get_data(22)
        #
        # idx3, = struct.unpack('<h', self._get_data(2))
        # data3 = self.data[:22].hex()
        # self._get_data(22)

        self.message += f'    |-> ID: {idx}\n'
        self.message += f'    |-> Counter: {counter}\n'

    def _server_constant_information(self) -> None:
        """
        Server send constant information.

        :rtype: None
        """
        data = self.data[:32]
        print(f'_server_constant_information: {data.hex()}')
        self._get_data(32)

        self.message += f'  |-> Constant Information\n'
        self.message += f'    |-> Counter: {data.hex()}\n'

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
        if origin == 'server':
            self.data = self.data[:-2]
            if len(self.data) == 0:
                return self.data_original

        # if origin == 'client':
        #     return self.data
        #
        # if origin == 'server':
        #     return self.data

        ids = {
            00000: self._noop,  # 0x0000
            15729: self._client_quest_selected,  # 0x713D
            15731: self._client_weapon_slot,  # 0x733D
            24940: self._server_gun_shoot,  # 0x6c61
            24941: self._server_magic_shoot,  # 0x6d61
            25957: self._client_item,  # 0x6565
            26922: self._client_shoot,  # 0x2A69
            27762: self._client_weapon_reload,  # 0x726C
            28778: self._client_jump,  # 0x6A70
            29286: self._client_shooting,  # 0x6672
            29552: self._server_monsters_position,  # 0x7073
            30317: self._client_position,  # 0x6D76
            30840: self._server_monsters_list,  # 0x7878
            28784: self._server_constant_information,  # 0x7070
        }

        self.message += f'[{origin}({port})]\n'
        is_unknown = False
        unknown_data = bytearray()

        while len(self.data) > 1:
            packet_id, = struct.unpack('<H', self._get_data(2))

            if packet_id not in ids:
                is_unknown = True
                self.should_display_message = True
                unknown_data += self.data[:1]
                if len(self.data) == 2:
                    unknown_data += self.data[1:]
                self.data: bytes = self.data[1:]
                continue

            if is_unknown:
                self.message += f'  |-> Unknown ---> Hex: {unknown_data.hex()}\n'
                self.message += f'  |-> Unknown ---> Raw: {unknown_data}\n'
                is_unknown = False
                self.show_data = True
                unknown_data = bytearray()

            ids.get(packet_id)()

        if is_unknown:
            self.show_data = True
            self.message += f'  |-> Unknown ---> Hex: {unknown_data.hex()}\n'
            self.message += f'  |-> Unknown ---> Raw: {unknown_data}\n'

        if self.should_display_message and len(self.message) > 20:
            if self.show_data:
                self.message += f'|-> Hex: {self.data_original.hex()}\n'
                self.message += f'|-> Raw: {self.data_original}\n'
            self.show_data = False
            print(self.message)
            logging.debug(self.message)

        return self.data_original
