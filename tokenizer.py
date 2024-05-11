class Tokenizer:
        
        def __init__(self, filename):
                jack_file = open(filename, "r");
                self.lines = jack_file.readlines();
                jack_file.close();
                self.tokens = []
                self.token = '';
                self.comment_mode = False



        def add_token(self):
                if len(self.token) > 0:
                        self.tokens.append(self.token); 
                self.token = ''
       


        def tokenize(self):       
                for line in self.lines:
                
                        prev_char = '@'
                        string_mode = False;
                        for c in line :
                                
                                if self.comment_mode:
                                        if prev_char == '*' and c == '/':
                                                self.comment_mode = False;
                                        prev_char = c;
                                else:
                                        if prev_char == '/' and c == '/':
                                                self.tokens.pop()
                                                self.token = ''      
                                                break;

                                        elif prev_char == '/' and c == '*':
                                                self.tokens.pop()
                                                self.token = ''       
                                                self.comment_mode = True
                                        else:
                                                if string_mode:
                                                        self.token += c;
                                                        if c == '"':
                                                                self.add_token();
                                                                string_mode = False;
                                                elif c == ';':
                                                        self.add_token();
                                                        self.token += c;
                                                        self.add_token();
                                                elif c == ' ' or c == '\n' or c == '\t':
                                                
                                                        self.add_token();
                                                elif c == '(' or c == ')' or c == '{' or c == '}' or c == '[' or c == ']':
                                                        self.add_token();
                                                        self.token += c;
                                                        self.add_token();
                                                elif c == '<' or c == '>' or c == '+' or c == '-' or c == '*' or c == '/':                 
                                                        self.add_token()
                                                        self.token += c
                                                        self.add_token()
                                                elif c == '|' or c == '&' or c == '~' or c == ',' or c == '.':
                                                        self.add_token();
                                                        self.token += c;
                                                        self.add_token();
                                                elif c == '"':
                                                        
                                                        string_mode = True;
                                                        self.token += c;        
                                                else :
                                                        self.token += c        
                                        prev_char = c;
        
        


        def type (str):
                flag = True
                for c in str : 
                        if c < '0' or c > '9' :
                                flag = False
                                break
        
                if flag :
                        return 'integerConstant'
                elif str == 'class' or str == 'constructor' or str == 'function' or str == 'method':
                        return 'keyword'
                elif str == 'field' or str == 'static' or str == 'var' or str == 'int':
                        return 'keyword'
                elif str == 'char' or str == 'boolean' or str == 'void' or str == 'true':
                        return 'keyword'
                elif str == 'false' or str == 'null' or str == 'this' or str == 'let':
                        return 'keyword'                
                elif str == 'do' or str == 'if' or str == 'else' or str == 'while' or str == 'return':
                        return 'keyword'        
                elif str == '(' or str == ')' or str == '[' or str == ']':
                        return 'symbol'
                elif str == '{' or str == '}' or str == '.' or str == ',' or str == ';':
                        return 'symbol'
                elif str == '+' or str == '-' or str == '*' or str == '/' or str == '&':
                        return 'symbol'
                elif str == '|' or str == '<' or str == '>' or str == '=' or str == '~':
                        return 'symbol'                                                
                elif str[0] == '"':
                        return 'stringConstant'
                elif str[0] > '9' or str[0] < '0':
                        return 'identifier'       
                else :
                        return "notDefinedType"                 



