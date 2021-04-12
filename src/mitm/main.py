#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Entrypoint of the application. Main in the Middle Attack is basically a proxy which get and send the package between the
client and server but we have the opportunity to analyze or modify this information.
"""
from os import kill
from signal import SIGTERM
from threading import enumerate as threading_enumerate

from core.proxy import Proxy
from core.queue import Queue


def main() -> None:
    """
    Main function which start the 'man in the middle attack'.

    :rtype: None
    """
    from_host = '0.0.0.0'
    to_host = '192.168.100.230'
    port_server = 3333
    ports_client = range(3000, 3006)

    server = Proxy(from_host, to_host, port_server)
    server.start()

    clients = []
    for port in ports_client:
        client_server = Proxy(from_host, to_host, port)
        client_server.start()
        clients.append(client_server)

    while True:
        try:
            cmd = input('>>> ').lower()
            if cmd == 'hello':
                print('Hello World!')
            elif cmd in ('quit', 'q', 'exit'):
                for thread in threading_enumerate():
                    kill(thread.native_id, SIGTERM)
            elif cmd in ('t', 'thread', 'threads'):
                for thread in threading_enumerate():
                    message = f'| {thread.name:>25} | PID {thread.native_id} | ID {thread.ident} | ' \
                              f'Alive {thread.is_alive()} | Daemon {thread.daemon} |'
                    print(message)
            elif cmd[0:2] == 's ':
                for client_server in clients:
                    if client_server.running:
                        Queue.SERVER_QUEUE.append(bytearray.fromhex(cmd[2:]))
            elif cmd[0:2] == 'c ':
                for client_server in clients:
                    if client_server.running:
                        Queue.CLIENT_QUEUE.append(bytearray.fromhex(cmd[2:]))
        except Exception as e:
            print(f'ERROR: Input section ---> {e}')


if __name__ == "__main__":
    main()
