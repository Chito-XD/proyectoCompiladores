from functionDirectory import FunctionDirectory
from utils.queue import Queue
from constansts import PROCESO, PRINCIPAL

class ManagerSemantic():

    def __init__(self):
        self.directory = FunctionDirectory()
        self.currentType = None
        self.currentId = None
        self.currentVariables = Queue()
    
    def setCurrentType(self, var_type):
        self.currentType = var_type
    
    def setCurrentId(self, curr_id):
        self.currentId = curr_id
    
    def deleteCurrentType(self):
        self.currentType = None
    
    def deleteCurrentId(self):
        self.currentId = None

    def createFunctionDirectory(self, program_id):
        params = {
            "tipo": PROCESO
        }
        self.directory.createFunction(program_id, params)
    
    def addFunction(self, id):
        params = {
            "tipo": self.currentType
        }
        self.directory.createFunction(program_id, params)
    
    def createPrincipal(self):
        params = {
            "tipo": PRINCIPAL
        }
        self.directory.createFunction(program_id, params)
    
    def stashVariable(self, var):
        self.currentVariables.add(var)
    
    def storeVariables(self):
        while (not self.currentVariables.isEmpty() ):
            var = self.currentVariables.poll()
            params = {
                "key": var
                "tipo": self.currentType
                # "value": 
            }
            self.directory.addLocalVariable(self.currentId, params)
        self.deleteCurrentType()
    
    def updateVariable(self, var, value):
        params = {
            "key": var
            "value": value
        }
        self.directory.updateVariable(self.currentId, params)

    
    

    
    