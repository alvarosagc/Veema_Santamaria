# Imports
import os
import pandas
import shutil
import sys
import time
import warnings
from datetime import datetime

datetime.fromtimestamp(1485714600).strftime("%A, %B %d, %Y %I:%M:%S")

warnings.filterwarnings("ignore")

def syncfunc(srcpath = 'C:\\Users\\usuario\\Desktop\\pythoncode', destpath = 'C:\\Users\\usuario\\Desktop\\testfolder'):
    # Define Dataframes an lists
    dfsrc = pandas.DataFrame()
    dfdest = pandas.DataFrame()
    df_log = pandas.DataFrame()
    srclist = []
    srctime = []
    destlist = []
    desttime = [] 

    # Search for files in the directory
    srcfiles = os.listdir(srcpath)
    destfiles = os.listdir(destpath)

    # Make a dataframe for all the files in the dataframe with their time in the source folder
    for i in srcfiles:
        srclist.append(i)
        srctime.append(os.path.getmtime(srcpath + '\\' + i))
    dfsrc['file'] = srclist
    dfsrc['time'] = srctime

    # Make a dataframe for all the files in the dataframe with their time in the destination folder
    for i in destfiles:
        destlist.append(i)
        desttime.append(os.path.getmtime(destpath + '\\' + i))
    dfdest['file'] = destlist
    dfdest['time'] = desttime  

    # Get the difference between the source and destination folder for all files present in either folders
    df_create = dfsrc[~(dfsrc['file'].isin(dfdest['file']))].reset_index(drop=True)
    df_notindest = dfsrc[~(dfsrc['file'].isin(dfdest['file']) & dfsrc['time'].isin(dfdest['time']))].reset_index(drop=True)
    df_copy = df_notindest[~(df_notindest['file'].isin(df_create['file']))].reset_index(drop=True)
    df_delete = dfdest[~(dfdest['file'].isin(dfsrc['file']) & dfdest['time'].isin(dfsrc['time']))].reset_index(drop=True)

    # Copy files from src to dest, and delete files
    notindest = df_create['file'].tolist()
    for i in notindest:
        path = srcpath + '\\' + i
        shutil.copy2(path, destpath)

    notinsrc = df_delete['file'].tolist()
    for i in notinsrc:
        path = destpath + '\\' + i
        os.remove(path)

    notindest = df_copy['file'].tolist()
    for i in notindest:
        path = srcpath + '\\' + i
        shutil.copy2(path, destpath)

    # Create log file
    df_create['operation'] = 'Create'
    df_copy['operation'] = 'Copy'
    df_delete['operation'] = 'Delete'
    df_log = df_log.append(df_create)
    df_log = df_log.append(df_copy)
    df_log = df_log.append(df_delete)
    #df_log['time'] = datetime.fromtimestamp(df_log['time']).strftime("%A, %B %d, %Y %I:%M:%S")

    return df_log

print(sys.argv)
value = True
while(value):
    df_log = pandas.DataFrame()
    time.sleep(int(sys.argv[3]))
    df_log = syncfunc(sys.argv[1], sys.argv[2])
    logpath = str(sys.argv[4]) + '\\logfile.csv'
    df_log.to_csv(logpath, header=None, index=None, sep=',', mode='a')