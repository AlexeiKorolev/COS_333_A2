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

# The regserver.py Program

First compose a preliminary server program named regserverprelim.py. Your regserverprelim.py program must have the same behavior as the ref_regserver.pyc program, except that it must not use multiple threads.

When executed with -h as a command-line argument, your regserverprelim.py must display a help message that describes the program's behavior:

$ python regserverprelim.py -h
usage: regserver.py [-h] port

Server for the registrar application

positional arguments:
port the port at which the server should listen

options:
-h, --help show this help message and exit

When executed without -h as a command-line argument, and as indicated by the usage message, your regserverprelim.py must listen for client requests on the given port. When it receives a request using the prescribed protocol, it must fetch data from the database, formulate a response using the prescribed protocol, and send the response to the client. Your regserverprelim.py must work with the given clients, and also with your clients.

Your regserverprelim.py must handle the SQLite database. Your client programs must not access the SQLite database. Assume that the client program is running on computer X, your reqserver.py is running on computer Y, and the SQLite database is located on computer Y where X may not be the same as Y.

Your regserverprelim.py must handle '%' and '\_' as ordinary characters, not wildcard characters, just as described in the Assignment 1 specification.

Your regserverprelim.py must protect itself from SQL injection attacks by using SQL prepared statements.

Note: Concerning killing the server:

Your regserverprelim.py must loop infinitely, as many servers do. The issue then becomes... How can you kill your server? That is, after creating a process by issuing a python regserverprelim.py someport command, how can you kill that process?

On any Mac or Linux computer the answer easy: type Ctrl-c. Doing that sends a SIGINT signal to the process, which (by default) kills it. Don't type Ctrl-z. Doing that sends a SIGTSTP signal to the process, which places it in the background. The process would continue to run and occupy the specified port. Subsequently issuing a fg command would bring the process back to the foreground.

On a Microsoft Windows computer the answer is harder. Ctrl-c does the job of killing any process, including one that is looping infinitely. However, your server will spend most of its time executing calls of server_sock.accept(), and while executing that function MS Windows blocks the effect of Ctrl-c.

So how can you kill the server on a MS Windows computer? Ctrl-Break might work. If your keyboard doesn't have a Break key, then consulting the Wikipedia Break key article might help. In the worst case you can kill the process via the Windows Task Manager; but that's an awkward last resort.

The ref_regserver.pyc program validates each "class overviews" request that it receives from a client, making sure that the request has the proper format. Thereby ref_regserver.pyc will inform you if the client sends a request that doesn't have the proper format. However, your regserverprelim.py may assume that each request that the client sends has the proper format.
After composing your regserverprelim.py program, compose program named regserver.py. Your regserver.py must have the same behavior as your regserverprelim.py program, except that it must use multiple threads. That is, each time it receives a client request, it must spawn a new thread to handle that request. Thus your regserver.py must have the same behavior as ref_regserver.pyc.

The connection between your regserver.py and the database must not be persistent. That is, it must not be the case that your regserver.py creates a database connection upon startup, and uses that database connection during the entire execution of your regserver.py.

Instead the database connection must be transient. Each time a client contacts your regserver.py, your regserver.py must create a database connection, fetch data from the database using that connection, and then close that connection.

The justification... Production-quality database management systems (such as PostgreSQL, Oracle, Microsoft SQLServer, and so forth) can handle requests concurrently. The "unit of concurrency" is the database connection. That is, production-quality database management systems can handle multiple database connections concurrently. To take advantage of that database management system concurrency, within your regserver.py each child thread must create a new database connection, fetch data from the database using that connection, and then close that connection. An upcoming lecture will elaborate under the heading database connection pooling.
