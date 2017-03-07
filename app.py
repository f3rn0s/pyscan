#!/usr/bin/env python3
import socket
import subprocess
import select
import sys
from datetime import datetime


"""

TODO:
    Implement a classified or functionified model
    Identify Services
    Pipe into easy to read output

"""


subprocess.call('clear', shell=True)

remoteServer = '127.0.0.1'
# remoteServer = input("Enter a remote Host to scan: ")
remoteServerIP = socket.gethostbyname(remoteServer)

t1 = datetime.now()

p1 = 0
p2 = 65535

openPorts = {}

try:
    for port in range(p1, p2):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIP, port))
        if result == 0:
            print("Port {}:  Open".format(port))
            ready = select.select([sock], [], [], 2)
            if ready[0]:
                openPorts[port] = sock.recv(1024).decode('utf-8').rstrip()
            else:
                openPorts[port] = 'unknown'
        sock.close()

except KeyboardInterrupt:
    sys.exit("ByeBye\n")
except socket.gaierror:
    sys.exit("Hostname could not be resolved")
except socket.error:
    sys.exit("Couldn't connect\n")

t2 = datetime.now()

total = t2 - t1

print("Initial scan took: " + str(total))

sortedports = sorted(openPorts.items(), key=lambda x: x[0])

print("\nResults:\n")

for result in sortedports:
    print("Port {}: ".format(result[0]) + result[1])

# print(sortedports[1][0])
