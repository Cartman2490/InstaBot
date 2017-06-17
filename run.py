#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import random

sys.path.append(os.path.join(sys.path[0], 'src'))

from check_status import check_status
from feed_scanner import feed_scanner
from follow_protocol import follow_protocol
from instabot import InstaBot
from unfollow_protocol import unfollow_protocol





def main():
    #login = ''
    #password = ''    
    settings = accept_command_line_arguments()
    
    login = settings[0]
    password = settings[1]   
    whitelist = settings[2]
    blacklist = settings[3]    
    inputTagList = whitelist
    inputTagBlackList = blacklist
    followSwitch = settings[4]
    if followSwitch == 'y':
        print("You have selected to follow/unfollow users")
        bot = create_Bot_with_settings(login, password, inputTagList, inputTagBlackList, 285 )
        loop(bot)
#    print(followSwitch)
    bot = create_Bot_with_settings(login, password, inputTagList, inputTagBlackList, 0)
    loop(bot)

    
# Special handling for when the user starts the program
# - It is capable of taking command line arguments upon execution for convenient
# - shortcut making abilities (like on the desktop)
def accept_command_line_arguments():
    commandLineArguments = []    
    for i in sys.argv:
        commandLineArguments.append(i)
    if len(commandLineArguments) == 3:
        commandLineArguments = commandLineArguments[1:]
        type = interpret(commandLineArguments)
        if type == 'account info':
            (username, password) = (commandLineArguments[0], commandLineArguments[1])
            (inputTagList, inputTagBlackList) = grab_tag_files()
            followSwitch = follow_switch()            
        else:
            (username, password) = grab_account_info()
            a = hashtags_list_form(txt_appender(commandLineArguments[0]))
            b = hashtags_list_form(txt_appender(commandLineArguments[1]))
            (inputTagList, inputTagBlackList) = (a, b)
            followSwitch = follow_switch()           
    elif len(commandLineArguments) in [0, 1, 2, 4]:
        print("Optional Format: run.py <Username> <Password> <inputTagList.txt> <inputTagBlackList.txt> <y/n>")
        print()

        (username, password) = grab_account_info()
        (inputTagList, inputTagBlackList) = grab_tag_files()
    if len(commandLineArguments) == 6:
        username = commandLineArguments[1]
        password = commandLineArguments[2]
        inputTagList = hashtags_list_form(txt_appender(commandLineArguments[3]))
        inputTagBlackList = hashtags_list_form(txt_appender(commandLineArguments[4]))
        followSwitch = commandLineArguments[5]
    if len(commandLineArguments) == 5:

        username = commandLineArguments[1]
        password = commandLineArguments[2]
        inputTagList = hashtags_list_form(txt_appender(commandLineArguments[3]))
        inputTagBlackList = hashtags_list_form(txt_appender(commandLineArguments[4]))
        followSwitch = follow_switch()
        
    editedCommandLineArguments = []
    editedCommandLineArguments.append(username)
    editedCommandLineArguments.append(password)
    editedCommandLineArguments.append(inputTagList)
    editedCommandLineArguments.append(inputTagBlackList)
    editedCommandLineArguments.append(followSwitch)
    return editedCommandLineArguments

# returns a character 'y' or 'n'
def follow_switch():
    inputString = "Would you like to enable follow/unfollow? (y/n)"
    inputFileName = input_master2(inputString)
    return inputFileName
    
def grab_account_info():
    print("Enter your username below, then hit ENTER")
    username = input("Type Username Here: ")
    username.strip('@')
    print("Enter your password below, then hit ENTER")
    password = input("Type Password Here: ")
    return (username, password)
 
 
# Interprets provided user input from the command line at execution as either
# - Text Files, in the case that the user wants to choose his/her user and password later
# - Strings, in the case that the user wants to choose his/her whitelist and blacklist later
def interpret(commandLineArguments):
    type = 'tag filename'
    errors = 0
    for argument in commandLineArguments:
        argument = txt_appender(argument)

        if open_error(argument, 'no') == 'Error':
            errors += 1
    if errors == 2:
        type = 'account info'
    return type  

def grab_tag_files():
    inputString = "Enter the name of the .txt file containing hashtags to search for: "
    inputFileName = input_master(inputString)
    inputTagList = hashtags_list_form(inputFileName)
    inputString2 = "Enter the name of the .txt file containing hashtags to avoid: "
    inputFileName2 = input_master(inputString2)
    inputTagBlackList = hashtags_list_form(inputFileName2)
    return (inputTagList, inputTagBlackList)

# Accepts inputFileName from accept_command_line_arguments(), and returns
# - an array list of the hashtags in the input file
def hashtags_list_form(inputFileName):
    inFile = open(inputFileName, 'r')
    lineList = []
    lineNumber = 0
    for line in inFile:
        if '\n' in line:
            line = line.strip('\n')

        lineList.append(line)
        lineNumber += 1

    return lineList    
    
# Accepts an input string, prompts the user with that input string if no provided input already, 
# - then performs necessary cleaning and returns keeps asking until it can open the file
def input_master(inputString, userInput=0):
    if userInput == 0:
        userInput = input(inputString)
    userInput = txt_appender(userInput)
    while open_error(userInput) == 'Error':
        userInput = input_master(inputString)
    return userInput    
    
def input_master2(inputString, userInput=0):
    if userInput == 0:
        userInput = input(inputString)
    userInput = userInput.lower()
    while userInput not in ['n', 'y']:
        userInput = input_master(inputString)
    return userInput    

def txt_appender(string):
    if '.txt' not in string:
        string += '.txt'
    return string        

# Attempts to open a file!
# - input_master uses it to check if it should ask for a better input :) 
def open_error(inputFileName, printErrorMessage='yes'):    
    try:
        open(inputFileName, 'r')
        return 'Success'
    except:
        if printErrorMessage == 'yes':
            print("\n" + "{!r}: File does not exist".format(inputFileName))
            print()
        return 'Error'

def create_Bot_with_settings(login, password, inputTagList, inputTagBlackList, bothFollowRates=0):
    bot = InstaBot(
        login = str(login),
        password = str(password),
        like_per_day=random.randint(750, 900),
        comments_per_day=random.randint(4, 7),
        tag_list = inputTagList,
        tag_blacklist= inputTagBlackList,
        user_blacklist={},
        max_like_for_one_tag=random.randint(45,55),
        follow_per_day=bothFollowRates,
        follow_time=1 * 60,
        unfollow_per_day=bothFollowRates,
        unfollow_break_min=15,
        unfollow_break_max=30,
        log_mod=0,
        proxy='',
    # List of list of words, each of which will be used to generate comment
    # For example: "This shot feels wow!"

#        comment_list=[["this", "the", "your"],
#                      ["photo", "picture", "pic", "shot", "snapshot"],
#                      ["is", "looks", "feels", "is really"],
#                      ["great", "super", "good", "very good", "good", "wow",
#                       "WOW", "cool", "GREAT","magnificent", "magical",
#                       "very cool", "stylish", "beautiful", "so beautiful",
#                       "so stylish", "so professional", "lovely",
#                       "so lovely", "very lovely", "glorious","so glorious",
#                       "very glorious", "adorable", "excellent", "amazing"],
#                      [".", "..", "...", "!", "!!", "!!!"]],

        comment_list=[["this", "that"],
                      ["photo", "picture", "pic", "shot"],
                      ["is", "looks", "is really"],
                      ["great", "awesome", "super", "good", "very good", "good",
                       "cool", "GREAT","magnificent",
                       "very cool", "stylish", "beautiful", "so beautiful",
                       "so stylish", "so professional",
                       "amazing"],
                      [".", "..", "...", "!", "!!", "!!!"]],                  

    # Use unwanted_username_list to block usernames containing a string
    ## Will do partial matches; i.e. 'mozart' will block 'legend_mozart'
    ### 'free_followers' will be blocked because it contains 'free'
        unwanted_username_list=[
            'second', 'stuff', 'art', 'project', 'love', 'life', 'food', 'blog',
            'free', 'keren', 'photo', 'graphy', 'indo', 'travel', 'art', 'shop',
            'store', 'sex', 'toko', 'jual', 'online', 'murah', 'jam', 'kaos',
            'case', 'baju', 'fashion', 'corp', 'tas', 'butik', 'grosir', 'karpet',
            'sosis', 'salon', 'skin', 'care', 'cloth', 'tech', 'rental', 'kamera',
            'beauty', 'express', 'kredit', 'collection', 'impor', 'preloved',
            'follow', 'follower', 'gain', '.id', '_id', 'bags'
        ],
        unfollow_whitelist=['example_user_1', 'example_user_2'])

    return bot
    
#def bot_follow_fixer(bot):
#    bot.follow_per_day = random.randint(250,285)
#    bot.unfollow_per_day = random.randint(250, 285)
#    return bot
    
def loop(bot):
    while True:
    
    #print("# MODE 0 = ORIGINAL MODE BY LEVPASHA")
    #print("## MODE 1 = MODIFIED MODE BY KEMONG")
    #print("### MODE 2 = ORIGINAL MODE + UNFOLLOW WHO DON'T FOLLOW BACK")
    #print("#### MODE 3 = MODIFIED MODE : UNFOLLOW USERS WHO DON'T FOLLOW YOU BASED ON RECENT FEED")
    #print("##### MODE 4 = MODIFIED MODE : FOLLOW USERS BASED ON RECENT FEED ONLY")
    #print("###### MODE 5 = MODIFIED MODE : JUST UNFOLLOW EVERYBODY, EITHER YOUR FOLLOWER OR NOT")

    ################################
    ##  WARNING   ###
    ################################

    # DON'T USE MODE 5 FOR A LONG PERIOD. YOU RISK YOUR ACCOUNT FROM GETTING BANNED
    ## USE MODE 5 IN BURST MODE, USE IT TO UNFOLLOW PEOPLE AS MANY AS YOU WANT IN SHORT TIME PERIOD

        mode = 0

    #print("You choose mode : %i" %(mode))
    #print("CTRL + C to cancel this operation or wait 30 seconds to start")
    #time.sleep(30)

        if mode == 0:
            bot.new_auto_mod()
    
        elif mode == 1:
            check_status(bot)
            while bot.self_following - bot.self_follower > 200:
                unfollow_protocol(bot)
                time.sleep(10 * 60)
                check_status(bot)
            while bot.self_following - bot.self_follower < 400:
                while len(bot.user_info_list) < 50:
                    feed_scanner(bot)
                    time.sleep(5 * 60)
                    follow_protocol(bot)
                    time.sleep(10 * 60)
                    check_status(bot)
    
        elif mode == 2:
            bot.bot_mode = 1
            bot.new_auto_mod()
    
        elif mode == 3:
            unfollow_protocol(bot)
            time.sleep(10 * 60)
    
        elif mode == 4:
            feed_scanner(bot)
            time.sleep(60)
            follow_protocol(bot)
            time.sleep(10 * 60)
    
        elif mode == 5:
            bot.bot_mode = 2
            unfollow_protocol(bot)
    
        else:
            print("Wrong mode!")

if __name__ == '__main__':
    main()