import os
import csv
from config import LOGSYSTEM_PATH

def writeLog(row1, row2, row3):
    '''write or create csv file'''

    with open(LOGSYSTEM_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([row1,
                         "=\"" + row2 + "\"", 
                         "=\"" + row3 + "\""
                         ])

def logging():
    '''logging system | create'''

    if not os.path.isfile(LOGSYSTEM_PATH):
        print("creating new csv file..")
        writeLog("Name", "Spieldauer", "Schlaege insgesamt")
    else:
        print("logfile already exists")