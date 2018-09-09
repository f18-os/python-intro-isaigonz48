import os, sys, time, re

pid = os.getpid()

os.write(1, ("Starting up shell\n").encode())

rc = os.fork()

if rc < 0:
    os.write(2, ("Fork failed, returning %d\n" % rc).encode())
    sys.exit()

elif rc == 0:
    #os.write(1, ("%s : \n" % os.environ['PATH']))
    
    while True:
        os.write(1, ("command prompt:").encode())
        userInput = os.read(0, 1024)
        args = re.split(" ", userInput)
        #args = {"blah", "pls"}
        args[-1] = args[-1][:-1]

        if args[-1] == "stop":
            sys.exit()

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
    os.write(1, ("SEE YA\n").encode())
