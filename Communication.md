The Communication Protocol
The given client programs and your client programs must communicate with the given server program and your server program. For that to be possible, the client programs and server programs must use a defined communication protocol. This section specifies that protocol.

Suppose a client wants to fetch class overviews. In that case the client must send to the server a JSON document representing a Python object. The object must be a list object. The first element of the list object must be the str object "get_overviews". The second element of the list object must must be a dict object. There must be four bindings in the list object, having keys "dept", "coursenum", "area", and "title". (The values of some of the bindings might be the empty string.) For example, a client might send to a server a JSON document representing this Python object:

['get_overviews', {'dept':'COS', 'coursenum':'2', 'area':'qr', 'title':'intro'}]
In response, the server must send to the client a JSON document representing a Python object. The object must be a list object. The first element of the list object must be a bool object — indicating whether the server handled the request successfully or not. If the bool object is False, then the second element must be a str object which is an error message. If the bool object is True, then the second element must be a list object. Each element of the list object must be a dict object containing the data for one class. For example, if the client sends the server the above request (and there are no errors), then the server must send to the client a JSON representation of this Python object:

[True, [
{'classid':8308, 'dept':'COS', 'coursenum':'217', 'area':'QR',
'title':'Introduction to C_Science Programming Systems'},
{'classid':9240, 'dept':'COS', 'coursenum':'342', 'area':'QR',
'title':'Introduction to Graph Theory'}]]
The classes within the list object must be sorted; the primary sort must be by dept in ascending order, the secondary sort must be by coursenum in ascending order, and tertiary sort must be by classid in ascending order.

Now suppose a client wants to fetch class details. In that case the client must send to the server a JSON document representing a Python object. The object must be a list object. The first element of the list object must be the str object "get_details". The second element of the list object must an int object which is a classid. For example, a client might send to a server a JSON representation of this Python object:

['get_details', 8321]
In response, the server must send to the client a JSON document representing a Python object. The object must be a list object. The first element of the list object must be a bool object — indicating whether the server handled the request successfully or not. If the bool object is False, then the second element must be a str object which is an error message. If the bool object is True, then the second element must be a dict object containing the details for the specified class. For example, if the client sends the server the above request (and there are no errors), then the server must send to the client a JSON representation of this Python object:

[True, {
'classid':8321,
'days':'TTh',
'starttime':'11:00AM',
'endtime':'12:20PM',
'bldg':'FRIEN',
'roomnum':'006',
'courseid':3672,
'deptcoursenums':[{'dept': 'COS', 'coursenum': '333'}],
'area':'',
'title':'Advanced C%Science Programming Techniques',
'descrip':'This is a course about the practice of programming. Programming is more than just writing code. Programmers must also assess tradeoffs, choose among design alternatives, debug and test, improve performance, and maintain software written by themselves & others. At the same time, they must be concerned with compatibility, robustness, and reliability, while meeting specifications. Students will have the opportunity to develop these skills by working on their own code and in group projects.',
'prereqs':'COS 217 and COS 226.',
'profnames': ['Brian W. Kernighan']
}]
Within the deptcoursenums list the elements must be sorted primarily by department and secondarily by course number. Within the profnames list the elements must be sorted.
