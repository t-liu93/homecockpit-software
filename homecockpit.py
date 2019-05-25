#!/usr/bin/env python3

import argparse
import collections
from hardware import hardwarehandler
from network import datahandler
import queue


def main(clientPort, hostPort):
    print("Home cockpit connector on Raspberry Pi")
    DataHandlerQueue = collections.namedtuple('datahandlerqueue', 'networktohardware hardwaretonetwork')
    dataHandlerQueue = DataHandlerQueue(queue.Queue(), queue.Queue())
    dataHandlerThread = datahandler.DataHandler(dataHandlerQueue, "socket", clientPort, hostPort)
    radioPanelThread = hardwarehandler.RadioPanel(dataHandlerQueue, "radio")
    
    dataHandlerThread.start()
    radioPanelThread.start()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("clientPort",
        help="The port you set in X-plane for sending data reference.",
        type=int)
    parser.add_argument("hostPort",
        help="The port which X-plane is listening to.",
        type=int)

    args = parser.parse_args()
    main(args.clientPort, args.hostPort)