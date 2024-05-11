class SymbolTable:
        static = 0
        def __init__(self):
                self.name = []
                self.kind = []
                self.type = []
                self.order = []
                


        def reset(self):
                self.name.clear()
                self.kind.clear()
                self.type.clear()
                self.order.clear()


        def varCount(self, kind):
                if kind == 'static':
                        return SymbolTable.static
                count = 0
                for var in self.kind:
                        if kind == var:
                                count += 1                
                
                return count

        def print(self):
                r = len(self.name)
                for i in range(r):
                        print(self.name[i] + ' ' + self.kind[i] + ' ' + self.type[i] + ' '+ str(self.order[i]))
        def define(self, name, kind, type):
                self.order.append(self.varCount(kind))
                self.name.append(name)
                self.kind.append(kind)
                self.type.append(type)
                if kind == 'static':
                        SymbolTable.static += 1
                

        def indexOf(self, name):

                for i in range  (len(self.name)):
                        if self.name[i] == name:
                                return i

                return -1                

        def kindOf(self, name):
                index = self.indexOf(name)
                if index == -1:
                        return "NONE"
                return self.kind[index]




        def typeOf(self, name):
                index = self.indexOf(name)
                if index == -1:
                        return "NONE"
                return self.type[index]                

