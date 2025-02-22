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

parser = argparse.ArgumentParser()

DATABASE_URL = r"file:reg.sqlite?mode=ro"
TESTING = True
#-----------------------------------------------------------------------

def return_overviews_query(department='%', course_number='%',
                 distribution_area='%', class_title='%'):
    if department is None:
        department = '%'
    else:
        department = department.replace('_', r'\_') #Replace underscores
        department = department.replace('%', r'\%') #Replace %'s

    if course_number is None:
        course_number = '%'
    else:
        course_number = course_number.replace('_', r'\_')
        # Replace underscores
        course_number = course_number.replace('%', r'\%')
        # Replace %'s

    if distribution_area is None:
        distribution_area = '%' #To allow SQL to ignore
    else:
        distribution_area = distribution_area.replace('_', r'\_')
        distribution_area = distribution_area.replace('%', r'\%')
    if class_title is None:
        class_title = '%' #To allow SQL to ignore
    else:
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

                # format_response(table)
                return True, table
    except Exception as ex:
        return False, f"{sys.argv[0]}: {ex}"

def get_class_info(classid):
    try:
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
                    return False, "regdetails.py: no class with " + f"classid {classid} exists"
                return True, table[0]
        return False, "Error: database could not be opened."
    except Exception as ex:
        return False, f"{sys.argv[0]}: {ex}"


def get_course_info(classid):
    classid = int(classid)
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
                    return False, "regdetails.py: no class with " +f"classid {classid} exists"

                # Get all info from crosslistings on courseid
                query = """SELECT dept, coursenum FROM crosslistings c
                WHERE c.courseid = ? ORDER BY dept ASC, coursenum ASC"""
                cursor.execute(query, [classid])
                crosslistings_info = cursor.fetchall()

                # Ensure there was a response
                if len(crosslistings_info) == 0:
                    return False, "regdetails.py: no class with " + f"classid {classid} exists"

                # Merge coursesprofs and profs, and get relevant names
                query = """SELECT profname FROM coursesprofs, profs
                        WHERE coursesprofs.profid = profs.profid AND
                        courseid = ? ORDER BY profname ASC"""
                cursor.execute(query, [classid])
                prof_info = cursor.fetchall()

                # Ensure there was a response
                if len(prof_info) == 0:
                    return False, "regdetails.py: no class with " + f"classid {classid} exists"

                return True, course_info, crosslistings_info, prof_info

    except Exception as ex:
        return False, f"{sys.argv[0]}: {ex}"

# Formats the isolated responses into a data dictionary
def details_format(class_info, course_info, crosslistings_info, res4):
    return {
        "courseid": class_info[0],
        "days": class_info[1],
        "starttime": class_info[2],
        "endtime": class_info[3],
        "building": class_info[4],
        "roomnum": class_info[5],
        "classid": class_info[6],
        "area": course_info[0][0],
        "title": course_info[0][1],
        "description": course_info[0][2],
        "prerequisites": course_info[0][3],
        "crosslistings": [{"dept": dept, "coursenum": coursenum} 
                          for dept, coursenum in crosslistings_info],
        "profs": [profname for profname, in res4]
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
        class_id = actual_call[1] # the second argument is supposed to the class id
        classinfo = get_class_info(class_id)

        if not classinfo[0]:
            return json.dumps(classinfo) # return False with the exception

        infosets = get_course_info(classinfo[1])

        if not infosets[0]:
            return json.dumps(infosets) # Return False with the exception

        
        resp = details_format(classinfo, infosets[1], infosets[2], infosets[3])

        flo = sock.makefile(mode="w", encoding="utf-8")
        # Potentially use inflo/outflo here
        flo.write("hello")
        flo.flush()
        # return json.dumps((True, resp)) # Insert True before the return

def handle_client_1(sock):
    datetime = time.asctime(time.localtime())
    flo = sock.makefile(mode='w', encoding='ascii')
    flo.write(datetime + '\n')
    flo.flush()
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
                with sock:
                    print('Accepted connection')
                    print('Opened socket')
                    print('Server IP addr and port:', sock.getsockname())
                    print('Client IP addr and port:', client_addr)
                    handle_client(sock)
            except Exception as ex:
                print(ex, file=sys.stderr)

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
