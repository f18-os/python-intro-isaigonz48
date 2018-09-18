#!usr/bin/env python3

import os, sys, time, re

pid = os.getpid()

while True:
    os.write(1, ("command prompt:").encode())

    userInput = os.read(0, 1024)
    ###### Removes \n character at end of input
    userInput = userInput[:-1]

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
            temp = re.split(" > ", userInput.decode())
            userInput = temp[0].encode()
            outFile = temp[1]
            break
        elif arg == ">>":
            extOut = 2
            temp = re.split(" >> ", userInput.decode())
            userInput = temp[0].encode()
            outFile = temp[1]
            break

        elif arg == "<":
            extIn = 1
            temp = re.split(" < ", userInput.decode())
            userInput = temp[0].encode()
            inFile = temp[1]
            break
        
        elif arg == "|":
            pipeUsed = 1
            sepCalls = re.split(" \| ", userInput.decode())
            break
    if pipeUsed:
        pipeFds = os.pipe()
        os.set_inheritable(pipeFds[0], True)
        os.set_inheritable(pipeFds[1], True)
    rc = os.fork()
    
    if rc < 0:
        os.write(2, ("Fork failed, returning %d\n" % rc).encode())
        sys.exit()

    elif rc == 0:
        if pipeUsed:
            nc = os.fork()
            if nc < 0:
                os.write(2, ("Fork failed, returning %d\n" % nc).encode())
                sys.exit()
            ######## New child supposed to write into pipe
            elif nc == 0:
                #os.set_inheritable(pipeFds[1],True)
                #os.set_inheritable(pipeFds[0],True)
                os.close(1)
                sys.stdout = os.fdopen(os.dup(pipeFds[1]), 'w')
                #os.fdopen(fd)
                fd = sys.stdout.fileno()
                os.set_inheritable(fd,True)
                userInput = sepCalls[0].encode()
                os.close(3)
                os.close(4)
            ####### Original child supposed to read from pipe
            else:
                #childPid = os.wait()
                #os.set_inheritable(pipeFds[0],True)
                #os.set_inheritable(pipeFds[1],True)
                os.close(0)
                sys.stdin = os.fdopen(os.dup(pipeFds[0]), 'r')
                #print (fd)
                #os.fdopen(fd)
                fd = sys.stdin.fileno()
                os.set_inheritable(fd, True)
                os.close(3)
                os.close(4)
                
                userInput = sepCalls[1].encode()        
                
        ####### Decodes userInput and removes last or first space char if there is one
        userInput = userInput.decode()
        if userInput[-1] == ' ':
            userInput = userInput[:-1]
        if userInput[0] == ' ':
            userInput = userInput[1:-1]
        args = re.split(" ", userInput)

        ############################################ Input redirection
        if extIn == 1:
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
        sys.exit()
        
    else:    
        childPidCode = os.wait()
        if pipeUsed:
            os.close(pipeFds[0])
            os.close(pipeFds[1])
