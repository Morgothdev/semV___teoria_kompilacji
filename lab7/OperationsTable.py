class OperationsTable:

    def __init__(self):
        self.ttype = {}
        self.addOperation('+','int','float','float')
        self.addOperation('-','int','float','float')
        self.addOperation('*','int','float','float')
        self.addOperation('/','int','float','float')

        self.addOperation('+','float','int','float')
        self.addOperation('-','float','int','float')
        self.addOperation('*','float','int','float')
        self.addOperation('/','float','int','float')

        self.addOperation('+','float','float','float')
        self.addOperation('-','float','float','float')
        self.addOperation('*','float','float','float')
        self.addOperation('/','float','float','float')

        self.addOperation('+','int','int','int')
        self.addOperation('-','int','int','int')
        self.addOperation('*','int','int','int')
        self.addOperation('/','int','int','int')
        self.addOperation('%','int','int','int')

        self.addOperation('==','float','float','int')
        self.addOperation('!=','float','float','int')
        self.addOperation('<','float','float','int')
        self.addOperation('>','float','float','int')
        self.addOperation('<=','float','float','int')
        self.addOperation('>=','float','float','int')

        self.addOperation('==','int','float','int')
        self.addOperation('!=','int','float','int')
        self.addOperation('<','int','float','int')
        self.addOperation('>','int','float','int')
        self.addOperation('<=','int','float','int')
        self.addOperation('>=','int','float','int')

        self.addOperation('==','float','int','int')
        self.addOperation('!=','float','int','int')
        self.addOperation('<','float','int','int')
        self.addOperation('>','float','int','int')
        self.addOperation('<=','float','int','int')
        self.addOperation('>=','float','int','int')

        self.addOperation('==','int','int','int')
        self.addOperation('!=','int','int','int')
        self.addOperation('<','int','int','int')
        self.addOperation('>','int','int','int')
        self.addOperation('<=','int','int','int')
        self.addOperation('>=','int','int','int')

        self.addOperation('EQ','string','string','int')
        self.addOperation('!=','string','string','int')
        self.addOperation('<','string','string','int')
        self.addOperation('>','string','string','int')


        self.addOperation('*','string','int','string')


    def addOperation(self, operator, leftSide, rightSide, result):
        #wstawienie tego do slownika
        if not operator in self.ttype: self.ttype[operator] = {}
        if not leftSide in self.ttype[operator]: self.ttype[operator][leftSide] = {}
        if not rightSide in self.ttype[operator][leftSide]: 
            self.ttype[operator][leftSide][rightSide] = result
        else: 
            raise Error("jest juz w tablicy")


    def getOperationType(self, operator, leftSide, rightSide):
        if operator not in self.ttype: return None
        if leftSide not in self.ttype[operator]: return None
        if rightSide not in self.ttype[operator][leftSide]: return None
        return self.ttype[operator][leftSide][rightSide]
