#!/usr/bin/env python3

from network import datatypes, datahandler
import socket
import time

# TODO: ip and port will be argument
IP = ""
PORT = 49000


def main():
    print("Home cockpit connector on Raspberry Pi")
    dh = datahandler.DataHandler()
    com1Stby = datatypes.DataReference(0, 0)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((IP, PORT))

    while True:
        dh.Data, addr = sock.recvfrom(1024)

        com1Stby = dh.Decode(com1Stby)

        print(com1Stby.Value, ", name:", com1Stby.Name)

        #time.sleep(1)



if __name__ == "__main__":
    main()
