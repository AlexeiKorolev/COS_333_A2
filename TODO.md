The regoverviews.py Client Program
Compose your regoverviews.py program. Your regoverviews.py program must have the same behavior as the ref_regoverviews.pyc program.

When executed with -h as a command-line argument, your regoverviews.py must display a help message that describes the program's behavior:

$ python regoverviews.py -h
usage: regoverviews.py [-h] [-d dept] [-n num] [-a area] [-t title] host port

Registrar application: show overviews of classes

positional arguments:
host the computer on which the server is running
port the port at which the server is listening

options:
-h, --help show this help message and exit
-d dept show only those classes whose department contains dept
-n num show only those classes whose course number contains num
-a area show only those classes whose distrib area contains area
-t title show only those classes whose course title contains title

Your regoverviews.py must accept two required command-line arguments. The first must be the host, that is, the IP address or domain name of the computer on which the server is running. The second must be the number of the port at which the server is listening. Your regoverviews.py also must must accept optional arguments, as does the Assignment 1 regoverviews.py program.

When executed without -h as a command-line argument, and as indicated by the usage message, your regoverviews.py must send a request to its server using the prescribed protocol, receive a response from its server using the prescribed protocol, and write the response to its stdout in the proper format (as defined in Assignment 1). At this point the server must be the given one. Later you'll also be able to use your server.

The ref_regoverviews.pyc program validates each response that it receives from a server, making sure that the the request has the proper format. Thereby ref_regoverviews.pyc will inform you if your server sends it a response that does not have the proper format. However, your regoverviews.py may assume that each response that the server sends has the proper format.
