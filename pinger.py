import datetime
import getopt
import platform
import subprocess
import sys
from time import sleep


# Returns true if host responds to ping request
def ping(timeout=1000, host="8.8.8.8"):
    info = subprocess.STARTUPINFO()
    info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    info.wShowWindow = subprocess.SW_HIDE
    if platform.system().lower() == "windows":
        numberOfPingParam = '-n'
    else:
        numberOfPingParam = '-c'
        timeout /= 1000.0
    output = subprocess.Popen(['ping', numberOfPingParam, '1', '-w', str(timeout), str(host)], stdout=subprocess.PIPE,
                              startupinfo=info).communicate()[0]
    return "Reply from" in output.decode('utf-8')



def writeLogs(content, filename='logs.txt'):
    if not isinstance(content, str):
        content = str(content)
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
    while 1:
        if ping(float(interval) * 1000, host) and connectionFlag:
            writeLogs("UP\n", logLocation)
        elif not ping(float(interval) * 1000, host) and connectionFlag:
            connectionFlag = False
            differenceTemp = abs(stateChange - datetime.datetime.now())
            difference = divmod(differenceTemp.days * 86400 + differenceTemp.seconds, 60)
            writeLogs("Was UP for " + str(difference[0]) + " minutes and " + str(difference[1]) + " seconds.\n",
                      logLocation)
            stateChange = datetime.datetime.now()
        elif not ping(float(interval) * 1000, host) and not connectionFlag:
            writeLogs("DOWN\n", logLocation)
        elif ping(float(interval) * 1000, host) and not connectionFlag:
            connectionFlag = True
            differenceTemp = abs(stateChange - datetime.datetime.now())
            difference = divmod(differenceTemp.days * 86400 + differenceTemp.seconds, 60)
            writeLogs("Was DOWN for " + str(difference[0]) + " minutes and " + str(difference[1]) + " seconds.\n",
                      logLocation)
            stateChange = datetime.datetime.now()
        sleep(float(interval))


if __name__ == "__main__":
    main(sys.argv[1:])
