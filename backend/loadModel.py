"""
Copyright (c) 2024 Hanyu Wang <https://github.com/Nozidoali>

Created Date: Monday, August 26th 2024, 12:09:42 am
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
"""

import gurobipy as gp

# Create a Gurobi environment with quiet mode enabled
env = gp.Env(empty=True)
env.setParam("OutputFlag", 0)
env.start()


def loadModel(filename: str):
    import re
    import gurobipy as gp

    model = gp.Model(env=env)
    name2var = {}
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()

            # append the next line if line is not ended with ;
            while not line.endswith(";"):
                line += " " + lines.pop(0).strip()

            # remove the ; at the end
            line = line[:-1].strip()

            # skip empty line
            if not line:
                continue

            # remove comments /* */
            m = re.findall(r"/\*.*?\*/", line)
            for comment in m:
                line = line.replace(comment, "")
            line = line.strip()

            # TODO: handle the case of max: and min: in the same file
            if line.startswith("min: "):
                # parse the equation
                line = line.split(":")[1]
                values = line.split()

                objFunc = gp.LinExpr()
                for name in values:
                    # deal with the coefficient
                    if name[0] in "+-":
                        sign = name[0]
                        coeffient = 1 if sign == "+" else -1
                        name = name[1:]
                    else:
                        sign = "+"

                    if name not in name2var:
                        name2var[name] = model.addVar(name=name)

                    objFunc.addTerms(coeffient, name2var[name])

                model.update()
                model.setObjective(objFunc, gp.GRB.MINIMIZE)
                continue

            constrName = None
            # remove the name of the constraints:
            if ":" in line:
                constrName = line.split(":")[0].strip()
                line = line.split(":")[1]

            constrType = None
            sep = None
            if " <= " in line:
                constrType = gp.GRB.LESS_EQUAL
                sep = "<="
            elif " >= " in line:
                constrType = gp.GRB.GREATER_EQUAL
                sep = ">="
            elif " = " in line:
                constrType = gp.GRB.EQUAL
                sep = "="
            else:
                raise ValueError(f"Invalid constraint: {line}")

            lhs = line.split(sep)[0].strip()
            rhs = line.split(sep)[1].strip()

            constr = gp.LinExpr()
            for name in lhs.split():
                # deal with the coefficient
                if name[0] in "+-":
                    sign = name[0]
                    coeffient = 1 if sign == "+" else -1
                    name = name[1:]
                else:
                    sign = "+"
                    coeffient = 1

                if name not in name2var:
                    name2var[name] = model.addVar(name=name)
                constr.addTerms(coeffient, name2var[name])

            rhs = float(rhs)

            model.addLConstr(constr, constrType, rhs)
            continue
    model.update()

    # solve the model
    model.optimize()

    return model

