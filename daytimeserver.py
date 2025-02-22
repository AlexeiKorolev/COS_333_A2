#!/usr/bin/env python

#-----------------------------------------------------------------------
# daytimeserver.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import os
import sys
import socket
import time

#-----------------------------------------------------------------------

def handle_client(sock):

    datetime = time.asctime(time.localtime())
    flo = sock.makefile(mode='w', encoding='ascii')
    flo.write(datetime + '\n')
    flo.flush()

#-----------------------------------------------------------------------

def main():

    if len(sys.argv) != 2:
        print('Usage: python %s port' % sys.argv[0])
        sys.exit(1)

    try:
        port = int(sys.argv[1])

        server_sock = socket.socket()
        print('Opened server socket')
        if os.name != 'nt':
            server_sock.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(('', port))
        print('Bound server socket to port')
        server_sock.listen()
        print('Listening')

        while True:
            try:
                sock, client_addr = server_sock.accept()
                with sock:
                    print('Accepted connection')
                    print('Opened socket')
                    print('Server IP addr and port:',
                        sock.getsockname())
                    print('Client IP addr and port:', client_addr)
                    handle_client(sock)
            except Exception as ex:
                print(ex, file=sys.stderr)

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
