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

from core.queue import Queue


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
        self.should_display_message = False
        self.show_data = False
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
        x, y, z, = struct.unpack('<fff', self._get_data(4 * 3))
        view = self.data[:4]
        self._get_data(4)
        view_limit, dy, dx = struct.unpack('<hbb', self._get_data(4))
        message = f'{x:10.2f} X | {y:10.2f} Y | {z:10.2f} Z | Direction X: {dx:4} | Y: {dy:4} | ' \
                  f'View: {view.hex()} | View limit: {view_limit}'

        self.message += f'    |-> {message}\n'

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

    def _server_my_position(self) -> None:
        """
        Get the positions of my character.

        :rtype: None
        """
        self.message += f'  |-> My Character\n'
        self._server_character_position()

    def _server_character_position(self) -> None:
        """
        Get the positions of the character.

        :rtype: None
        """
        idx, = struct.unpack('<I', self._get_data(4))

        self.message += f'  |-> Character Position\n'
        self.message += f'    |-> ID: {idx}\n'
        self._general_position()
        unknown_1 = self.data[:4]
        self._get_data(4)
        self.message += f'    |-> Unknown #1: {unknown_1.hex()}\n'

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
        counter, = struct.unpack('<i', self._get_data(4))

        self.message += f'  |-> Magic Shoot\n'
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

    def _server_init(self) -> None:
        """
        Server send initial information in some specific events during the game.

        :rtype: None
        """
        idx, = struct.unpack('<I', self._get_data(4))
        unknown_1 = self.data[:4]
        self._get_data(4)
        boolean, = struct.unpack('<b', self._get_data(1))
        length, = struct.unpack('<h', self._get_data(2))
        name = str(self.data[:length], 'UTF-8')
        self._get_data(length)
        x, y, z, = struct.unpack('<fff', self._get_data(12))
        d1 = self.data[:1]
        d2 = self.data[1:2]
        d3 = self.data[2:3]
        d4 = self.data[3:4]
        self._get_data(4)
        unknown_2 = self.data[:2]
        self._get_data(2)
        type_object, = struct.unpack('<i', self._get_data(4))

        # Auto loot
        # TODO: Fix the bug when the bear is running and die or use the Fire Ball looks like it is broken. 0x7073
        print(f'name: {name}')
        if "Drop" in name:
            pickup = struct.pack("=HI", 0x6565, idx)
            Queue.SERVER_QUEUE.append(pickup)
            print(f'--*-- Pickup the {name} -> ID: {idx} | Hex: {pickup.hex()}')

        message = f'-> ID: {idx:<{5}} | True: {boolean} | Type: {type_object:<{5}} | ' \
                  f'{unknown_1.hex()} {unknown_2.hex()} | ' \
                  f'{x:10.2f} X | {y:10.2f} Y | {z:10.2f} Z | D: {d1.hex()} {d2.hex()} {d3.hex()} {d4.hex()} | ' \
                  f'{name}'
        self.message += f'  |-> Init Information\n'
        self.message += f'    |-> {message}\n'

    def client(self, port: int) -> bytes:
        """
        Start to parse the data of the client.

        :type port: int
        :param port: The number of the port of the communication.

        :rtype: bytes
        :return: Return the data with or without modifications.
        """

        ids = {
            00000: self._noop,  # 0x0000
            15729: self._client_quest_selected,  # 0x713D
            15731: self._client_weapon_slot,  # 0x733D
            25957: self._client_item,  # 0x6565
            26922: self._client_shoot,  # 0x2A69
            27762: self._client_weapon_reload,  # 0x726C
            28778: self._client_jump,  # 0x6A70
            29286: self._client_shooting,  # 0x6672
            30317: self._client_position,  # 0x6D76
        }

        self.message += f'[client({port})]\n'
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
                self.message += f'  |-> Unknown #1.1 ---> Hex: {unknown_data.hex()}\n'
                self.message += f'  |-> Unknown #1.2 ---> Raw: {unknown_data}\n'
                is_unknown = False
                self.show_data = True
                unknown_data = bytearray()

            ids.get(packet_id)()

        if is_unknown:
            self.show_data = True
            self.message += f'  |-> Unknown #1.3 ---> Hex: {unknown_data.hex()}\n'
            self.message += f'  |-> Unknown #1.4 ---> Raw: {unknown_data}\n'

        if self.should_display_message and len(self.message) > 20:
            if self.show_data:
                self.message += f'|-> Hex: {self.data_original.hex()}\n'
                self.message += f'|-> Raw: {self.data_original}\n'
            self.show_data = False
            print(self.message)
            logging.debug(self.message)

        return self.data_original

    def server(self, port: int) -> bytes:
        """
        Start to parse the data of the server.

        :type port: int
        :param port: The number of the port of the communication.

        :rtype: bytes
        :return: Return the data with or without modifications.
        """
        self.data = self.data[:-2]
        if len(self.data) == 0:
            return self.data_original

        ids = {
            00000: self._noop,  # 0x0000
            24940: self._server_gun_shoot,  # 0x6c61
            24941: self._server_magic_shoot,  # 0x6d61
            27501: self._server_init,  # 0x6d6b
            28784: self._server_constant_information,  # 0x7070
            29552: self._server_character_position,  # 0x7073
            30840: self._server_monsters_list,  # 0x7878
            30317: self._server_my_position,  # 0x6d76
        }

        self.message += f'[server({port})]\n'
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
                self.message += f'  |-> Data         ---> Hex: {self.data_original.hex()}\n'
                self.message += f'  |-> Unknown #2.1 ---> Hex: {unknown_data.hex()}\n'
                self.message += f'  |-> Unknown #2.2 ---> Raw: {unknown_data}\n'
                is_unknown = False
                self.show_data = True
                unknown_data = bytearray()

            ids.get(packet_id)()

        if is_unknown:
            self.show_data = True
            self.message += f'  |-> Data         ---> Hex: {self.data_original.hex()}\n'
            self.message += f'  |-> Unknown #2.3 ---> Hex: {unknown_data.hex()}\n'
            self.message += f'  |-> Unknown #2.4 ---> Raw: {unknown_data}\n'

        if self.should_display_message and len(self.message) > 20:
            if self.show_data:
                self.message += f'|-> Hex: {self.data_original.hex()}\n'
                self.message += f'|-> Raw: {self.data_original}\n'
            self.show_data = False
            print(self.message)
            logging.debug(self.message)

        return self.data_original
