#!/usr/bin/python3

import sys
import getopt
import hashlib
import requests

def main(argv):

    output_file = sys.stdout
    passwords, output_file = _initProgram(argv)

    for password in passwords:
        theHash, prefix, suffix  = getHash(password)

        response = requests.get("https://api.pwnedpasswords.com/range/" + prefix)
        responseText = response.text

        suffixIndex = responseText.find(suffix)
        if suffixIndex > -1: #if the suffix is found ==> I have been PWNED
            recurrenceIndex = responseText.find(":", suffixIndex+1)
            eolIndex = responseText.find("\r\n", recurrenceIndex)
            output_file.write("The password [" + password + "] has been compromised " + responseText[recurrenceIndex+1:eolIndex] + " times\n")
        else:
            output_file.write ("Your password [" + password + "] has not yet been compromised.\n")

    print("=========DONE==========")
    output_file.close()


def printUsage():
    print("USAGE:")
    print("\thibp_password.py [OPTIONS] [password1, password2...]")
    print("\nOPTIONS")
    print("-h, -H, -help, -Help")
    print("\tPrint a usage message briefly summarizing these command-line options\n")
    print("-i, --ifile=")
    print("\tInput file name containing one password on each line\n")
    print("-o, --ofile=")
    print("\tOutout file to store the PWNED resuts. The default is STDOUT\n\n")


def _initProgram(argv):

    passwords = []
    output_file = sys.stdout

    #Setup from the command line.
    try:
        arguments, values = getopt.getopt(argv, 'hHi:o:', ['help', 'Help', 'ifile=', 'ofile=', ])
    except:
        printUsage()
        sys.exit(2)

    for argument, value in arguments:
        if argument in ("-h", "-H", "--help", "--Help"):
            printUsage()
            sys.exit(2)
        elif argument in ("-i", "--ifile"):
            try:
                with open(value, "r") as inputFile:
                    passwords.extend(inputFile.read().splitlines())
            except IOError as error:
                print("Unable to read file:", value)
                print(error)
                exit(2)
        elif argument in ("-o", "--ofile"):
            try:
                output_file = open(value, "w")
            except IOError as error:
                sys.stdout = original_stdout
                print ("Unable to open output file:", value)
                print (error)
                sys.exit(2)

    #Add any command line arguments as password array elements
    passwords.extend(values)
    return passwords, output_file


def getHash(string):
    hashObj = hashlib.sha1(string.encode())
    theHash =  hashObj.hexdigest().upper()

    #Prefix is used to send to the API
    prefix = theHash[0:5]

    #Suffix is used to find if the password has been compromised
    suffix = theHash[5:]

    return theHash, prefix, suffix


main(sys.argv[1:])
