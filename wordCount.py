import sys
import os
import re

if len(sys.argv) is not 3:
    print("Correct usage: wordCount.py <input text file> <output file>")
    exit()
    
fInName = sys.argv[1]
if not os.path.exists(fInName):
    print("Input text file does not exist")
    exit()

fOutName = sys.argv[2]

file = open(fInName, "r")

wordList = {}

for line in file:
    line = re.sub('[^a-zA-Z\n]', ' ',line)
    
    for word in line.split():

        if (word.lower() in wordList):
            wordList[word.lower()] += 1
        else:
            wordList[word.lower()] = 1
            
file.close()

file = open(fOutName,"w")

for word,repetitions in sorted(wordList.items()):
    file.write(word)
    file.write(" ")
    file.write("%d\n" % repetitions)
