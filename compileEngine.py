import tokenizer
import VMWriter
import SymbolTable
class compileEngine :
        def __init__(self, input, filePath):
                self.tokens = input
                self.cur_index = 0
                self.VM = VMWriter.VMWriter(filePath)
                self.classSymbolTable = SymbolTable.SymbolTable()
                self.subroutineSymbolTable = SymbolTable.SymbolTable()
                self.compilation_error = False
                self.binary_operators = ['+', '-', '*', '/', '&', '|', '>', '<', '=']
                self.className = ''
                self.subroutineName = ''
                self.nArgs = 0
                self.cons = 0
        def eat_alpha(self, expected):
                if self.tokens[self.cur_index] != expected:
                        self.compilation_error = True
                        self.VM.VMFile.write("compilation error ...expected to see " + expected + " but found " + self.tokens[self.cur_index])

        def eat_type(self, expected):
            if tokenizer.Tokenizer.type(self.tokens[self.cur_index]) != expected:
                        self.compilation_error = True
                        self.VM.VMFile.write(self.tokens[self.cur_index] + '\n')
                        self.VM.VMFile.write("compilation error ...expected to see " + expected + " token but found " + tokenizer.Tokenizer.type(self.tokens[self.cur_index]))    

        def compile_class(self):
                self.eat_alpha("class")
                if self.compilation_error:
                        return

                self.cur_index += 1

                self.eat_type("identifier")
                if self.compilation_error:
                        return
                self.className = self.tokens[self.cur_index]
                self.cur_index += 1

                self.eat_alpha("{")
                if self.compilation_error:
                        return
                self.cur_index += 1


                while self.tokens[self.cur_index] != "}":

                        if self.compilation_error:
                                return

                        if self.tokens[self.cur_index] == "field" or self.tokens[self.cur_index] == 'static':
                                self.compile_class_var_dec()                
                        else :
                                self.compile_subroutine_dec()
                                


                self.eat_alpha("}")
                if self.compilation_error:
                        return
                self.cur_index += 1
                self.VM.close()

        
        def compile_subroutine_dec(self):
               
                if self.tokens[self.cur_index] == 'method' or self.tokens[self.cur_index] == 'function':                
                        if self.tokens[self.cur_index] == 'method':
                                self.cons = 2
                        else :
                                self.cons = 0
                        self.cur_index += 1
                        if self.tokens[self.cur_index] == "boolean" or self.tokens[self.cur_index] == "char" or self.tokens[self.cur_index] == "int" or self.tokens[self.cur_index] == "void":
                                self.cur_index += 1
                        else :
                                self.eat_type("identifier")
                                if self.compilation_error:
                                        return
                                self.cur_index += 1 

                        self.eat_type("identifier")
                        if self.compilation_error:
                                return
                        self.subroutineName = self.tokens[self.cur_index]
                        self.cur_index += 1   

                else :
                        self.cons = 1
                        self.subroutineName = 'new'
                        self.eat_alpha("constructor")
                        if self.compilation_error :
                                return


                        self.cur_index += 1

                        self.eat_type("identifier")
                        if self.compilation_error:
                                return

                        self.cur_index += 1  

                        self.eat_alpha("new")
                        if self.compilation_error:
                                return
                        self.cur_index += 1          



                self.eat_alpha('(')
                if self.compilation_error:
                        return
                self.cur_index += 1
                self.compile_parameter_list()
                self.eat_alpha(')')
                if self.compilation_error:
                        return
                
                self.cur_index += 1
                self.compile_subroutine_body()


        def compile_parameter_list(self):
                key = 1
                if self.cons == 2:
                        self.subroutineSymbolTable.define('object', 'argument', self.className)
                while self.tokens[self.cur_index] != ')':
                        if key == 1 :
                                type = self.tokens[self.cur_index]
                                self.cur_index += 1               
                                
                                self.eat_type("identifier")
                                if self.compilation_error:
                                        return
                                name = self.tokens[self.cur_index]     
                                self.subroutineSymbolTable.define(name, 'argument', type)          
                                
                                self.cur_index += 1
                                key = 0        
                        else :
                                self.eat_alpha(",")
                                if self.compilation_error:
                                        return
                                
                                self.cur_index += 1
                                key = 1


       
        def compile_term(self):
               
                type_of_token = tokenizer.Tokenizer.type(self.tokens[self.cur_index])
                if type_of_token == 'stringConstant':
                        token = self.tokens[self.cur_index]
                        token = token[1 : ]
                        token = token[0 : -1]
                        length = len(token)
                        self.VM.writePush('constant', length)
                        self.VM.writeCall('String.new', 1)
                        for c in token:
                                self.VM.writePush('constant', ord(c))
                                self.VM.writeCall('String.appendChar', 2)
                        self.cur_index += 1
                elif type_of_token == 'integerConstant':
                        self.VM.writePush("constant", self.tokens[self.cur_index])
                        self.cur_index += 1
                elif type_of_token == 'keyword':
                        if self.tokens[self.cur_index] != 'null' and self.tokens[self.cur_index] != 'this' and self.tokens[self.cur_index] != 'true' and self.tokens[self.cur_index] != 'false':
                                self.compilation_error = True
                                self.new_file.write("compilation error ..expected to see null, this, true, false keyword\n")
                        if self.compilation_error:
                                return
                        if self.tokens[self.cur_index] == 'true':
                                self.VM.writePush('constant', 0)
                                self.VM.writeArithmetic('~')
                        elif self.tokens[self.cur_index] == 'false' or self.tokens[self.cur_index] == 'null':
                                self.VM.writePush('constant', 0)
                        elif self.tokens[self.cur_index] == 'this':
                                self.VM.writePush('pointer', 0)

                        self.cur_index += 1
                
                elif self.tokens[self.cur_index] == '-' or self.tokens[self.cur_index] == '~':
                        saved_operator = self.tokens[self.cur_index]
                        self.cur_index += 1
                        self.compile_term()
                        if saved_operator == '-':
                                saved_operator = '@'
                        self.VM.writeArithmetic(saved_operator)
                elif self.tokens[self.cur_index] == '(' or self.tokens[self.cur_index] == '[':
                        
                        self.cur_index += 1
                        self.compile_expression()
                        self.eat_alpha(')')
                        if self.compilation_error:
                                return
                       
                        self.cur_index += 1
                
                else :
                        self.eat_type("identifier")
                        if self.compilation_error:
                                return
                        varName = self.tokens[self.cur_index]        
                        self.cur_index += 1
                        if self.tokens[self.cur_index] == '[':
                                self.cur_index += 1
                                index = self.subroutineSymbolTable.indexOf(varName)
                                segment = ''
                                order = 0
                                if index != -1:
                                        segment = self.subroutineSymbolTable.kind[index]
                                        order = self.subroutineSymbolTable.order[index]
                                else :
                                        index = self.classSymbolTable.indexOf(varName)
                                        segment = self.classSymbolTable.kind[index]
                                        order = self.classSymbolTable.order[index]
                                self.VM.writePush(segment, order)
                                self.compile_expression()
                                self.VM.writeArithmetic('+')
                                self.VM.writePop('pointer', 1)
                                self.VM.writePush('that', 0)
                                self.eat_alpha(']')
                                if self.compilation_error:
                                        return
                                self.cur_index += 1
                        elif self.tokens[self.cur_index] == '.':
                                self.cur_index += 1
                                self.eat_type("identifier")
                                if self.compilation_error:
                                        return
                                index = self.subroutineSymbolTable.indexOf(varName)
                                subroutine = 0
                                method = 0
                                segment = ''
                                order = 0
                                if index == -1:
                                        index = self.classSymbolTable.indexOf(varName)
                                else :
                                        subroutine = 1        
                                
                                if index != -1:
                                        method = 1
                                        if subroutine == 1:
                                                varName = self.subroutineSymbolTable.typeOf(self.subroutineSymbolTable.name[index])
                                                segment = self.subroutineSymbolTable.kind[index]
                                                order = self.subroutineSymbolTable.order[index]
                                        else:
                                                varName = self.classSymbolTable.typeOf(self.classSymbolTable.name[index])
                                                segment = self.classSymbolTable.kind[index]
                                                order = self.classSymbolTable.order[index]
                                

                                varName += '.'
                                varName += self.tokens[self.cur_index]
                                self.cur_index += 1
                                self.eat_alpha('(')
                                if self.compilation_error:
                                        return
                                self.cur_index += 1
                                if method == 1:
                                        self.VM.writePush(segment, order)
                                self.compile_expression_list()
                                self.VM.writeCall(varName, self.nArgs + method)
                                self.eat_alpha(')')
                                if self.compilation_error:
                                        return
                                self.cur_index += 1
                        elif self.tokens[self.cur_index] == '(':
                                self.cur_index += 1
                                self.VM.writePush('pointer', 0)
                                self.compile_expression_list()
                                callee = self.className
                                callee += '.'
                                callee += varName
                                self.VM.writeCall(callee, self.nArgs + 1)
                                self.eat_alpha(')')
                                if self.compilation_error:
                                        return
                                self.cur_index += 1
                        else:
                                index = self.subroutineSymbolTable.indexOf(varName)
                                segment = ''
                                order = 0
                                if index != -1:
                                        segment = self.subroutineSymbolTable.kind[index]
                                        order = self.subroutineSymbolTable.order[index]
                                else :
                                        index = self.classSymbolTable.indexOf(varName)
                                        segment = self.classSymbolTable.kind[index]
                                        order = self.classSymbolTable.order[index]
                                self.VM.writePush(segment, order)

        def compile_expression(self):
                last_token_is_term = 0
                saved_operator = '$'
                while True:
                        if self.tokens[self.cur_index] == ',' or self.tokens[self.cur_index] == ';' or self.tokens[self.cur_index] == ']' or self.tokens[self.cur_index] == ')':
                                break
                                                
                
                        if last_token_is_term == 1:
                               
                                if self.tokens[self.cur_index] in self.binary_operators:
                                        saved_operator = self.tokens[self.cur_index]
                                        last_token_is_term = 0
                                        self.cur_index += 1
                                else :
                                        self.compilation_error = True
                                        self.new_file.write("compilation error... binary operator should come after a term \n")
                                        return                                
                        
                               
                        else :
                                
                                self.compile_term()
                                if saved_operator != '$':
                                        self.VM.writeArithmetic(saved_operator)
                                last_token_is_term = 1
                                

                
       
        def compile_class_var_dec(self):
                if self.tokens[self.cur_index] != "field" and self.tokens[self.cur_index] != "static":
                        self.compilation_error = True
                if self.compilation_error:
                        return
                kind = self.tokens[self.cur_index]
                if kind == 'field':
                        kind = 'this'
                self.cur_index += 1
                type = self.tokens[self.cur_index]
                self.cur_index += 1        
                key = 1
                while self.tokens[self.cur_index] != ";":
                        if key == 1:
                                self.eat_type("identifier")
                                if self.compilation_error:
                                        return
                                self.classSymbolTable.define(self.tokens[self.cur_index], kind, type)
                                self.cur_index += 1
                                key = 0
                        else :
                                self.eat_alpha(",")
                                if self.compilation_error:
                                        return
                                self.cur_index += 1
                                key = 1                
                self.eat_alpha(';')
                if self.compilation_error:
                        return
                self.cur_index += 1

        def compile_subroutine_var_dec(self):
                self.eat_alpha("var")
                if self.compilation_error:
                        return
                self.cur_index += 1

                type = self.tokens[self.cur_index]
                self.cur_index += 1       
                key = 1
                while self.tokens[self.cur_index] != ";":
                        if key == 1:
                                self.eat_type("identifier")
                                if self.compilation_error:
                                        return
                                name = self.tokens[self.cur_index]
                                self.subroutineSymbolTable.define(name, 'local', type)
                                self.cur_index += 1
                                key = 0
                        else :
                                self.eat_alpha(",")
                                if self.compilation_error:
                                        return
                                self.cur_index += 1
                                key = 1                
                self.eat_alpha(';')
                if self.compilation_error:
                        return
                self.cur_index += 1       
 

        def compile_subroutine_body(self):
                if self.subroutineName == 'moveBall':
                        self.classSymbolTable.print()
                self.eat_alpha("{")
                if self.compilation_error:
                        return
                self.cur_index += 1

                while self.tokens[self.cur_index] != '}':
                        if self.compilation_error:
                                return

                        if self.tokens[self.cur_index] == 'var':
                                self.compile_subroutine_var_dec()
                        else :
                                
                                self.VM.writefunction(self.className + '.' + self.subroutineName, self.subroutineSymbolTable.varCount('local'))
                                if self.cons == 1:
                                        self.VM.writePush('constant', self.classSymbolTable.varCount('this'))
                                        self.VM.writeCall('Memory.alloc', 1)
                                        self.VM.writePop('pointer', 0)
                                elif self.cons == 2:
                                        self.VM.writePush('argument', 0)
                                        self.VM.writePop('pointer', 0)        
                                self.compile_statements()               
                self.eat_alpha("}")
                if self.compilation_error:
                        return
                self.cur_index += 1
                self.subroutineSymbolTable.reset()


        def compile_expression_list(self):
                cnt = 0
                while self.tokens[self.cur_index] != ')':
                        if self.compilation_error:
                                return
                        if self.tokens[self.cur_index] == ',':
                                self.cur_index += 1
                        else :
                                self.compile_expression()
                                cnt += 1
                        
                self.nArgs = cnt
                
                

        def compile_let(self):
                self.eat_alpha("let")
                if self.compilation_error:
                        return
                
                self.cur_index += 1
                self.eat_type("identifier")
                if self.compilation_error:
                        return
                varName = self.tokens[self.cur_index]
                
                self.cur_index += 1
                if self.tokens[self.cur_index] != '=':
                        self.eat_alpha("[")
                        if self.compilation_error:
                                return
                        self.cur_index += 1 
                        segment = ''
                        order = 0
                        index = self.subroutineSymbolTable.indexOf(varName)
                        if index != -1:
                                segment = self.subroutineSymbolTable.kind[index]
                                order = self.subroutineSymbolTable.order[index]
                        else :
                                index = self.classSymbolTable.indexOf(varName)
                                segment = self.classSymbolTable.kind[index]
                                order = self.classSymbolTable.order[index]        
                        self.VM.writePush(segment, order)
                        self.compile_expression()
                        self.VM.writeArithmetic('+')
                        self.eat_alpha("]")
                        if self.compilation_error:
                                return
                        self.cur_index += 1        
                        self.eat_alpha('=')
                        if self.compilation_error:
                                return
                        self.cur_index += 1
                        self.compile_expression()
                        self.VM.writePop('temp', 0)
                        self.VM.writePop('pointer', 1)
                        self.VM.writePush('temp', 0)
                        self.VM.writePop('that', 0)
                              
                else :
                        self.eat_alpha('=')
                        if self.compilation_error:
                                return
                        self.cur_index += 1
                        self.compile_expression()
                        segment = ''
                        order = 0
                        index = self.subroutineSymbolTable.indexOf(varName)
                        if index != -1:
                                segment = self.subroutineSymbolTable.kind[index]
                                order = self.subroutineSymbolTable.order[index]
                        else :
                                index = self.classSymbolTable.indexOf(varName)
                                segment = self.classSymbolTable.kind[index]
                                order = self.classSymbolTable.order[index]        
                        self.VM.writePop(segment, order)
                self.eat_alpha(';')
                if self.compilation_error:
                        return
                
                self.cur_index += 1        



        
        def compile_do(self):
                
                self.eat_alpha("do")
                if self.compilation_error:
                        return
                
                self.cur_index += 1
                        
                self.eat_type("identifier")
                if self.compilation_error:
                        return
                clss_obj = self.tokens[self.cur_index]
                callee = ''        
                method = 1
                segment = ''
                order = 0
                dot = 0
                self.cur_index += 1
                if self.tokens[self.cur_index] == '.':
                        dot = 1
                        self.cur_index += 1
                        index = self.subroutineSymbolTable.indexOf(clss_obj)
                        subroutineTable = 0
                        if index == -1:
                              index = self.classSymbolTable.indexOf(clss_obj)
                        else :
                                subroutineTable = 1         
                        if index == -1:
                                callee += clss_obj
                                callee += '.'
                                method = 0
                        else :
                                if subroutineTable == 1:
                                        segment = self.subroutineSymbolTable.kind[index]
                                        order = self.subroutineSymbolTable.order[index]
                                        clss_obj = self.subroutineSymbolTable.typeOf(self.subroutineSymbolTable.name[index])
                                else:
                                        segment = self.classSymbolTable.kind[index]
                                        order = self.classSymbolTable.order[index]
                                        clss_obj = self.classSymbolTable.typeOf(self.classSymbolTable.name[index])
                                callee += clss_obj
                                callee += '.'        

                if dot == 0:
                        callee = self.className
                        callee += '.'
                        callee += clss_obj
                else :        
                        self.eat_type("identifier")
                        if self.compilation_error:
                                return
                        callee += self.tokens[self.cur_index] 
                        self.cur_index += 1      
                self.eat_alpha('(')
                if self.compilation_error:
                        return
               
                self.cur_index += 1
                
                if method == 1:
                        if dot == 0:
                                self.VM.writePush('pointer', 0)
                        else:
                                self.VM.writePush(segment, order)
                self.compile_expression_list() 
                

                self.VM.writeCall(callee, self.nArgs + method)
                self.eat_alpha(')')
                if self.compilation_error:
                        return
               
                self.cur_index += 1
                self.eat_alpha(';')
                self.VM.writePop('temp', 0)
                if self.compilation_error:
                        return
                
                self.cur_index += 1                               
                



        def compile_while(self):
                start_label = self.VM.generateLabel()
                end_label = self.VM.generateLabel()
                self.VM.writeLabel(start_label)
                self.eat_alpha("while")
                if self.compilation_error:
                        return
                self.cur_index += 1
                self.eat_alpha("(")
                if self.compilation_error:
                        return
                self.cur_index += 1
                self.compile_expression()
                self.eat_alpha(")")
                if self.compilation_error:
                        return

                self.cur_index += 1
                self.VM.writeArithmetic('~')
                self.VM.writeIf(end_label)
                self.eat_alpha("{")
                if self.compilation_error:
                        return
                self.cur_index += 1
                self.compile_statements()
                self.eat_alpha("}")
                if self.compilation_error:
                        return
                self.cur_index += 1
                self.VM.writeGoto(start_label)
                self.VM.writeLabel(end_label)


        def compile_return(self):             
                self.eat_alpha("return")
                if self.compilation_error:
                        return
                self.cur_index += 1
                if self.tokens[self.cur_index] == ';':
                        self.VM.writePush('constant', 0)
                        self.VM.writeReturn()
                        self.cur_index += 1        
                        
                else :
                        self.compile_expression()               
                        self.eat_alpha(";")
                        if self.compilation_error:
                                return
                        self.VM.writeReturn()
                        self.cur_index += 1       

        def compile_if(self):            
                self.eat_alpha("if")
                if self.compilation_error:
                        return
                self.cur_index += 1
                self.eat_alpha("(")
                if self.compilation_error:
                        return
                self.cur_index += 1
                self.compile_expression()
                self.eat_alpha(")")
                if self.compilation_error:
                        return
                self.cur_index += 1
                self.eat_alpha("{")
                if self.compilation_error:
                        return

                self.cur_index += 1   
                
                self.VM.writeArithmetic('~')
                elseLabel = self.VM.generateLabel()
                endLabel = self.VM.generateLabel()
                self.VM.writeIf(elseLabel)
                self.compile_statements()
                self.VM.writeGoto(endLabel)
                
                self.eat_alpha("}")
                if self.compilation_error:
                        return

                self.cur_index += 1

                if self.tokens[self.cur_index] == 'else':
                        self.VM.writeLabel(elseLabel)
                        self.cur_index += 1
                        self.eat_alpha("{")
                        if self.compilation_error:
                                return
                        self.cur_index += 1   
                        self.compile_statements()
                        self.eat_alpha("}")
                        if self.compilation_error:
                                return
                        self.cur_index += 1     
                else :
                        self.VM.writeLabel(elseLabel)
                self.VM.writeLabel(endLabel)

        def compile_statements(self):
               
                while self.tokens[self.cur_index] != '}':
                        if self.tokens[self.cur_index] == 'if':
                                self.compile_if()
                        elif self.tokens[self.cur_index] == 'let':
                                self.compile_let()
                        elif self.tokens[self.cur_index] == 'while':
                                self.compile_while()
                        elif self.tokens[self.cur_index] == 'do':
                                self.compile_do()
                        elif self.tokens[self.cur_index] == 'return':
                                self.compile_return()
                        else:
                                self.VM.VMFile.write("compilation error expected to see statement")
                                self.compilation_error = True
                                break                                        
                










