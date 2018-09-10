import os, sys, time, re

pid = os.getpid()

os.write(1, ("Starting up shell\n").encode())
exitNum = 0
while True:
    os.write(1, ("command prompt:").encode())

    userInput = os.read(0, 1024)
    userInput = userInput[:-1]

    if userInput.decode() == "stop":
        #print (args[-1])
        sys.exit()
        #break
        #sys.exit()

    extOut = 0    
    checkSymbols = re.split(" ", userInput.decode())
    for arg in checkSymbols:
        if arg == ">":
            print ("1")
            extOut = 1
            temp = re.split(" > ", userInput.decode())
            userInput = temp[0].encode()
            outFile = temp[1]
        elif arg == ">>":
            print ("2")
            extOut = 2
            temp = re.split(" >> ", userInput.decode())
            userInput = temp[0].encode()
            outFile = temp[1]
            
    rc = os.fork()

    if rc < 0:
        os.write(2, ("Fork failed, returning %d\n" % rc).encode())
        sys.exit()

    elif rc == 0:
        #os.write(1, ("%s : \n" % os.environ['PATH']))while True:
        userInput = userInput.decode()
        if userInput[-1] == ' ':
            userInput = userInput[:-1]
        args = re.split(" ", userInput)
        #args = arg
        #args = {"blah", "pls"}
        
        #print (args[-1])
        #print (args[1])
        #print (args[0])

        if extOut == 2:
            #print ("2")
            with open(outFile, "r") as readFile:
                curText = readFile.read()
            readFile.close()
            
            os.close(1)
            sys.stdout = open(outFile, "w")
            fd = sys.stdout.fileno()
            os.set_inheritable(fd,True)
            #os.write(1, ("Writing in here").encode())
            os.write(1, (curText).encode())

        elif extOut == 1:
            #print ("1")
            os.close(1)
            sys.stdout = open(outFile, "w")
            fd = sys.stdout.fileno()
            os.set_inheritable(fd,True)
            #os.write(1, ("Writing in here").encode())

        #print (args[0])
        #print (args[1])
        #print (args[2])
        print (userInput)
        for dir in re.split(":", os.environ['PATH']):
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program,args,os.environ)
            except FileNotFoundError:
                pass
            
        os.write(2, ("Error try again\n").encode())
        
        
    else:
        #os.write(1, ("What happen"))
    
        childPidCode = os.wait()
        #time.sleep(2)
        #os.write(1, ("SEE YA\n").encode())
