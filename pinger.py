import os
import platform
import sys
import getopt
import datetime
from time import sleep


# Returns true if host responds to ping request
def ping(timeout=1000, host="8.8.8.8"):
    if platform.system().lower() == "windows":
        #timeout in miliseconds
        strPingParameters = "-n 1" + " -w " + str(timeout)
    else:
        #timeout in seconds
        strPingParameters = "-c 1" + " -W " + str(timeout/1000)
    # print("ping " + strPingParameters + " " + host)
    return os.system("ping " + strPingParameters + " " + host) == 0


def writeLogs(content, filename='logs.txt'):
    # if isinstance(content, str):
    #     pass
    # else:
    #     content = str(content)
    file = open(filename, "a+")
    file.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + " " + content)
    file.close()


def main(argv):
    host = ""
    logLocation = ""
    interval = 20
    connectionFlag = ping()
    stateChange = datetime.datetime.now()
    try:
        opts, args = getopt.getopt(argv, "hi:o", ["ipaddress=", "logs=", "interval="])
    except getopt.GetoptError:
        print("pinger.py -ip <hostIP> -l <logLocation> -i <interval>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("pinger.py -ip <hostIP> -l <logLocation> -i <interval>")
            sys.exit()
        elif opt in ("-ip", "--ipaddress"):
            host = arg
        elif opt in ("-l", "--logs"):
            logLocation = arg
        elif opt in ("-i", "--interval"):
            interval = arg
    # print(host)
    # print(logLocation)
    # print(interval)
    while 1:
        if ping(int(interval)*1000, host) and connectionFlag:
            writeLogs("UP\n", logLocation)
        elif not ping(int(interval)*1000, host) and connectionFlag:
            connectionFlag = False
            differenceTemp = abs(stateChange - datetime.datetime.now())
            difference = divmod(differenceTemp.days * 86400 + differenceTemp.seconds, 60)
            writeLogs("Was UP for " + str(difference[0]) + " minutes and " + str(difference[1]) + " seconds.\n",
                      logLocation)
            stateChange = datetime.datetime.now()
        elif not ping(int(interval)*1000, host) and not connectionFlag:
            writeLogs("DOWN\n", logLocation)
        elif ping(int(interval)*1000, host) and not connectionFlag:
            connectionFlag = True
            differenceTemp = abs(stateChange - datetime.datetime.now())
            difference = divmod(differenceTemp.days * 86400 + differenceTemp.seconds, 60)
            writeLogs("Was DOWN for " + str(difference[0]) + " minutes and " + str(difference[1]) + " seconds.\n",
                      logLocation)
            stateChange = datetime.datetime.now()
        sleep(int(interval))


if __name__ == "__main__":
    main(sys.argv[1:])
