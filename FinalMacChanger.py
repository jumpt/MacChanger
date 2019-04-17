#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Execute using Python by looking up the path to the Python interpreter automatically via env


import subprocess
# Allows use of the subprocess module, the subprocess module allows you to spawn new processes.
# This means you can run system commands such as ls, ifconfig etc

import argparse
# Updated version of optparse. The argparse module allows you to parse user input and allows you to define
# what arguments you require.

import re


# Allows the use of regex commands


def get_arguments():
    # def means we are defining a function called get_arguments
    parser = argparse.ArgumentParser()
    # this creates an ArgumentParser object (parser), this will hold all the information necessary to parse the
    # command line into Python data types.
    parser.add_argument("-i", "--interface", dest="interface", help="interface to change MAC of")
    # Filling an ArgumentParser object (parser) with information about program arguments is done by making
    # calls to the add_argument() method. This defines the attributes to be added to the object.
    parser.add_argument("-m", "--mac", dest="newmac", help="new MAC address")
    # in addition to the above, dest is the name of the attribute to be added to the object returned by parse_args()
    args = parser.parse_args()
    # Convert argument strings to objects and assign them as attributes of the namespace. Return the populated
    # namespace. So now we get args.interface and args.newmac (I think this is the namespace)
    if not args.interface:
        # this detects if interface has not been entered
        parser.error("[-] Please enter an interface")
    # This is a method that prints the error message
    elif not args.newmac:
        # this detects if a MAC address has not been entered
        parser.error("[-] Please enter a MAC address")
    # A method (like an action) is something an object can do, so the object (parser) can do a method (error)
    return args


# This returns the namespace (args) with the interface and newmac attributes to the main program.


def change_mac(interface, newmac):
    # This defines the functions and the two parameters it requires to work.
    print("[+] Changing MAC address for " + interface + " to " + newmac)
    # print is a function
    subprocess.call(["ifconfig", interface, "down"])
    # shuts the interface down so the mac can be changed
    subprocess.call(["ifconfig", interface, "hw", "ether", newmac])
    # changes the MAC using the standard command
    subprocess.call(["ifconfig", interface, "up"])


# brings the interface back online


def get_current_mac(interface):
    # This defines the function and the argument you have to supply it with (interface)
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    # print(type(ifconfig_result))
    # used the above to find out variable type
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    # Was not working on Python3 until I put str in front of the ifconfig_result variable
    # this is because ifconfig-result was being stored as class 'bytes' not a string and you
    # cannot perform a regex on a non-string!!!

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    # regex can return multiple results and they are stored in a group, first result is stored in # (0),
    # the regex we used on the string only returns a single match.
    else:
        print('[-]could not read MAC address')


args = get_arguments()
# calls the defined function and gets back the namespace and values. Note this is the first part of the program
# that is actually 'run'

current_mac = get_current_mac(args.interface)
# call get_current_mac function using the args.interface argument

print("current mac = " + str(current_mac))
# str(current_mac) is used so if there's a problem and no value is stored in current_mac you'll just get a blank gap
# if not you'll get a type error


change_mac(args.interface, args.newmac)
# calls the function using the two arguments

current_mac = get_current_mac(args.interface)

if current_mac == args.newmac:
    # == means are these things equal, = on it's own means setting a variable
    print("[+] MAC address was successfully changed to " + str(current_mac))
else:
    print("[-] Something went wrong")
