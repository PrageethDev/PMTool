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
This will send http requests to the selected server and check for responses and calculate the time for roundtrips.
Here, a request-batch is the word to state how many requests to fire at once; which means how many requests to fire within a second.

1) Basic no. of requests in a request-batch at the beginning? (TPS); This means how many requests to fire at once in the beginning,
this request quantity can be increment later. State how many requests should fire at the first fire.

2) How many request-batches to fire ?; This mean how many times this request-batches should run? request quantity in these batches can be
incremented or can keep constantly

3) Basic time interval between two request-batches at the beginning? Enter time in Seconds; there could be time interval between
two firings, so the next request batch will hold for some time after firing the previous request-batch

4) Time interval increment between two request-batches? Enter time in Seconds; The time interval can be incremented when firing
request-batches, if you give 0 in here there will be no time interval incrementation between two request-batches.
Or you can give a number, so the time will be incremented by that no. of seconds.

5) Requests incrementation for batches?; Requests in a batch also can be incremented with giving a no. for this. If you don't want to
increment no. of requests in a request-batch you can insert 0.

6) URL of the testing server?; Just provide the url of the server you wanted to connect. You can also insert it using the ip and the port.

7) Time out for a request? insert in seconds; request timeout in seconds.



MySQL test
-----------------
1) Enter the host ip

2) Enter the user name of the mysql user you want to login

3) Then enter the password for the mysql user 

4) Finally enter the name of the database you want to test




Checking a remote servers current usage
------------------


























