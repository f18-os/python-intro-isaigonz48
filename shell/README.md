# Python Shell Assignment

* Developed using python3, should work with previous versions (Used python3 because paths were not working for my linux on python 2.7)

* Supports any commands available on standard library

* Supports simple (one) output redirection and input redirection, not on same command
** '<<' is not supported (did not know if it should)
* Single pipeline is supported

* Commands should work if tokens are separated by a space (ex. "wc myShell.py")
** Otherwise, results may vary

* '&' is somewhat supported. Once used, it causes a bug where the rest of the commands will also run in background

* To exit the shell, type "exit" or send an EOF