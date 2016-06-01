import os
import platform
import sys
import getopt
import datetime
from time import sleep


# Returns true if host responds to ping request
def ping(host="8.8.8.8"):
    if platform.system().lower() == "windows":
        strPingParameters = "-n 1"
    else:
        strPingParameters = "-c 1"
    return os.system("ping " + strPingParameters + " " + host) == 0


def writeLogs(content, filename='logs.txt'):
    # if isinstance(content, str):
    #     pass
    # else:
    #     content = str(content)
    file = open(filename, "a+")
    file.write(content)
    file.close()


def main(argv):
    host = ""
    logLocation = ""
    interval = 20
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
        if ping(host):
            writeLogs("\n" + str(datetime.datetime.now()) + " " + " UP", logLocation)
        else:
            writeLogs("\n" + str(datetime.datetime.now()) + " " + " DOWN", logLocation)
        sleep(int(interval))


if __name__ == "__main__":
    main(sys.argv[1:])
