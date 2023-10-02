#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Name: Gavin Fletcher
Date: 10/2/23
Version: 1.0
'''
#Import useful package(s)
import subprocess

def getMemoryInformation(): 
    memoryPrint = ""
    memoryInfo = subprocess.check_output(["free", "-g", "-h"]) # Show the memory (free) in gigabytes (-g), and human readability (-h)
    splitData = memoryInfo.decode().strip().split()
    memoryPrint += "Ram Information:\n"
    memoryPrint += "Total RAM:\t\t "+splitData[7]+"\n"
    memoryPrint += "Available RAM:\t\t "+splitData[11]+"\n"
    return memoryPrint

def find_Default_gateway():
    # Runs a command to immeidately get the line containing the default gateway
    result = subprocess.check_output("ip route | grep default", shell=True) 
    # If no gateway is set, terminal returns 1
    if (result == 1):
        print("No gateway found!")
        return None
    else:
        # Decodes the result to turn it into a string
        result = result.decode()
        result = result.strip().split(" ") # Remove special characters and split on spaces
        gateway = result[2] # Default Gateway is the 3rd item in the split string
        return gateway
def main():
    finalPrint = "" #This will be the printed message written to a file at the nedo f the program.
    user_input = None # Setting user_input so that the while loop can run
    subprocess.call("clear", shell=True)
    finalPrint += getMemoryInformation()
    print(finalPrint)
    subprocess.run(["echo", finalPrint], shell = True)


if __name__ == "__main__":
    main()