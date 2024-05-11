class VMWriter:
        label = 1
        def __init__(self, filePath):
                filePath += '.vm'
                self.VMFile = open(filePath, 'w');
                

        def writePush(self, segment, index):
                self.VMFile.write("push " + segment + ' ' + str(index) + '\n')

        def writePop(self, segment, index):
                self.VMFile.write("pop " + segment + ' ' + str(index) + '\n')        

        def writeArithmetic (self, command):
                if command == '+':
                        self.VMFile.write('add' + '\n')
                elif command == '-':
                        self.VMFile.write('sub' + '\n')
                elif command == '>':
                        self.VMFile.write('gt' + '\n')
                elif command == '<':
                        self.VMFile.write('lt' + '\n')
                elif command == '=':
                        self.VMFile.write('eq' + '\n')
                elif command == '|':
                        self.VMFile.write('or' + '\n')
                elif command == '&':
                        self.VMFile.write('and' + '\n') 
                elif command == '~':
                        self.VMFile.write('not' + '\n')
                elif command == '@':
                        self.VMFile.write('neg' + '\n')  
                elif command == '*':
                        self.writeCall('Math.multiply', 2)
                elif command == '/':
                        self.writeCall('Math.divide', 2)                                                                             

        def writeLabel(self, label):
                self.VMFile.write("label " + label + '\n')

        def writeGoto(self, label):
                self.VMFile.write("goto " + label + '\n')   

        def writeIf(self, label):
                self.VMFile.write("if-goto " + label + '\n')

        def writeCall(self, name, nArgs):
                self.VMFile.write("call " + name + ' ' + str(nArgs) + '\n')

        def writefunction(self, name, nVars):
                self.VMFile.write('function ' + name + ' ' + str(nVars)+ '\n')
                

        def writeReturn(self):
                self.VMFile.write("return\n")

        def generateLabel(self):
                ret = 'L' + str(VMWriter.label)
                VMWriter.label += 1
                return ret
        def close(self):
                self.VMFile.close()                       



                