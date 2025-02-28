import argparse
import socket
import sys
import json
import textwrap

parser = argparse.ArgumentParser(description =
                    "Registrar application: \
                    show details about a class")

# Not formatting responses correctly
def format_reg_response(dict_results):
    output = []
    output.append("-------------")
    output.append("Class Details")
    output.append("-------------")
    # Get results from dictionary

    output.append(f"Class Id: {dict_results['classid']}")

    output.append(f"Days: {dict_results['days']}")

    output.append(f"Start time: {dict_results['starttime']}")

    output.append(f"End time: {dict_results['endtime']}")

    output.append(f"Building: {dict_results['bldg']}")

    output.append(f"Room: {dict_results['roomnum']}")

    output.append("--------------")
    output.append("Course Details")
    output.append("--------------")
    output.append(f"Course Id: {dict_results['courseid']}")

    for item in dict_results['deptcoursenums']:
        output.append(f"Dept and Number: {item['dept'] +
                        " " + item['coursenum']}")

    output.append(f"Area: {dict_results['area']}")

    output.append(f"Title: {dict_results['title']}")

    output.append(f"Description: {dict_results['descrip']}")

    output.append(f"Prerequisites: {dict_results['prereqs']}")

    for prof in dict_results['profnames']:
        output.append(f"Professor: {prof}")

    for row in output:
        wrapped_text = textwrap.fill(row,
                                     width=72,subsequent_indent='   ')
        print(wrapped_text)


    # Formatting based on requirements


def main():
    # Set up help options

    parser.add_argument(dest="host", metavar="host",
                        help="the computer on \
                        which the server is running",
                        type=str)
    parser.add_argument(dest="port", metavar="port",
                        help="the port at which the \
                            server is listening",
                        type=int)
    parser.add_argument(dest="classid", metavar="classid",
                        help="the id of the class whose \
                            details should be shown",
                        type=int)
    args = parser.parse_args()

    payload = ['get_details', args.classid]

    try:
        host = sys.argv[1]
        port = int(sys.argv[2])

        with socket.socket() as sock:
            sock.connect((host, port))

            flo = sock.makefile(mode='w', encoding='utf-8')
            flo.write(json.dumps(payload) + '\n')
            # This needs to have \n for write to work correctly
            flo.flush()

            flo.close()

            result = sock.makefile('r', encoding='utf-8')
            result_text = json.loads(result.read())
            if result_text[0]:
                dict_results = result_text[1]
                format_reg_response(dict_results)
            else:
                print(f"{sys.argv[0]}: {result_text[1]}")
                sys.exit(1)
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)
    finally:
        sock.close()


if __name__ == "__main__":
    main()
