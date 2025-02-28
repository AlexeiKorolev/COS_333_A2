import os
import sys
import socket
import json
import argparse
import sqlite3 as sql
import contextlib
import time
import dotenv

dotenv.load_dotenv()

parser = argparse.ArgumentParser()

DATABASE_URL = r"file:reg.sqlite?mode=ro"
TESTING = True

try:
    CDELAY = int(os.environ.get("CDELAY", "0"))
    IODELAY = int(os.environ.get("IODELAY", "0"))
except Exception:
    CDELAY = 0 # Assume CDELAY and IODELAY = 0
    IODELAY = 0



# Function to actively consume CPU time, with delay being the
# number of seconds to perform computations.
def consume_cpu_time(delay):
    initial_thread_time = time.thread_time()
    while (time.thread_time() - initial_thread_time) < delay:
        pass

#-----------------------------------------------------------------------


# Returns a course overviews query from the
# database given a search substring
# for the department, course number, distribution
# area, and/or class title.
# If the query was successful, then the return tuple
# is (True, QUERY_RESULT),
# and if the query failed, then the return looks
# like (False, ERROR_MESSAGE)
def return_overviews_query(department='%', course_number='%',
                 distribution_area='%', class_title='%'):
    if department == '':
        department = '%'
    else:
        pass

    if course_number == '':
        course_number = '%'
    else:
        pass

    if distribution_area == '':
        distribution_area = '%' #To allow SQL to ignore
    else:
        pass

    if class_title == '':
        class_title = '%' #To allow SQL to ignore
    else:
        pass


    try:
        time.sleep(IODELAY)
        consume_cpu_time(CDELAY)

        with sql.connect(DATABASE_URL,
            isolation_level=None, uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:
                query_statement = r""" SELECT classes.classid,
                    crosslistings.dept, crosslistings.coursenum, courses.area, courses.title
                    FROM courses
                    INNER JOIN crosslistings ON courses.courseid=crosslistings.courseid
                    INNER JOIN classes ON classes.courseid=courses.courseid
                    WHERE crosslistings.dept LIKE ? AND crosslistings.coursenum LIKE ?
                    AND courses.area LIKE ? AND courses.title LIKE ? ESCAPE '\'
                    ORDER BY crosslistings.dept ASC, crosslistings.coursenum ASC, classes.classid ASC
                        """# Run the necessary query

                cursor.execute(query_statement, ['%' + department + '%',
                                        '%' + course_number + '%',
                                        '%' + distribution_area + '%',
                                        '%' + class_title + '%']) 
                #Prevent SQL injections
                table = cursor.fetchall() # fetch query results
                order_of_keys = ['classid', 'dept', 'coursenum',
                                 'area', 'title']

                print("creating dictionized table")

                # Converts each row in the
                # table to a key: value dictionary
                dictionized_table = [dict(zip(order_of_keys, row))
                                      for row in table]


                print("Returning a table with"
                      + f"{len(dictionized_table)} elements")

                return True, dictionized_table
    except Exception as ex:
        return False, f"{sys.argv[0]}: {ex}"



# Given a classid, returns a tuple with True and a list containing the
# courseid, days, starttime, endtime, bldg, roomnum, and classid if the
# classid exists, otherwise it returns (False, ERROR_MESSAGE)
def get_class_info(classid):
    try:
        time.sleep(IODELAY)
        consume_cpu_time(CDELAY)
        # Connect to database
        with sql.connect(DATABASE_URL,
                         isolation_level=None, uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:

                # Fetch relevant class info
                sql_statement = """SELECT courseid, days, starttime,
                endtime, bldg, roomnum, classid FROM classes cls WHERE
                cls.classid = ?"""
                cursor.execute(sql_statement, [classid])
                table = cursor.fetchall()

                # Ensure there was a response
                if len(table) == 0:
                    return (False, "no class with "
                + f"classid {classid} exists")
                return True, table[0]
        return False, "Error: database could not be opened."
    except Exception as ex:
        print(str(ex))
        return (False,
                "A server error occurred. Please contact " +
                "the system administrator.")


# Given the courseid, returns a tuple with (True, COURSE_INFO)
# if successful,
# and (False, ERROR_MESSAGE) otherwise.
def get_course_info(classid):
    classid = int(classid)
    try:
        time.sleep(IODELAY)
        consume_cpu_time(CDELAY)
        # Connect to the database
        with sql.connect(DATABASE_URL, isolation_level=None,
                         uri=True) as connection:
            with contextlib.closing(connection.cursor()) as cursor:

                # Get all info from courses on courseid
                query = """SELECT area, title, descrip, prereqs
                        FROM courses c WHERE c.courseid = ?"""
                cursor.execute(query, [classid])
                course_info = cursor.fetchall()

                # Ensure there was a response
                if len(course_info) == 0:
                    return (False, "no class with "
                + f"classid {classid} exists")

                # Get all info from crosslistings on courseid
                query = """SELECT dept, coursenum FROM crosslistings c
                WHERE c.courseid = ? ORDER BY dept ASC, coursenum ASC"""
                cursor.execute(query, [classid])
                crosslistings_info = cursor.fetchall()
                print(f"crosslistings_info: {crosslistings_info}")
                print(f"classid: {classid}")

                # Ensure there was a response
                if len(crosslistings_info) == 0:
                    return (False, "no class with "
                + f"classid {classid} exists")

                # Merge coursesprofs and profs, and get relevant names
                query = """SELECT profname FROM coursesprofs, profs
                        WHERE coursesprofs.profid = profs.profid AND
                        courseid = ? ORDER BY profname ASC"""
                cursor.execute(query, [classid])
                prof_info = cursor.fetchall()
                print(f"prof_info: {prof_info}")

                return True, course_info, crosslistings_info, prof_info

    except Exception as ex:
        return False, f"{sys.argv[0]}: {ex}"


# Formats the isolated responses into a data dictionary
def details_format(class_info, course_info, crosslistings_info, res4):
    print(f"courseinfo: {course_info}")
    print(f"class_info: {class_info}")
    print(f"res4: {res4}")
    print(f"crosslistings_info: {crosslistings_info}")
    return {
        "classid": class_info[6],
        "courseid": class_info[0],
        "days": class_info[1],
        "starttime": class_info[2],
        "endtime": class_info[3],
        "bldg": class_info[4],
        "roomnum": class_info[5],
        "deptcoursenums": [{"dept": dept, "coursenum": coursenum} 
                          for dept, coursenum in crosslistings_info],
        "area": course_info[0][0],
        "title": course_info[0][1],  
        "descrip": course_info[0][2],  
        "prereqs": course_info[0][3],  
        "profnames": [profname for profname, in res4]
    }


def handle_client(sock):
    call = sock.makefile(mode="r", encoding='utf-8')
    print(f"call: {call}")
    call_data = call.readline()
    print("GOT HERE!")

    actual_call = json.loads(call_data)
    print(f"actual call: {actual_call}")
    if actual_call[0] == 'get_overviews':
        args = {
            "dept": None,
            "coursenum": None,
            "area": None,
            'title': None
        }
        given_args = actual_call[1]

        for arg, val in given_args.items():
            args[arg] = val

        payload =  return_overviews_query(department=args["dept"],
                            course_number=args["coursenum"],
                            distribution_area=args["area"],
                            class_title=args["title"])
        flo = sock.makefile(mode="w", encoding="utf-8")
        # Potentially use inflo/outflo here
        flo.write(json.dumps(payload) + "\n")
        flo.flush()

        # return json.dumps(payload)

    elif actual_call[0] == 'get_details':
        print(actual_call, type(actual_call[1]))
        class_id = int(actual_call[1])
        print("got past classid")
        classinfo = get_class_info(class_id)

        if not classinfo[0]:
            flo = sock.makefile(mode="w", encoding="utf-8")
            flo.write(json.dumps(classinfo) + "\n")
            flo.flush()

        infosets = get_course_info(classinfo[1][0])

        if not infosets[0]:
            flo = sock.makefile(mode="w", encoding="utf-8")
            flo.write(json.dumps(infosets) + "\n")
            flo.flush()

        # CHANGE THIS LATER
        print(f"infosets here: {infosets[0]}")
        payload = [True, details_format(classinfo[1],
                                        infosets[1],
                                        infosets[2],
                                        infosets[3])]

        print(f"payload: {payload}")

        flo = sock.makefile(mode="w", encoding="utf-8")
        flo.write(json.dumps(payload) + "\n")
        flo.flush()
#-----------------------------------------------------------------------

# Runs the main process. Starts a server at the given port, and returns
# the queries sent in by the client. Supports the get_details and
# get_overviews functions
def main():
    if len(sys.argv) != 2:
        print('Usage: python %s port' % sys.argv[0])
        sys.exit(1)

    try:
        port = int(sys.argv[1])

        server_sock = socket.socket()
        print('Opened server socket')
        if os.name != 'nt':
            server_sock.setsockopt(socket.SOL_SOCKET,
                                   socket.SO_REUSEADDR, 1)
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
                    print('Client IP addr and port:',
                          client_addr)
                    handle_client(sock)
            except Exception as ex:
                print(ex, file=sys.stderr)

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
