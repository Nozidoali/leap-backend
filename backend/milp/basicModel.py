
import gurobipy as gp


class BasicModel:
    def __init__(self, clockPeriod: float) -> None:
        self._createModel()

        self.clockPeriod = clockPeriod
        self.__instructions = []

    def loadModel(self, fileName: str):
        self.model = gp.read(fileName)

    def dumpModel(self, fileName: str):
        self.model.write(filename=fileName)

    def loadInstructions(self, fileName: str):
        with open(fileName, "r") as f:
            for line in f:
                self.__instructions.append(line.strip())

    def solve(self):
        self.model.optimize()
        if self.model.status == gp.GRB.INFEASIBLE:
            assert False, "Model is infeasible"
        assert self.model.status == gp.GRB.OPTIMAL, "Model is not optimal"

    def getDepth(self):
        raise NotImplementedError
    
    def getLatency(self):
        raise NotImplementedError
    
    def _createModel(self):
        with gp.Env(empty=True) as env:
            env.setParam("OutputFlag", 0)
            env.start()
            self.model = gp.Model(env=env)
            
def constr2Str(model: gp.Model, constr: gp.Constr):
    output = None
    constrType = constr.Sense
    if constrType == gp.GRB.LESS_EQUAL:
        output = f"{constr.ConstrName}: {model.getRow(constr)} <= {constr.RHS}"
    elif constrType == gp.GRB.GREATER_EQUAL:
        output = f"{constr.ConstrName}: {model.getRow(constr)} >= {constr.RHS}"
    elif constrType == gp.GRB.EQUAL:
        output = f"{constr.ConstrName}: {model.getRow(constr)} = {constr.RHS}"
    else:
        raise ValueError(f"Unknown constraint type: {constrType}")
    return output
        
def lpModel2Str(model: gp.Model):
    output = []

    output.append(f"Model Name: {model.ModelName}\n")

    output.append("Variables:\n")
    for var in model.getVars():
        # skip X if the model is not solved
        if model.Status == gp.GRB.Status.OPTIMAL:
            output.append(f"  {var.VarName}: {var.X}\n")
        else:
            output.append(f"  {var.VarName}\n")

    output.append("Constraints:\n")
    for constr in model.getConstrs():
        output.append(constr2Str(model, constr) + "\n")

    output.append(f"Objective: {model.getObjective()}\n")
    return "".join(output)
