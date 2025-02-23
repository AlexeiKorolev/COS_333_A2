import argparse
import socket
import sys
import json
import textwrap

parser = argparse.ArgumentParser()

# Not formatting responses correctly
def format_reg_response(resp: list):
    print("ClsId Dept CrsNum Area Title")
    print("----- ---- ------ ---- -----")
    for row in resp:
        row = tuple(row) # Make sure the row is a tuple for formatting
        row = '%5s %4s %6s %4s %s' % row

        wrapped_text = textwrap.fill(row, width=72,
                                     subsequent_indent=' '*23)
        # Formatting based on requirements
        print(wrapped_text)


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
                        type=str)
    parser.add_argument(dest="port", metavar="port",help="",
                        type=int)
    args = parser.parse_args()

    payload = ['get_overviews', {
        "dept": args.dept,
        "coursenum": args.num,
        "area": args.area,
        'title': args.title
    }]

    # if payload[1]["dept"] is None:
    #     pass
    # else:
    #     payload[1]["dept"] = payload[1]["dept"].replace('_', r'\_') #Replace underscores
    #     payload[1]["dept"] = payload[1]["dept"].replace('%', r'\%') #Replace %'s
    
    # if payload[1]["coursenum"] is None:
    #     payload[1]["coursenum"] = '' # Handle ignore on server side
    # else:
    #     payload[1]["coursenum"] = payload[1]["coursenum"].replace('_', r'\_')
    #     # Replace underscores
    #     payload[1]["coursenum"] = payload[1]["coursenum"].replace('%', r'\%')
    #     # Replace %'s
    
    # if payload[1]["area"] is None:
    #     payload[1]["area"] = '' #To allow SQL to ignore
    # else:
    #     payload[1]["area"] = payload[1]["area"].replace('_', r'\_')
    #     payload[1]["area"] = payload[1]["area"].replace('%', r'\%')
    # if payload[1]["title"] is None:
    #     payload[1]["title"] = '' #To allow SQL to ignore
    # else:
    #     payload[1]["title"] = payload[1]["title"].replace('_', r'\_')
    #     payload[1]["title"] = payload[1]["title"].replace('%', r'\%')

    try:
        host = sys.argv[1]
        port = int(sys.argv[2])

        with socket.socket() as sock:
            sock.connect((host, port))
            
            flo = sock.makefile(mode='w', encoding='utf-8')
            flo.write(json.dumps(payload) + '\n') # This needs to have \n for write to work correctly
            print(f"wrote {payload} \n")
            flo.flush()

            flo.close()

            result = sock.makefile('r', encoding='utf-8')
            result_text = json.loads(result.read())
            print(f"result_text: {result_text}")
            print(f"result_text[1]: {result_text[1]}")
            if result_text[0]:
                format_reg_response(result_text[1])
                pass # need to format responses

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)
    finally:
        sock.close()


if __name__ == "__main__":
    main()


