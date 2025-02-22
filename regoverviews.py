import argparse
import socket


parser = argparse.ArgumentParser()





def main():
     # Set up help options
    parser.add_argument("-d", dest="dept", metavar="dept",
        help="show only those classes whose department contains dept")
    parser.add_argument("-n",dest="num", metavar="num",
        help="show only those classes whose course number contains num")
    parser.add_argument("-a", dest="area", metavar="area",
        help="show only those classes whose distrib area contains area")
    parser.add_argument("-t", dest="title", metavar="title",
        help="show only those classes whose course " +
            "title contains title") 
    parser.add_argument(dest="host", metavar="host",help="",
                        type=int)
    parser.add_argument(dest="port", metavar="port",help="",
                        type=int)
    args = parser.parse_args()



    # big cigarette lol


