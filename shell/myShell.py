#! /usr/bin/env python3

import os, sys, time, re


while True:
    pid = os.getpid()

    if ("PS1" in os.environ):
        os.write(1,(os.environ["PS1"]).encode())
    else:
        os.write(1,("prompt:").encode())

    userInput = os.read(0, 1024)
    
    ###### Removes \n character at end of input
    if userInput.decode()[-1] == '\n':
        userInput = userInput[:-1]

    if len(userInput) < 1:
        continue
    if userInput.decode() == "exit":
        sys.exit()

    ######## Flags
    extOut = 0
    extIn = 0
    pipeUsed = 0
    ######## Checks for use of >> > < or |
    checkSymbols = re.split(" ", userInput.decode())
    for arg in checkSymbols:
        if arg == ">":
            extOut = 1
            temp = re.split(">", userInput.decode())
            userInput = temp[0].encode()
            outFile = temp[1]
            break
        elif arg == ">>":
            extOut = 2
            temp = re.split(">>", userInput.decode())
            userInput = temp[0].encode()
            outFile = temp[1]
            break

        elif arg == "<":
            extIn = 1
            temp = re.split("<", userInput.decode())
            userInput = temp[0].encode()
            inFile = temp[1]
            break
        
        elif arg == "|":
            pipeUsed = 1
            sepCalls = re.split("\|", userInput.decode())
            break
        
    if pipeUsed:
        pipeR,pipeW = os.pipe()
        for f in (pipeR, pipeW):
            os.set_inheritable(f, True)

    rc = os.fork()
    
    if rc < 0:
        os.write(2, ("Fork failed, returning %d\n" % rc).encode())
        sys.exit()

    elif rc == 0:
        if pipeUsed:
            nc = os.fork()
            if nc < 0:
                os.write(2, ("Fork failed, returning %d\n" % nc).encode())
                sys.exit(1)
            ######## New child writes into pipe
            elif nc == 0:
                os.close(1)
                os.dup(pipeW)
                os.set_inheritable(1,True)
                os.close(pipeR)
                os.close(pipeW)
                
                userInput = sepCalls[0].encode()

            ####### Original child reads from pipe
            else:
                os.close(0)
                os.dup(pipeR)
                os.set_inheritable(0,True)
                os.close(pipeR)
                os.close(pipeW)
                
                userInput = sepCalls[1].encode()

        ####### Decodes userInput and removes last or first space char if there is one
        userInput = userInput.decode()
        if userInput[-1] == ' ':
            userInput = userInput[:-1]
        if len(userInput) < 1:
            sys.exit()
        if userInput[0] == ' ':
            userInput = userInput[1:]
        args = re.split(" ", userInput)

        ############################################ Input redirection
        if extIn == 1:
            if inFile[0] == ' ':
                inFile = inFile[1:]
            if inFile[-1] == ' ':
                inFile = inFile[:-1]
            os.close(0)
            sys.stdin = open(inFile, "r")
            fd = sys.stdin.fileno()
            os.set_inheritable(fd,True)
        ######################################### Output redirection
        ####### >>
        if extOut == 2:
            ####### Must put what was already in file, back in
            if outFile[0] == ' ':
                outFile = outFile[1:]
            if outFile[-1] == ' ':
                outFile = outFile[:-1]
            with open(outFile, "r") as readFile:
                curText = readFile.read()
            readFile.close()
            
            os.close(1)
            sys.stdout = open(outFile, "w")
            fd = sys.stdout.fileno()
            os.set_inheritable(fd,True)
            os.write(1, (curText).encode())
        ####### >
        elif extOut == 1:
            if outFile[0] == ' ':
                outFile = outFile[1:]
            if outFile[-1] == ' ':
                outFile = outFile[:-1]
            os.close(1)
            sys.stdout = open(outFile, "w")
            fd = sys.stdout.fileno()
            os.set_inheritable(fd,True)

        ####################################### Executing
        for dir in re.split(":", os.environ['PATH']):
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program,args,os.environ)
            except FileNotFoundError:
                pass
            
        os.write(2, ("Error try again\n").encode())
        sys.exit(1)
        
    else:    
        if pipeUsed:
            os.close(pipeR)
            os.close(pipeW)
        childPidCode = os.wait()
