import os, sys, time, re

pid = os.getpid()

os.write(1, ("Starting up shell\n").encode())
exitNum = 0
while True:
    rc = os.fork()

    if rc < 0:
        os.write(2, ("Fork failed, returning %d\n" % rc).encode())
        sys.exit()

    elif rc == 0:
        #os.write(1, ("%s : \n" % os.environ['PATH']))while True:
        os.write(1, ("command prompt:").encode())
        userInput = os.read(0, 1024)
        userInput = userInput[:-1]
        
        args = re.split(" ", userInput.decode())
        #args = arg
        #args = {"blah", "pls"}
        
        if args[-1] == "stop":
            print (args[-1])
            exitNum = 1
            break
            sys.exit()
        print (args[-1])
        #print (args[1])
        #print (args[0])
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
        if(exitNum):
            sys.exit()
        os.write(1, ("SEE YA\n").encode())
