import os
import sys
import socket
import time
import json
import argparse
import sqlite3 as sql
import contextlib
import textwrap
import sys
import threading
import time
import dotenv 

dotenv.load_dotenv()

parser = argparse.ArgumentParser()

DATABASE_URL = r"file:COS_333_A2\reg.sqlite?mode=ro"
TESTING = True

CDELAY = int(os.environ.get("CDELAY", "0"))
IODELAY = int(os.environ.get("IODELAY", "0"))
       
def consume_cpu_time(delay):
    initial_thread_time = time.thread_time()
    while (time.thread_time() - initial_thread_time) < delay:
        pass


class ChildThread (threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        print("Spawned child thread")
        self._sock = sock

    def run(self):
        call = self._sock.makefile(mode="r", encoding='utf-8')
        call_data = call.readline()

        actual_call = json.loads(call_data)
        print(f'Received request: {actual_call}')
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
            flo = self._sock.makefile(mode="w", encoding="utf-8")
            # Potentially use inflo/outflo here
            flo.write(json.dumps(payload) + "\n")
            flo.flush()

            # return json.dumps(payload)

        elif actual_call[0] == 'get_details':
            class_id = int(actual_call[1]) # the second argument is supposed to the class id
            classinfo = get_class_info(class_id)

            if not classinfo[0]:
                flo = self._sock.makefile(mode="w", encoding="utf-8")
                flo.write(json.dumps(classinfo) + "\n")
                flo.flush()
            else:

                # Return just the course number, which is [True, (coursenum, ....)].
                infosets = get_course_info(classinfo[1][0])



                if not infosets[0]:
                    flo = self._sock.makefile(mode="w", encoding="utf-8")
                    flo.write(json.dumps(infosets) + "\n")
                    flo.flush()
                
                else:

                    # CHANGE THIS LATER
                    payload = [True, details_format(classinfo[1], infosets[1], infosets[2], infosets[3])]

                    flo = self._sock.makefile(mode="w", encoding="utf-8")
                    flo.write(json.dumps(payload) + "\n")
                    flo.flush()
        print("Closed socket in child thread")
        print("Exiting child thread")
#-----------------------------------------------------------------------

def return_overviews_query(department='%', course_number='%',
                 distribution_area='%', class_title='%'):
    time.sleep(IODELAY)
    consume_cpu_time(CDELAY)
    if department == '':
        department = '%'
    else:
        pass
        department = department.replace('_', r'\_') #Replace underscores
        department = department.replace('%', r'\%') #Replace %'s

    if course_number == '':
        course_number = '%'
    else:
        pass
        course_number = course_number.replace('_', r'\_')
        course_number = course_number.replace('%', r'\%')

    if distribution_area == '':
        distribution_area = '%' #To allow SQL to ignore
    else:
        pass
        distribution_area = distribution_area.replace('_', r'\_')
        distribution_area = distribution_area.replace('%', r'\%')
    if class_title == '':
        class_title = '%' #To allow SQL to ignore
    else:
        pass
        class_title = class_title.replace('_', r'\_')
        class_title = class_title.replace('%', r'\%')

    try:
        
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
                order_of_keys = ['classid', 'dept', 'coursenum', 'area', 'title']

                # Converts each row in the table to a key: value dictionary
                dictionized_table = [{key: value for key, value in zip(order_of_keys, row)} for row in table]

                return True, dictionized_table
    except Exception as ex:
        return False, f"{sys.argv[0]}: {ex}"


def get_class_info(classid):
    time.sleep(IODELAY)
    consume_cpu_time(CDELAY)
    try:
        # Connect to database
        time.sleep(IODELAY)
        consume_cpu_time(CDELAY)
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
                    return False, "no class with " + f"classid {classid} exists"
                return True, table[0]
        return False, "Error: database could not be opened."
    except Exception as ex:
        return False, f"{sys.argv[0]}: {ex}"


def get_course_info(classid):
    classid = int(classid)
    time.sleep(IODELAY)
    consume_cpu_time(CDELAY)
    try:
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
                    return False, "no class with " +f"classid {classid} exists"

                # Get all info from crosslistings on courseid
                query = """SELECT dept, coursenum FROM crosslistings c
                WHERE c.courseid = ? ORDER BY dept ASC, coursenum ASC"""
                cursor.execute(query, [classid])
                crosslistings_info = cursor.fetchall()

                # Ensure there was a response
                if len(crosslistings_info) == 0:
                    return False, "no class with " + f"classid {classid} exists"

                # Merge coursesprofs and profs, and get relevant names
                query = """SELECT profname FROM coursesprofs, profs
                        WHERE coursesprofs.profid = profs.profid AND
                        courseid = ? ORDER BY profname ASC"""
                cursor.execute(query, [classid])
                prof_info = cursor.fetchall()

                return True, course_info, crosslistings_info, prof_info

    except Exception as ex:
        return False, f"{sys.argv[0]}: {ex}"

# ['classid', 'courseid', 'days', 'starttime', 'endtime', 'bldg', 'roomnum', 'deptcoursenums': {'dept': ... , 'coursenum': ...}, 'area', 'title', 'descrip', 'prereqs', 'profnames': [...]]

# Formats the isolated responses into a data dictionary
def details_format(class_info, course_info, crosslistings_info, res4):

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


#-----------------------------------------------------------------------

def main():
    if len(sys.argv) != 2:
        print('Usage: python %s port' % sys.argv[0])
        sys.exit(1)

    try:
        port = int(sys.argv[1])

        server_sock = socket.socket()
        print('Opened server socket')
        if os.name != 'nt':
            server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind(('', port))
        print('Bound server socket to port')
        server_sock.listen()
        print('Listening')

        while True:
            try:
                sock, client_addr = server_sock.accept()
                print('Accepted connection, opened socket')
                with sock:
                    
                    child_thread = ChildThread(sock)
                    child_thread.start()
                    child_thread.join()
            except Exception as ex:
                print(ex, file=sys.stderr)

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
