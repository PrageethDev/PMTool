# PMTool

How to install
------------------
Place the PMTool directory where you like
then run the PMTool.py script using the terminal

NOTE: Python 2x has to be installed in your server
following libraries should also be installed for python
MySQLdb
logging
paramiko
requests
time
threading
datetime
traceback
_mysql
sys

How to use
------------------
There are 4 options in the main menu
1) Web test
2) MySQL test
3) Checking a remote servers current usage
4) Web test with remote servers usage

Web test
------------------
This will send http requests to the selected server and check for responses and calculate the time for roundtrips
1) enter the url of the server you want to perform the web test, just type the url or ip address and the port of the server; program will auto add the http:// infront of the url.

2) Then enter the time out time for requests, use seconds.

3) Then enter the number of users to send requests for the server; program will create a thread for each user and send requests parellaly.

4) Then enter the number of request-batches to fire from a user; this means how many times you want to send sets of requests. A request-batch can consist any no. of requests. requests in a request-batch will fire continuesly one after one. But request-batches will start with a given time interval.

5) Enter the time interval between two request-batches; this should be in seconds.

6) Then enter the basic no. of requests in a request-batch. This will be the starting no. of requests in a request-batch.

7) Then enter the requests incrementation for batches. This is the incrementing no. of requests for each batch. (eg: if the incrementing no. is 2, then second batch will send 2 more reqests than in the first batch)

8) Then select the http request type you want.



MySQL test
-----------------
1) Enter the host ip

2) Enter the user name of the mysql user you want to login

3) Then enter the password for the mysql user 

4) Finally enter the name of the database you want to test




Checking a remote servers current usage
------------------


























