# -*- coding: utf-8 -*-

class Memory:

    def __init__(self, name): # memory name
    	self.name = name
    	self.memoryDic = {}

    def has_key(self, name):  # variable name
        return name in self.memoryDic
    	
    def get(self, name):         # get from memory current value of variable <name>
        if name in self.memoryDic: return self.memoryDic[name]
        else: return False
    def put(self, name, value):  # puts into memory current value of variable <name>
        self.memoryDic[name] = value

    def __repr__(self):
        return "\n\t"+self.name+":: "+repr(self.memoryDic)

class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        self.memoryStack = [memory]

    def get(self, name):             # get from memory stack current value of variable <name>
        for i in reversed(self.memoryStack):
            if i.has_key(name): return i.get(name)
        return False
    def put(self, name, value): # puts into memory stack current value of variable <name>
        for i in reversed(self.memoryStack):
            if i.has_key(name):
                i.put(name, value)
                return True
        raise Exception("nie ma takiej zmiennej" + name)

    def push(self, memory): # push memory <memory> onto the stack
        self.memoryStack.append(memory)
    def pop(self):          # pops the top memory from the stack
        return self.memoryStack.pop()

    def shallowCopy(self):
        copy = MemoryStack()
        copy.memoryStack = list(self.memoryStack)
        return copy

    def __str__(self):
        return "stack:  "+str(self.memoryStack)

class FunctionMemory:

    def __init__(self):
        self.declaredFunctions = {}
        self.globalMemory = None

    def getFunction(self, functionName):
        return self.declaredFunctions[functionName][0]

    def getStack(self, functionName, functionCallMemory):
        stackToReturn = self.declaredFunctions[functionName][1].shallowCopy()
        stackToReturn.push(functionCallMemory)
        return stackToReturn

    def putFunction(self, functionName, argumentsMemory, functionNode):
        stack = MemoryStack(self.globalMemory)
        stack.push(argumentsMemory)
        self.declaredFunctions[functionName] = functionNode, stack

    def pushGlobalMemory(self, globalMemory):
        if self.globalMemory is not None: raise Exception("stos jest niepusty! chyba już jest ustawione")
        self.globalMemory = globalMemory