#!/usr/bin/env python3
#Author: Darryl Beckham

import json
import requests
import socket
import sys
import subprocess

s = None

class GitHubRepo:
    
    attr_list = {"1":"name", "2":"description", "3":"homepage", "4":"private", "5":"has_issues", "6":"has_wiki", "7":"team_id", "8":"auto_init", "9":"gitignore_template", "10":"license_template"}

    attributes = {"name":None, "description":None}

    def __init__(self, name, desc):
        self.attributes["name"] = name
        self.attributes["description"] = desc

    def getAttr(self):
        return self.attributes

    def getFurtherInfo(self):
        prompt = str(input('Would you like to enter more information about this repository? (y/N): '))
        if prompt.lower() == "y" or prompt.lower() == "yes":
            user_input = menuPrompt()
            if user_input in self.attr_list:
                self.attributes[attr_list[user_input]] = input("Enter", self.attr_list[user_input])
                print("Updated", selfattr_list[user_input], "attribute.")

def menuPrompt():
    print("Select a repository attribute to update.")
    print("1. name")
    print("2. description")
    print("3. homepage")
    print("4. private")
    print("5. has_issues")
    print("6. has_wiki")
    print("7. team_id")
    print("8. auto_init")
    print("9. gitignore_template")
    print("10. license_template")
    return str(input("Press enter to finish."))

def getUserName():
    proc = subprocess.Popen(["git","config","user.name"], stdout=subprocess.PIPE)
    if not proc:
        print("Git environment variable user.name is not set.")
        return
    return proc.stdout.read().rstrip().decode("ascii")

def connectRemote():
    global s
    url = "https://api.github.com/user/repos"
    #print(url)
    remote = socket.gethostbyname(url)
    print("Attempting connection to", remote)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((remote, 80))
        print("Successfully connected to remote.")
    except:
        print("Error connecting to remote location.")

def createRepo(name, desc):
    repo = GitHubRepo(name, desc)
    repo.getFurtherInfo()
    connectRemote()
    user_name = getUserName()
    try:
        s.send("POST " + json.dumps(repo.getAttr()))
        print("Repository sucessfully created.")
        s.close()
        #resp = s.recv(4096)
        #print(resp)
    except:
        print("Error creating repository. Connection closed.")
        s.close()

if len(sys.argv) < 2:
    print("gitcreate NAME DESCRIPTION")
    if len(sys.argv) == 2:
        print("Description field cannot be empty.")
    sys.exit(1)

createRepo(sys.argv[1], sys.argv[2])
