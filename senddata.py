#!/usr/bin/env python

#-----------------------------------------------------------------------
# daytimeclient.py
# Author: Bob Dondero
#-----------------------------------------------------------------------
# Try this:
# daytimeclient.py time-a.nist.gov 13
#-----------------------------------------------------------------------

import sys
import socket

#-----------------------------------------------------------------------

def main():
    if len(sys.argv) != 3:
        print('Usage: python %s host port' % sys.argv[0])
        sys.exit(1)

    try:
        host = sys.argv[1]
        port = int(sys.argv[2])

        with socket.socket() as sock:
            sock.connect((host, port))
            flo = sock.makefile(mode='r', encoding='ascii')
            for line in flo:
                print(line, end='')

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
