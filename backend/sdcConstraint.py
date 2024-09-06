'''
Copyright (c) 2024 Hanyu Wang <https://github.com/Nozidoali>

Created Date: Monday, August 26th 2024, 7:51:14 am
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

import numpy as np
import gurobipy as gp

from .dumpModel import *

class SdcConstriant:
    
    def __init__(self, posVar: str, negVar: str, constant: int = 0, sense = gp.GRB.EQUAL) -> None:
        self.posVar = str(posVar)
        self.negVar = str(negVar)
        self.constant = constant
        self.sense = sense
        
    def getPosVar(self):
        return self.posVar
    
    def getNegVar(self):
        return self.negVar
    
    def getConstant(self):
        return self.constant
    
    def getSense(self):
        return self.sense
    

def extractSDCconstraints(model: gp.Model):
    constraints = []
    for constr in model.getConstrs():
        constrType = constr.Sense

        expr: gp.LinExpr = model.getRow(constr)
        
        if expr.size() > 2:
            # SDC constraints should only have 2 variables
            print(f"Warning: constraint {constr2Str(model, constr)} has size != 2 and is not a SDC constraint")
            continue
        
        isSDC = True
        posVar, negVar = None, None
        for i in range(expr.size()):
            var = expr.getVar(i)
            coef = expr.getCoeff(i)
            if constrType != gp.GRB.LESS_EQUAL:
                if np.isclose(coef, 1.0):
                    posVar = var
                elif np.isclose(coef, -1.0):
                    negVar = var
                else:
                    isSDC = False
                    print(f"coeff: {coef}, constrType: {constrType}")
                    break
            else:
                if np.isclose(coef, 1.0):
                    negVar = var
                elif np.isclose(coef, -1.0):
                    posVar = var
                else:
                    isSDC = False
                    print(f"coeff: {coef}, constrType: {constrType}")
                
        # SDC constraints should have 1 positive and 1 negative variable
        if not isSDC:
            print(f"Warning: constraint {constr2Str(model, constr)} is not a SDC constraint")
            continue
        
        constraint = SdcConstriant(posVar, negVar, int(constr.RHS), constrType)
        constraints.append(constraint)

    return constraints