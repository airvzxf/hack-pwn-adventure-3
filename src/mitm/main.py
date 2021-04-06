#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Entrypoint of the application. Main in the Middle Attack is basically a proxy which get and send the package between the
client and server but we have the opportunity to analyze or modify this information.
"""
from core.proxy import Proxy


def main() -> None:
    """
    Main function which start the 'man in the middle attack'.

    :rtype: None
    """
    from_host = '0.0.0.0'
    to_host = '192.168.100.12'
    master_server = Proxy(from_host, to_host, 3333)
    master_server.start()

    game_servers = []
    for port in range(3000, 3006):
        _game_server = Proxy(from_host, to_host, port)
        _game_server.start()
        game_servers.append(_game_server)

    master_server.join()
    for game_server in game_servers:
        game_server.join()


if __name__ == "__main__":
    main()
