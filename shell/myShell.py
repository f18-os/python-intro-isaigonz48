import os, sys, time, re

pid = os.getpid()

exitNum = 0
while True:
    os.write(1, ("command prompt:").encode())

    userInput = os.read(0, 1024)
    userInput = userInput[:-1]

    if userInput.decode() == "stop":
        sys.exit()

    extOut = 0    
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
            
    rc = os.fork()

    if rc < 0:
        os.write(2, ("Fork failed, returning %d\n" % rc).encode())
        sys.exit()

    elif rc == 0:
        userInput = userInput.decode()
        if userInput[-1] == ' ':
            userInput = userInput[:-1]
        args = re.split(" ", userInput)

        if extOut == 2:
            with open(outFile, "r") as readFile:
                curText = readFile.read()
            readFile.close()
            
            os.close(1)
            sys.stdout = open(outFile, "w")
            fd = sys.stdout.fileno()
            os.set_inheritable(fd,True)
            os.write(1, (curText).encode())

        elif extOut == 1:
            os.close(1)
            sys.stdout = open(outFile, "w")
            fd = sys.stdout.fileno()
            os.set_inheritable(fd,True)

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
