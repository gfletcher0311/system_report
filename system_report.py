#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Name: Gavin Fletcher
Date: 10/2/23
Version: 1.2
'''
#Import useful package(s)
import subprocess
import socket 
import struct

def cidr_to_netmask(cidr):# Code written by Trenton Mckinney stackoverflow.com/questions/33750233/convert-cidr-to-subnet-mask-in-python
    network, netbits = cidr.split("/")
    hostbits = 32- int(netbits)
    netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << hostbits)))
    return netmask

def runCommand(command):
    return subprocess.check_output(command, shell=True).strip().decode() # Function used to make running commands simple


def getNetworkInformation():
    networkPrint = "Network Information:\n"
    ipAddr = runCommand('nmcli device show ens192 | grep "IP4.ADDRESS" | awk \'$1 {print $2}\'') # Retruns the entire CIDR IP address
    gateway = runCommand('nmcli device show ens192 | grep "IP4.GATEWAY" | awk \'$1 {print $2}\'') # Retruns the gateway
    DNS1 = runCommand('nmcli device show ens192 | grep "IP4.DNS\[1\]" | awk \'$1 {print $2}\'') # Returns DNS1
    DNS2 = runCommand('nmcli device show ens192 | grep "IP4.DNS\[2\]" | awk \'$1 {print $2}\'') # Returns DNS 2
    ipOnly = ipAddr.split("/")[0] # Splits on the CIDR so we only have the IP and not netmask
    networkPrint += "Ip Address\t\t "+ ipOnly+"\n" # Adds the IP address to network print
    networkPrint += "Gateway: \t\t "+gateway+"\n"
    networkPrint += "Network Mask: \t\t "+cidr_to_netmask(ipAddr)+"\n"
    networkPrint += "DNS1: \t\t\t "+DNS1+"\n"
    networkPrint += "DNS2: \t\t\t "+DNS2+"\n\n"
    return networkPrint


def getOSInformation():
    osPrint = "OS Information:\n"
    #Comamnd explanation:
    # Read the file /ect/os-release and look for "Name", take the first entry, and split on "=", then replace the quotation amrks with air 
    osPrint += "Operating System: \t "+runCommand("cat /etc/os-release | grep \"NAME\" | head -1 | awk -F \"=\" \'$1 {print $2}\' | sed -e \'s/\"//g'")+"\n"
    osPrint += "Operating Version: \t "+runCommand("cat /etc/os-release | grep \"VERSION_ID\" | awk -F \"=\" \'$1 {print $2}\' | sed -e \'s/\"//g'")+"\n"
    osPrint += "Kernal Version: \t "+runCommand("uname -r")+"\n\n"
    return osPrint

def getStorageInformation():
    storagePrint = "Storage Information:\n"
    #Command: get storage informatiuo nand make it human readable
    # Look for root and print the 2nd column
    storagePrint += "Hard Drive capacity: \t "+runCommand("df -h | grep \"root\" | awk '$1 {print $2}'")+"\n"
    storagePrint += "Available Space: \t "+runCommand("df -h | grep \"root\" | awk '$1 {print $4}'")+"\n\n"
    return storagePrint

def getProcessorInformation():
    cpuPrint = "Processor Infomation:\n"
    # command: Open /proc/cpuinfo and grep for "model name", take the first entry, and split on ":", printing second column
    cpuModel = runCommand("cat /proc/cpuinfo | grep \"model name\" | head -1 | awk -F \":\" \'$1 {print $2}\'") 
    cpuPrint += "CPU Model:\t\t "+cpuModel+"\n"
    cpuPrint += "Number of processors: \t "+runCommand("nproc")+"\n"
    cpuPrint += "Number of Cores: \t "+str(int(runCommand("nproc"))/2)+"\n\n"
    return cpuPrint

def getDeviceInformation():
    devicePrint = ""
    hostname = runCommand("hostname")
    devicePrint += "Device Information:\n"
    devicePrint += "Hostname:\t\t "+hostname+"\n"
    devicePrint += "Domain:\t\t\t "+runCommand("domainname")+"\n\n"
    return hostname, devicePrint


def getMemoryInformation(): 
    memoryPrint = ""
    totalRam = runCommand("free -h | grep 'Mem' | awk '$1 {print $2}'")# Show the memory (free) and human readability (-h), then print the 2nd column
    availableRam = runCommand("free -h | grep 'Mem' | awk '$1 {print $6}'")
    memoryPrint += "Memory Information:\n"
    memoryPrint += "Total RAM:\t\t "+totalRam+"\n"
    memoryPrint += "Available RAM:\t\t "+availableRam+"\n"
    return memoryPrint


def main():
    finalPrint = "" #This will be the printed message written to a file at the nedo f the program.
    user_input = None # Setting user_input so that the while loop can run
    subprocess.call("clear", shell=True) # Clears terminal


    finalPrint += runCommand("date")+"\n\n" # Gets the current date and adds it the final print

    hostname, deviceInfo = getDeviceInformation() # Returns the hostname (for naming the file) and device information
    finalPrint += deviceInfo # adds the device information to the final print
    finalPrint += getNetworkInformation() # adds network info to print
    finalPrint += getOSInformation() 
    finalPrint += getStorageInformation() 
    finalPrint += getProcessorInformation() 
    finalPrint += getMemoryInformation() 
    print(finalPrint) # prints final message to the terminal
    subprocess.check_output(f"echo \"{finalPrint}\" > {hostname}_system_report.log", shell=True) # Uses echo to print the final result to a file



if __name__ == "__main__":
    main()