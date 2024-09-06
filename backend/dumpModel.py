'''
Copyright (c) 2024 Hanyu Wang <https://github.com/Nozidoali>

Created Date: Monday, August 26th 2024, 8:06:10 am
Author: Hanyu Wang

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
contributors may be used to endorse or promote products derived from this
software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS AS
IS AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.

HISTORY:
Date      	By	Comments
----------	---	----------------------------------------------------------
'''

import gurobipy as gp

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
