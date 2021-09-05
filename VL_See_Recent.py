#! python3
# VL_SEE_RECENT

from __future__ import print_function
import argparse
import sys
import os.path, time
import socket
import datetime

_author_ = ['Copyright 2021 North Loop Consulting']
_copy_ = ['(C) 2021']
_description_ = ("---VL_See_Recent v1.0---"
                 " A tool to retrieve recent file activity from VLC configuration ini file."" \n "
                 " This iteration of the tool was designed solely for use with KAPE. "" \n"
                 " The Target - tkape and Module - mkape files needed to run this tool are available on the same Github page you used to download VL_See_Recent. " 
                 )
now = datetime.datetime.now()
parser = argparse.ArgumentParser(
    description=_description_,
    epilog="{}".format(
        ", ".join(_author_), _copy_))


#Add positional arguments
parser.add_argument("INPUT_FOLDER", help="Path to the input folder")
parser.add_argument("OUTPUT_FOLDER", help="Path to the output file")

# Optional Arguments
                    

#Parsing and using the arguments

args = parser.parse_args()

input_folder = args.INPUT_FOLDER
output_folder = args.OUTPUT_FOLDER


savePath = args.OUTPUT_FOLDER
completeName = os.path.join(savePath, "VL_See_Recent Report.txt")


#open a text output file

org_stdout = sys.stdout

with open(completeName, 'w') as report:
    sys.stdout = report

#Parse ini file 
def parse_INI():
    
    INI = input_folder + ("\\C\\Users\\")  #input folder = drive letter, then narrow to user folders
    
    
##    print("VL_See_Recent Report ")
##    print("Report Generated:  ", now)
##    print("Host:  " + socket.gethostname(), "\n")

    with open(completeName, 'a') as report:     #print report header to file
        sys.stdout = report
        print("VL_See_Recent Report ")
        print("Report Generated:  ", now)
        print("Host:  " + socket.gethostname(), "\n")
        sys.stdout = org_stdout

    for root, dirs, files in os.walk(INI, topdown=False):  #walk user folders to find the .ini
        for INI in files:
            if INI == "vlc-qt-interface.ini":
                
                targetuser = (os.path.join(root, INI))
                #print(targetuser)
                mtime = os.path.getmtime(targetuser) #Gets last mod time for ini file
                #print("File Last Modified: %s" % datetime.datetime.fromtimestamp(mtime), '\n')
    
                with open(completeName, 'a') as report:   #print user/ini to file
                    sys.stdout = report
                    print(targetuser)
                    print("File Last Modified: %s" % datetime.datetime.fromtimestamp(mtime), '\n')
                    sys.stdout = org_stdout

                file = open(targetuser, "r")   #locate recent files played in VLC
                lines = file.readlines()
                file.close()
                for line in lines:
                    line = line.strip()
                    if line.startswith('list='):
                        line = line.strip('list=')
                        line = line.split(', ')
                        for fpath in line:
                            #print(fpath)
                            with open(completeName, 'a') as report:
                                sys.stdout = report
                                print(fpath)
                                sys.stdout = org_stdout
                            
                #print("\n")
                with open(completeName, 'a') as report:
                    sys.stdout = report
                    print("\n")
                    sys.stdout = org_stdout
               

parse_INI()
report.close()
