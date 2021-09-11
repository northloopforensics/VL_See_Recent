#! python3
# VL_SEE_RECENT
# Copyright 2021 North Loop Consulting, LLC

from __future__ import print_function
import argparse
import sys
import os.path, time
import socket
from datetime import datetime, timezone
import glob2

_author_ = ['Copyright 2021 North Loop Consulting']
_copy_ = ['(C) 2021']
_description_ = ("---VL_See_Recent v1.0---\n"
                 " A tool to retrieve recent file activity from VLC configuration ini file."" \n "
                 )
now = datetime.now()
now = now.strftime('%Y-%m-%d %H:%m:%d')
parser = argparse.ArgumentParser(
    description=_description_,
    epilog="{}".format(
        ", ".join(_author_), _copy_))

#Add positional arguments
parser.add_argument("INPUT_VOLUME", help="Input volume letter - ex. 'C:' or Absolute path - ex. 'E:\\Evidence\\KapeCollection\\C'")
parser.add_argument("OUTPUT_FOLDER", help="Path to store report text file")

# Optional Arguments
#Parsing and using the arguments
args = parser.parse_args()

input_volume = args.INPUT_VOLUME
output_folder = args.OUTPUT_FOLDER

savePath = args.OUTPUT_FOLDER
rptfile = (f"VL_See_Recent Report-{datetime.now():%Y-%m-%d %H-%m-%d}.txt")
completeName = os.path.join(savePath, rptfile)

org_stdout = sys.stdout

with open(completeName, 'w') as report:
    sys.stdout = report

#Parse ini file 
def parse_INI():
    
    with open(completeName, 'a') as report:     #print report header to file
        sys.stdout = report
        print(""" _    ____        _____                ____                       __ 
| |  / / /       / ___/___  ___       / __ \___  ________  ____  / /_
| | / / /        \__ \/ _ \/ _ \     / /_/ / _ \/ ___/ _ \/ __ \/ __/
| |/ / /___     ___/ /  __/  __/    / _, _/  __/ /__/  __/ / / / /_  
|___/_____/____/____/\___/\___/____/_/ |_|\___/\___/\___/_/ /_/\__/  
         /_____/             /_____/                                 """)
        print("\nVL_See_Recent Report")
        print("Target Volume/Directory: ", input_volume)
        print("Report Generated:  ", now, "Local Time")
        print("Report Generated with User Acct: ", os.getlogin())
        print("Report Generated on Host:  " + socket.gethostname(), "\n")
        sys.stdout = org_stdout

    if len(input_volume) == 2:
        INI2 = input_volume + ("\\Users\\*\\AppData\\Roaming\\vlc\\vlc-qt-interface.ini")    #Finds the ini file for any/all users using volume letter
    else:
        INI2 = input_volume + ("\\**\\Users\\*\\AppData\\Roaming\\vlc\\vlc-qt-interface.ini")

    for targetuser in glob2.glob(INI2):
        print(targetuser)
        mtime = os.path.getmtime(targetuser) #Gets last mod time for ini file
                #print("File Last Modified: %s" % datetime.datetime.fromtimestamp(mtime), '\n')
    
        modtime = datetime.fromtimestamp(mtime)
        modtime = modtime.strftime('%Y-%m-%d %H:%m:%d')

        with open(completeName, 'a') as report:   #print user/ini to file
            sys.stdout = report
            print('\t******************************************************************\n')
            print("\tVLC INI File Path: ")
            print('\t'+targetuser)
            print("\n\tvlc-qt-interface.ini Last Modified: %s" % modtime, 'Local Time (May indicate last use of VLC to view files.) \n')
            print("\tRECENT FILES:")
            sys.stdout = org_stdout

        file = open(targetuser, "r")   #locate recent files played in VLC
        lines = file.readlines()
        file.close()
        for line in lines:
            line = line.strip()
            if line.startswith('list='):
                line = line.strip('list=')
                line = line.split(', ')             #seperates the long line of files to ind file paths
                
                for fpath in line:
                    fpath = fpath[8:] #strips extraneous header for each filepath
                    with open(completeName, 'a') as report:
                        sys.stdout = report
                        
                        print('\t---',fpath)
                        sys.stdout = org_stdout

        with open(completeName, 'a') as report:
            sys.stdout = report
            print("\n")
            print('\t******************************************************************')
            sys.stdout = org_stdout

parse_INI()
report.close()
