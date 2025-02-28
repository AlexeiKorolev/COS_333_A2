#!/usr/bin/env python

#-----------------------------------------------------------------------
# testregdetails.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import os
import sys
import argparse
import shutil

#-----------------------------------------------------------------------

MAX_LINE_LENGTH = 72
UNDERLINE = '-' * MAX_LINE_LENGTH

#-----------------------------------------------------------------------

def parse_args():

    parser = argparse.ArgumentParser(
        description=
        "Test the Registrar's application's handling of " +
        "class details requests")
    parser.add_argument('program', metavar='program', type=str,
        help='the client program to run')
    parser.add_argument('host', metavar='host', type=str,
        help='the host on which the server is running')
    parser.add_argument('port', metavar='port', type=int,
        help='the port at which the server is listening')
    args = parser.parse_args()

    return (args.program, args.host, args.port)

#-----------------------------------------------------------------------

def print_flush(message):
    print(message)
    sys.stdout.flush()

#-----------------------------------------------------------------------

def exec_command(program, args):

    print_flush(UNDERLINE)
    command = 'python ' + program + ' ' + args
    print_flush(command)
    exit_status = os.system(command)
    if os.name == 'nt':  # Running on MS Windows?
        print_flush('Exit status = ' + str(exit_status))
    else:
        print_flush('Exit status = ' + str(os.WEXITSTATUS(exit_status)))

#-----------------------------------------------------------------------

def main():

    program, host, port = parse_args()

    prefix = host + ' ' + str(port) + ' '

    # Add more tests here.

    def test_commands():
        exec_command(program, prefix + '8321')
        exec_command(program, prefix + '9032')
        exec_command(program, prefix + '7842')
        exec_command(program, prefix + '8094')
        exec_command(program, prefix + '8285')
        exec_command(program, prefix + '8508')
        exec_command(program, prefix + '7838')
        # should be error in row_missing.sqlite

        #Testing erroneous command line arguments
        exec_command(program, prefix + '')
        exec_command(program, prefix + '8321 9032')
        exec_command(program, prefix + 'abc123')
        exec_command(program, prefix + '9034')

        exec_command(program, prefix + '7838')
        exec_command(program, prefix + '7839')
        exec_command(program, prefix + '7840')
        exec_command(program, prefix + '7841')

    test_commands()

    shutil.copy('reg.sqlite', 'reg_copy.sqlite')
    os.remove('reg.sqlite')
    shutil.copy('blank.sqlite', 'reg.sqlite')

    test_commands()

    os.remove('reg.sqlite')
    shutil.copy('row_missing.sqlite', 'reg.sqlite')

    test_commands()

    os.remove('reg.sqlite')
    shutil.copy('table_missing.sqlite', 'reg.sqlite')

    test_commands()

    os.remove('reg.sqlite')
    shutil.copy('reg_copy.sqlite', 'reg.sqlite')



    # Add more tests here.

if __name__ == '__main__':
    main()
