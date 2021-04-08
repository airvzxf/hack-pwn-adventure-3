#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Entrypoint of the application. Main in the Middle Attack is basically a proxy which get and send the package between the
client and server but we have the opportunity to analyze or modify this information.
"""
import os

from core.proxy import Proxy


def main() -> None:
    """
    Main function which start the 'man in the middle attack'.

    :rtype: None
    """
    from_host = '0.0.0.0'
    to_host = '192.168.100.230'
    port_server = 3333
    ports_client = range(3000, 3006)

    master_server = Proxy(from_host, to_host, port_server)
    master_server.start()

    game_servers = []
    for port in ports_client:
        _game_server = Proxy(from_host, to_host, port)
        _game_server.start()
        game_servers.append(_game_server)

    while True:
        try:
            cmd = input('>>> ')
            if cmd in ('quit', 'q', 'exit'):
                os._exit(0)
            if cmd == 'hello':
                print('Hello World!')
        except Exception as e:
            print(f'ERROR: Input section ---> {e}')


if __name__ == "__main__":
    main()
