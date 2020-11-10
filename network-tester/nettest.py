import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import datetime
import time
import os
import sys
from networkInterfaces import NetworkInterfaces

TEST_HOST = "google.com"
DEFAULT_GATEWAY = "192.168.128.1"
NETWORK_INTERFACE = "eth0"
INTERVAL = 1

PING_ERROR_MESSAGE = "ERROR:Can't ping Test host (%s)" % TEST_HOST
ADAPTER_ERROR_MESSAGE = "ERROR:Ethernet Network Adapter disconnected or inexistent! (%s)" % NETWORK_INTERFACE
GATEWAY_ERROR_MESSAGE = "ERROR:Can't ping the Default gateway (%s)!" % DEFAULT_GATEWAY

errors = 0
logFile = None
logFileName = ""

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0

def doNetworkTests():
    global PING_ERROR_MESSAGE
    global GATEWAY_ERROR_MESSAGE
    global ADAPTER_ERROR_MESSAGE

    global TEST_HOST
    global DEFAULT_GATEWAY
    global NETWORK_INTERFACE

    okay = True
    errorMsg = ""
    
    if not isInterfaceUp(NETWORK_INTERFACE):
        okay = False
        errorMsg = ADAPTER_ERROR_MESSAGE
        return okay, errorMsg

    if not ping(DEFAULT_GATEWAY):
        okay = False
        errorMsg = GATEWAY_ERROR_MESSAGE
        return okay, errorMsg

    if not ping(TEST_HOST):
        okay = False
        errorMsg = PING_ERROR_MESSAGE
        return okay, errorMsg

    return okay, errorMsg

def isInterfaceUp(interface):
    return NetworkInterfaces.isInterfaceUp(interface)

def getTimestampString():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H-%M-%S")

def createNewLogFile():
    global logFile
    global logFileName

    logFileName = "%s.txt" % getTimestampString()
    logFile = open(logFileName, 'w+')
    return logFile

def openLogFile():
    global logFile
    global logFileName

    logFile = open(logFileName, 'a+')
    return logFile

def writeToLogFile(file, errorMsg):
    global errors
    file.write("%s: %s at Timestamp:%s" % (errors, errorMsg, getTimestampString()))
    file.write("\n")
    file.close()
    return

def hasPassedOneHour(startTime):
    try:
        if startTime == '':
            return True
        sTime = datetime.datetime.strptime(startTime, '%Y-%m-%d %H-%M-%S').timestamp()
        elapsed = time.time() - sTime
        if elapsed >= 59:
            return True
        else:
            return False
    except:
        return False


def logError(errorMsg):
    global errors
    global logFileName
    startTime = logFileName.replace(".txt",'')

    if hasPassedOneHour(startTime):
        logFile = createNewLogFile()
        writeToLogFile(logFile, errorMsg)
    else:
        logFile = openLogFile()
        writeToLogFile(logFile, errorMsg)

def printHeader():
    print("This program tests internet and network connection in the bellow order")
    print("Network Adapter >>> Default Gateway >>> Test Host (A server on LAN/WAN)")
    print("The program will execute the following tests:")
    print("Network Adapter | is UP (Cable Connected or enable on the OS) or not")
    print("Default Gateway | ping")
    print("Test Host  | ping")

def printUsage():
    print("")
    print("USAGE:")
    print("python nettest.py <Test host> <Default gateway> <Network interface> <Interval>")

def handleCommandLineArguments():
    global TEST_HOST
    global DEFAULT_GATEWAY
    global NETWORK_INTERFACE
    global INTERVAL

    if len(sys.argv) == 1:
        print("running tests with default parameters!")
        print("Test Host = %s" % TEST_HOST)
        print("Default Gateway = %s" % DEFAULT_GATEWAY)
        print("Network Interface = %s" % NETWORK_INTERFACE)
        print("Interval = %s" % NETWORK_INTERFACE)
        print("to set the above parameters use the command like bellow example!")
        printUsage()

    if len(sys.argv) == 5:
        print("starting...")
        TEST_HOST = sys.argv[1]
        DEFAULT_GATEWAY = sys.argv[2]
        NETWORK_INTERFACE = sys.argv[3]
        INTERVAL = sys.argv[4]

    if len(sys.argv) == 2 or len(sys.argv) == 3 or len(sys.argv) > 5:
        printHeader()
        printUsage()
        exit()


handleCommandLineArguments()

while(True):
    okay, errorMsg = doNetworkTests()
    if not okay:
        logError(errorMsg)
        errors = errors + 1
    time.sleep(int(INTERVAL))