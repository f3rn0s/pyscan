#!/usr/bin/env python3
import socket
import subprocess
import select
import sys
from datetime import datetime as timeGet


"""

TODO:
    Identify Services
    Pipe into easy to read output

"""

serviceGuess = {
                7  : 'Echo',
                9  : 'Wake-On-Lan',
                17 : 'Quote of the Day',
                18 : 'Message of the Day',
                20 : 'FTP',
                21 : 'FTP',
                22 : 'SSH',
                23 : 'Telnet',
                25 : 'SMTP',
                53 : 'DNS',
                69 : 'TFTP',
                79 : 'Finger',
                80 : 'HTTP',
                111: 'RPC bind',
                115: 'SFTP',
                161: 'SNMP',
                170: 'Print Server',
                194: 'IRC',
                443: 'HTTPS',
                465: 'SMTPS',
                531: 'AOL',
                631: 'Cups',
                666: 'Doom!!!',
                843: 'Dropbox',
                3306: 'mySQL',
                4243: 'Docker',
                5432:'PostGresql',
                5433:'PostGresql'
                }

def scanner(host, p1, p2):
    openPorts = {}
    t1 = timeGet.now()
    try:
        for port in range(p1, p2):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((host, port))
            if result == 0:
                # print("Port {}:  Open".format(port))
                ready = select.select([sock], [], [], 2)
                if ready[0]:
                    openPorts[port] = sock.recv(1024).decode('utf-8').rstrip()
                elif port in serviceGuess:
                    openPorts[port] = serviceGuess[port] + "?"
                else:
                    openPorts[port] = "Unknown"
            sock.close()
        t2 = timeGet.now()
        return openPorts, t2 - t1
    except KeyboardInterrupt:
        sys.exit("ByeBye\n")
    except socket.gaierror:
        sys.exit("Hostname could not be resolved")
    except socket.error:
        sys.exit("Couldn't connect\n")

def scan(host='127.0.0.1', p1=0, p2=10001):
    retList, retTime = scanner(host, p1, p2)
    sortList = sorted(retList.items(), key=lambda x: x[0])
    return sortList, retTime

def clear():
    subprocess.call('clear', shell=True)

def getIP(hostname):
    return socket.gethostbyname(hostname)

clear()

# scanIP = getIP(input("Enter a remote Host to scan: "))

results, totalTime = scan()


print("\nResults:\n")

print("Initial scan took: " + str(totalTime) + "\n")

for result in results:
    print("Port {}: ".format(
                            result[0])
             + " " * ( 5 - len(str(result[0]))) +
                            result[1])

# print(sortedports[1][0])
