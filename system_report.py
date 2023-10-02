#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Name: Gavin Fletcher
Date: 10/2/23
Version: 1.1
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
    return subprocess.check_output(command, shell=True).strip().decode()


def getNetworkInformation():
    networkPrint = ""
    ipAddr = runCommand('nmcli device show ens192 | grep "IP4.ADDRESS" | awk \'$1 {print $2}\'')
    gateway = runCommand('nmcli device show ens192 | grep "IP4.GATEWAY" | awk \'$1 {print $2}\'')
    DNS1 = runCommand('nmcli device show ens192 | grep "IP4.DNS\[1\]" | awk \'$1 {print $2}\'')
    DNS2 = runCommand('nmcli device show ens192 | grep "IP4.DNS\[2\]" | awk \'$1 {print $2}\'')
    ipOnly = ipAddr.split("/")[0]
    networkPrint += "Network Information:\n"
    networkPrint += "Ip Address\t\t "+ ipOnly+"\n"
    networkPrint += "Gateway: \t\t "+gateway+"\n"
    networkPrint += "Network Mask: \t\t "+cidr_to_netmask(ipAddr)+"\n"
    networkPrint += "DNS1: \t\t\t "+DNS1+"\n"
    networkPrint += "DNS2: \t\t\t "+DNS2+"\n\n"
    return networkPrint

def getProcessorInformation():
    cpuPrint = "Processor Infomation:\n"
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
    return devicePrint


def getMemoryInformation(): 
    memoryPrint = ""
    totalRam = runCommand("free -h | grep 'Mem' | awk '$1 {print $2}'")# Show the memory (free) in gigabytes (-g), and human readability (-h)
    availableRam = runCommand("free -h | grep 'Mem' | awk '$1 {print $6}'")
    memoryPrint += "Memory Information:\n"
    memoryPrint += "Total RAM:\t\t "+totalRam+"\n"
    memoryPrint += "Available RAM:\t\t "+availableRam+"\n"
    return memoryPrint


def main():
    finalPrint = "" #This will be the printed message written to a file at the nedo f the program.
    user_input = None # Setting user_input so that the while loop can run
    subprocess.call("clear", shell=True)
    finalPrint += getDeviceInformation()
    finalPrint += getNetworkInformation()
    finalPrint += getProcessorInformation()
    finalPrint += getMemoryInformation()
    print(finalPrint)



if __name__ == "__main__":
    main()