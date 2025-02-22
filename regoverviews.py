import argparse
import socket
import sys
import json

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

    payload = ['get_overviews', {
        "dept": args.dept,
        "coursenum": args.num,
        "area": args.area,
        'title': args.title
    }]

    try:
        host = sys.argv[1]
        port = int(sys.argv[2])

        with socket.socket() as sock:
            sock.connect((host, port))
            flo = sock.makefile(mode='w', encoding='utf-8')
            flo.write(json.dumps(payload))
            flo.flush()

            result = sock.makefile(mode='r', encoding='utf-8')
            result_data = result.read()

            print(result_data)

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)
    finally:
        sock.close()



    # big cigarette lol


