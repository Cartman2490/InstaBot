#testing.py

#login = 'westcoastautos'
#password = '1qazxsw2'

from opensourcebotsfuckyeah import *


def input_master(inputFileName):
    if '.txt' not in inputFileName:
        inputFileName += '.txt'
    return inputFileName
    
    
inputFileName = input("Enter the name of the .txt file containing hashtags to search for: ")
inputFileName = input_master(inputFileName)
inputTagList = hashtags_list_form(inputFileName)

inputFileBlackList = input("Enter the name of the .txt file containing hashtags to avoid: ")
inputFileBlackList = input_master(inputFileName)
inputTagBlackList = hashtags_list_form(inputFileBlackList)


