import argparse
import socket
import sys
import json
import textwrap

parser = argparse.ArgumentParser(description = "Registrar application: show overviews of classes")

# Not formatting responses correctly
def format_reg_response(dict_results):
    print("ClsId Dept CrsNum Area Title")
    print("----- ---- ------ ---- -----")
    for row in dict_results:
        classid = row['classid']
        dept = row['dept']
        coursenum = row['coursenum']
        area = row['area']
        title = row['title']
        row = '%5s %4s %6s %4s %s' % (classid, dept, coursenum, area, title)

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
    parser.add_argument(dest="host", metavar="host",help="the computer on which the server is running",
                        type=str)
    parser.add_argument(dest="port", metavar="port",help="the port at which the server is listening",
                        type=int)
    args = parser.parse_args()

    payload = ['get_overviews', {
        "dept": args.dept,
        "coursenum": args.num,
        "area": args.area,
        'title': args.title
    }]

    if payload[1]["dept"] is None:
        payload[1]["dept"] = ''
    
    if payload[1]["coursenum"] is None:
        payload[1]["coursenum"] = '' # Handle ignore on server side
    
    if payload[1]["area"] is None:
        payload[1]["area"] = '' #To allow SQL to ignore
    if payload[1]["title"] is None:
        payload[1]["title"] = '' #To allow SQL to ignore

    try:
        host = sys.argv[1]
        port = int(sys.argv[2])

        with socket.socket() as sock:
            sock.connect((host, port))
            
            flo = sock.makefile(mode='w', encoding='utf-8')
            flo.write(json.dumps(payload) + '\n') # This needs to have \n for write to work correctly
            flo.flush()

            flo.close()

            result = sock.makefile('r', encoding='utf-8')
            result_text = json.loads(result.read())
            if result_text[0]:
                dict_results = result_text[1]
                format_reg_response(dict_results)
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)
    finally:
        sock.close()


if __name__ == "__main__":
    main()


