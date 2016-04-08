#!/usr/bin/python
import MySQLdb
import logging
import paramiko
import requests
import time
import threading
from datetime import datetime
import traceback
import _mysql
import sys


threadsForWebTests = []
threadsForRemoteServerTests = []
threadsForMySQLTests = []

setThreadID = 1

queueLock = threading.Lock()
lockRelease = 0

logging.basicConfig(filename='log/PerformenceMeter.log', level=logging.DEBUG)
logger1 = logging.getLogger('RSTest')
logger2 = logging.getLogger('myapp.area2')

#Variables for web tests

#No of threads in the begining (Requests in a request-batch)
noOfThrInTheBeg = 0

#Request-batch count
reqBatCou = 0

#Time interval
timInt = 0

#Increment number
reqBatCouInc = 0

#Time incrementation
timIntInc = 0


class threadForWebTest (threading.Thread):

    tesSerURL = "" #http://google.lk
    timeToWait = 1


    requestType = 0

    fireNum = 0

    finishingTheThread = 0


    def __init__(self, threadID, threadName):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = threadName

    def run(self):
        print "Starting " + self.threadID + ", " + self.threadName + " at " + str(datetime.now())
        logging.info("Starting " + self.threadID + ", " + self.threadName + " at " + str(datetime.now()))

        self.processingWorks(self.threadID)

        print "Exiting " + self.threadID + " at " + str(datetime.now())
        logging.info("Exiting " + self.threadID + " at " + str(datetime.now()))



    def httpHeadRequest(self, threadID):
        self.fireNum += 1
        try:
            requestTime = datetime.now()
            response = requests.head(self.tesSerURL, timeout=self.timeToWait) #timeout - timeToWaitForARequest
            response.content  # wait until full content has been transfered
            responseTime = datetime.now()

            transactionTime = responseTime - requestTime

            logging.info(str(threadID) + " HEAD request " + str(self.fireNum) + " fired successfully at " + str(requestTime) + " to " + str(self.tesSerURL))
            logging.info(str(threadID) + " response " + str(self.fireNum) + " receive completed at " + str(responseTime) + "  status code: " + str(response.status_code) + " roundtrip time: " + str(transactionTime))

            print (str(threadID) + " HEAD request " + str(self.fireNum) + " fired successfully at " + str(requestTime) + " to " + str(self.tesSerURL))
            print (str(threadID) + " response " + str(self.fireNum) + " receive completed at " + str(responseTime) + "  status code: " + str(response.status_code) + " roundtrip time: " + str(transactionTime))

        except Exception as printExcep:
            requestTime = datetime.now()
            #traceback.print_exc()
            logging.info(str(threadID) + " HEAD request " + str(self.fireNum) + " fired, but completion failed at " + str(requestTime) + " to " + str(self.tesSerURL))
            logging.info(str(printExcep))
            print (str(threadID) + " HEAD request " + str(self.fireNum) + " fired, but completion failed at " + str(requestTime) + " to " + str(self.tesSerURL))
            print printExcep
            pass


    def httpGetRequest(self, threadID):

        self.fireNum += 1
        try:
            requestTime = datetime.now()
            response = requests.get(self.tesSerURL, timeout=self.timeToWait) #timeout - timeToWaitForARequest
            response.content  # wait until full content has been transfered
            responseTime = datetime.now()

            transactionTime = responseTime - requestTime

            logging.info(str(threadID) + " GET request " + str(self.fireNum) + " fired successfully at " + str(requestTime) + " to " + str(self.tesSerURL))
            logging.info(str(threadID) + " response " + str(self.fireNum) + " receive completed at " + str(responseTime) + "  status code: " + str(response.status_code) + " roundtrip time: " + str(transactionTime))

            print (str(threadID) + " GET request " + str(self.fireNum) + " fired successfully at " + str(requestTime) + " to " + str(self.tesSerURL))
            print (str(threadID) + " response " + str(self.fireNum) + " receive completed at " + str(responseTime) + "  status code: " + str(response.status_code) + " roundtrip time: " + str(transactionTime))

        except Exception as printExcep:
            requestTime = datetime.now()
            #traceback.print_exc()
            logging.info(str(threadID) + " GET request " + str(self.fireNum) + " fired, but completion failed at " + str(requestTime) + " to " + str(self.tesSerURL))
            logging.info(str(printExcep))
            print (str(threadID) + " GET request " + str(self.fireNum) + " fired, but completion failed at " + str(requestTime) + " to " + str(self.tesSerURL))
            print printExcep
            pass

    def httpPostRequest(self, threadID):

        self.fireNum += 1

        with open('config/post.txt', 'r') as postData:
            writePostData = postData.read()

        try:

            requestTime = datetime.now()
            response = requests.post(self.tesSerURL, data=writePostData, timeout=self.timeToWait) #timeout - timeToWaitForARequest
            response.content  # wait until full content has been transfered
            responseTime = datetime.now()

            transactionTime = responseTime - requestTime

            logging.info(str(threadID) + " POST request " + str(self.fireNum) + " fired successfully at " + str(requestTime) + " to " + str(self.tesSerURL))
            logging.info(str(threadID) + " response " + str(self.fireNum) + " receive completed at " + str(responseTime) + "  status code: " + str(response.status_code) + " roundtrip time: " + str(transactionTime))

            print (str(threadID) + " POST request " + str(self.fireNum) + " fired successfully at " + str(requestTime) + " to " + str(self.tesSerURL))
            print (str(threadID) + " response " + str(self.fireNum) + " receive completed at " + str(responseTime) + "  status code: " + str(response.status_code) + " roundtrip time: " + str(transactionTime))

        except Exception as printExcep:
            requestTime = datetime.now()
            #traceback.print_exc()
            logging.info(str(threadID) + " POST request " + str(self.fireNum) + " fired, but completion failed at " + str(requestTime) + " to " + str(self.tesSerURL))
            logging.info(str(printExcep))
            print (str(threadID) + " POST request " + str(self.fireNum) + " fired, but completion failed at " + str(requestTime) + " to " + str(self.tesSerURL))
            print printExcep
            pass




    def firingHttpRequests(self, threadID):
        time.sleep(1)
        if self.requestType == 2:
                self.httpGetRequest(threadID)

        elif self.requestType == 3:
                self.httpPostRequest(threadID)

        elif self.requestType == 1:
                self.httpHeadRequest(threadID)





    def processingWorks(self, threadID):
        queueLock.acquire()
    #Releasing the lock
        while 1:
            if lockRelease == 1:
                if queueLock.locked():
                    queueLock.release()

                self.firingHttpRequests(threadID)
                break




class threadForRemoteServerTest(threading.Thread):

    # ssh credential.
    ip = ''#'127.0.0.1'
    userName = ''#'prageeth'
    password = ''

    activeIndicator = 0

    def __init__(self, threadID, threadName):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = threadName

    def run(self):

        print "Starting " + self.threadID + ", " + self.threadName + " at " + str(datetime.now())
        logging.info("Starting " + self.threadID + ", " + self.threadName + " at " + str(datetime.now()))

        self.processingWorks(self.threadID)

        print "Exiting " + self.threadID + " at " + str(datetime.now())
        logging.info("Exiting " + self.threadID + " at " + str(datetime.now()))


    def processingWorks(self, threadID):
        queueLock.acquire()
    #Releasing the lock
        for x in range(0, 1000):
            time.sleep(0.001)
            if lockRelease == 1:
                if queueLock.locked():
                    queueLock.release()
                self.connectingToRemoteServer(threadID)
                break



    def connectingToRemoteServer(self, threadID):
        global logger1
        # connection to the remote server
        command = ""

        ssh = paramiko.SSHClient()
        # set the ssh client, and force it to accept new/unknown host keys.
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(self.ip, username=self.userName, password=self.password, look_for_keys=False, allow_agent=False)
            print threadID, "Connected to ", self.userName, "@", self.ip

            #selecting the command
            selectingCommand = raw_input( "select the no. for the operation you want to perform in " + str(threadID) + " \n"
                                        "1) Show memory usage\n"
                                        "2) Show CPU usage\n")

            RSTestLoopCount = input("how many times the test should perform?")
            RSTestWaitTime = input("What is the time interval between two tests")

            if selectingCommand == "1":
                command = 'free'
            elif selectingCommand == "2":
                command = 'free'

        except Exception:
            print "Can't login to remote server; check credentials"
            pass

        self.activeIndicator = 1

        try:
            y = 0
            while (RSTestLoopCount != y):
                stdin, stdout, stderr = ssh.exec_command(command)

                # read each line of the free -m command for pretty printing in the next step
                type(stdin)
                output = stdout.readlines()
                logging.info(str(threadID) + str(datetime.now()))
                logger1.info(str(threadID) + str(datetime.now()))
                print threadID + str(datetime.now())
                # this will display the output
                length = len(output)
                for x in range(0, length):
                    logging.info(str(output[x]))
                    logger1.info(str(output[x]))
                    print output[x]

                y += 1
                time.sleep(RSTestWaitTime)

        except Exception as printExcept:
            traceback.print_exc()
            print printExcept
            print "Can't perform the test in the remote server"
            pass
        ssh.close()

        self.activeIndicator = 1


class threadForMySQLTest(threading.Thread):
    dbHost = "" #127.0.0.1
    dbUserName = "" #Prageeth
    dbPassword = "" #123987
    dbName = "" #test


    finishingTheThread = 0

    def __init__(self, threadID, threadName):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadName = threadName

    def run(self):

        print "Starting " + self.threadID + ", " + self.threadName + " at " + str(datetime.now())
        logging.info("Starting " + self.threadID + ", " + self.threadName + " at " + str(datetime.now()))

        self.processingWorks(self.threadID)

        print "Exiting " + self.threadID + " at " + str(datetime.now())
        logging.info("Exiting " + self.threadID + " at " + str(datetime.now()))


    def processingWorks(self, threadID):
        queueLock.acquire()
    #Releasing the lock
        for x in range(0, 1000):
            time.sleep(0.001)
            if lockRelease == 1:
                if queueLock.locked():
                    queueLock.release()
                self.connectingAndTestingDB(threadID)
                break



    def connectingAndTestingDB(self, threadID):

        try:
            con = MySQLdb.connect(host=self.dbHost, user=self.dbUserName, passwd=self.dbPassword, db=self.dbName)
            #cur = con.cursor()

            con.query("SELECT VERSION()")
            result = con.use_result()

            print "MySQL version: %s" % \
                result.fetch_row()[0]

        except _mysql.Error, e:

            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)

        finally:

            if con:
                con.close()



def creatingUsers_threadsForWebTests():

    global lockRelease

    global noOfThrInTheBeg
    global reqBatCou
    global timInt
    global reqBatCouInc
    global timIntInc

    for x in range(1, reqBatCou +1):
        lockRelease = 0
        for y in range(1, noOfThrInTheBeg + 1):

            setThreadID = "Thread-" + str(y) + "_of_B" + str(x) + "_4WT"
            setThreadName = "Thread for web test-" + str(y) + "_of_B" + str(x)

            try:
                thread = threadForWebTest(setThreadID, setThreadName)
                thread.start()
                threadsForWebTests.append(thread)

            except Exception as e:
                print "Thread creating error in Thread-" + str(y) + "_of_B" + str(x)
                print e
                logging.warning("Thread creating error in Thread-" + str(y) + "_of_B" + str(x))
                pass
        lockRelease = 1
        time.sleep(timInt)
        noOfThrInTheBeg += reqBatCouInc
        timInt += timIntInc




def creatingUsers_threadsForRemoteServerTests():

    global lockRelease

    for x in range(1, 2):

        setThreadID = "Thread_RST-" + str(x)
        setThreadName = "Thread for RemoteServerTest-" + str(x)

        try:
            thread2 = threadForRemoteServerTest(setThreadID, setThreadName)
            thread2.start()
            threadsForRemoteServerTests.append(thread2)

        except Exception as e:
            traceback.print_exc()
            print "Thread creating error in ThreadRST-" + str(x)
            print e
            logging.warning("Thread creating error in Thread_RST-" + str(x))
            pass

    lockRelease = 1


def creatingUsers_threadsForDBTests():

    global lockRelease

    for x in range(1, 2):

        setThreadID = "Thread_DBT-" + str(x)
        setThreadName = "Thread for DataBaseTest-" + str(x)

        try:
            thread3 = threadForMySQLTest(setThreadID, setThreadName)
            thread3.start()
            threadsForMySQLTests.append(thread3)

        except Exception as e:

            print "Thread creating error in ThreadRST-" + str(x)
            print e
            logging.warning("Thread creating error in Thread_DBT-" + str(x))
            pass

    lockRelease = 1



def webTestInitialization():

    #No Of Users
    global noOfThrInTheBeg
    noOfThrInTheBeg = input("Basic no. of requests in a request-batch at the beginning? (TPS)")

    #request-batch count
    global reqBatCou
    reqBatCou = input("How many request-batches to fire ?")

    #time interval between two batches
    global timInt
    timInt = input("Basic time interval between two request-batches at the beginning? Enter time in Seconds")

    #Time interval incrementation between two batches
    global timIntInc
    timIntInc = input("Time interval increment between two request-batches? Enter time in Seconds")

    #Incrementation number
    global reqBatCouInc
    reqBatCouInc = input("Requests incrementation for batches?")




    #Testing server url
    chkURL = raw_input("URL of the testing server? http://")
    if chkURL == "":
        while (chkURL==""):
            chkURL = raw_input("Please enter the URL of the testing server? http://")
    url = "http://" + str(chkURL)
    print "Your url for the server is " + url
    threadForWebTest.tesSerURL = url

    #Waiting time
    threadForWebTest.timeToWait = input("Time out for a request? insert in seconds")

    #what type of request
    threadForWebTest.requestType = input("Select 1 to send HEAD requests\n"
                                        "Select 2 to send GET requests\n"
                                        "Select 3 to send POST requests")

    logging.info('A web test initialized at ' + str(datetime.now()) + ': TPS at the beginning=' + str(noOfThrInTheBeg) + ', TPS loop count='\
                 + str(reqBatCou) + ', Time interval at the beginning =' + str(timInt) + ', Request incrementation =' + str(reqBatCouInc))





def remoteServerUsageTestInitialization():
    #ip address of the remote server
    threadForRemoteServerTest.ip = raw_input("Enter the remote servers ip address")

    #name of the user
    threadForRemoteServerTest.userName = raw_input("Enter the name of the remote servers user")

    #password for the user
    threadForRemoteServerTest.password = raw_input("Enter the password for the remote servers user")


def mySQLPerformenceTestInitialization():
    #host ip of the dbserver
    threadForMySQLTest.dbHost = raw_input("Enter the host ip")

    #name of the user
    threadForMySQLTest.dbUserName = raw_input("Enter the user name")

    #password for the user
    threadForMySQLTest.dbPassword = raw_input("Enter the password for the user")

    #database to connect
    threadForMySQLTest.dbName = raw_input("Enter the database name")



def startingTheProgramme():
    print "Welcome to performence testing tool"
    selectingOpt = input("Please select number for the test you want to perform\n"
                          "1) Web test\n"
                          "2) MySQL test\n"
                          "3) Checking a remote servers current usage\n"
                         ""
                          "4) Web test with remote servers usage")


    if selectingOpt == 1:
        webTestInitialization()
        creatingUsers_threadsForWebTests()
    elif selectingOpt == 2:
        mySQLPerformenceTestInitialization()
        creatingUsers_threadsForDBTests()
    elif selectingOpt == 3:
        remoteServerUsageTestInitialization()
        creatingUsers_threadsForRemoteServerTests()
    elif selectingOpt == 4:
        webTestInitialization()
        remoteServerUsageTestInitialization()
        creatingUsers_threadsForRemoteServerTests()
        while (threadsForRemoteServerTests[0].activeIndicator == 0):
            time.sleep(0.01)
        creatingUsers_threadsForWebTests()



startingTheProgramme()


# Wait for all threads to complete

for allThreads1 in threadsForWebTests:
    allThreads1.join()

for allThreads2 in threadsForRemoteServerTests:
    allThreads2.join()

for allThreads3 in threadsForMySQLTests:
    allThreads3.join()

print "Exiting the Thread array"
logging.info('Exiting the Thread array')
logging.info('Testing finished at ' + str(datetime.now()))
logging.info('-----------------------------------------------------------------------------------------')

