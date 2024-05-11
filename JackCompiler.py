import tokenizer
import compileEngine
import os 
import sys

inpt = sys.argv[1]


filePath = []

if ".jack" in inpt :
        filePath.append(inpt)
else :
        files = os.listdir(inpt)
        for file in files :
                if ".jack" in file:
                        path = inpt
                        path += '/'
                        path += file
                        filePath.append(path)        

n = len(filePath)
for i in range(n):
        obj = tokenizer.Tokenizer(filePath[i])
        obj.tokenize()
        obj1 = compileEngine.compileEngine(obj.tokens, filePath[i][0 : len(filePath[i]) - 5])
        obj1.compile_class()
