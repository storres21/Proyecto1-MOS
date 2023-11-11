# *************************************************************************
# ***      Proyecto 1 MOS                                               ***
# ***                                                                   ***
# ***      Author: Paula Daza y Sofia Torres                            ***
# *************************************************************************


from pyomo.environ import *
from pyomo.opt import SolverFactory

Model = ConcreteModel()

Model.asignaciones = {'Taller1', 'Taller2', 'Parcial1', 'Parcial2', 'Proyecto'}
Model.caracteristicas = {'Dificultad', 'Tiempo', 'Porcentaje'}
Model.nAsignaciones = 5
Model.tiempoDisponible = 40


Model.P = Param(Model.asignaciones, Model.caracteristicas, initialize=0, mutable=True)

Model.P['Taller1', 'Porcentaje'] = 0.1
Model.P['Taller2', 'Porcentaje'] = 0.15
Model.P['Parcial1', 'Porcentaje'] = 0.25
Model.P['Parcial2', 'Porcentaje'] = 0.25
Model.P['Proyecto', 'Porcentaje'] = 0.25

Model.T = Param(Model.asignaciones, Model.caracteristicas, initialize=999, mutable=True)

Model.T['Taller1', 'Tiempo'] = 1
Model.T['Taller2', 'Tiempo'] = 3
Model.T['Parcial1', 'Tiempo'] = 6
Model.T['Parcial2', 'Tiempo'] = 4
Model.T['Proyecto', 'Tiempo'] = 8

Model.E = Param(Model.asignaciones, Model.caracteristicas, initialize=999, mutable=True)

Model.E['Taller1', 'Dificultad'] = 1
Model.E['Taller2', 'Dificultad'] = 5
Model.E['Parcial1', 'Dificultad'] = 7
Model.E['Parcial2', 'Dificultad'] = 10
Model.E['Proyecto', 'Dificultad'] = 8

#Variables de decision
# Me dice que prioridad le debo dar a esa asignacion
Model.x = Var(Model.asignaciones, domain=NonNegativeIntegers, bounds=(1,Model.nAsignaciones))


#Funcion objetivo 1 - maximizar el porcentaje de la nota
Model.obj1 = sum(Model.x[i]*Model.P[i,'Porcentaje'] for i in Model.asignaciones)

Model.obj2 = sum(Model.x[i]*-(Model.T[i,'Tiempo']) for i in Model.asignaciones)

Model.obj3 = sum(Model.x[i]*-(Model.E[i,'Dificultad']) for i in Model.asignaciones)

#Funcion  objetivo
Model.Obj = Objective(expr= Model.obj1 + Model.obj2 + Model.obj3, sense=maximize)


#Siempre debo tener cuenta todas las asignaciones
Model.res1 = Constraint(expr=sum(Model.P[i,'Porcentaje'] for i in Model.asignaciones) == 1)


# Restricciones para asegurarse de que dos asignaciones no tengan la misma prioridad

Model.res2 = ConstraintList()
for i in Model.asignaciones:
    for j in Model.asignaciones:
        if i != j:
           Model.res2.add(abs(Model.x[i] - Model.x[j]) >= 1 )

# Restricción de tiempo total
Model.res3 = Constraint(expr=sum(Model.x[i] * Model.T[i, 'Tiempo'] for i in Model.asignaciones) <= Model.tiempoDisponible)


# Aplicación del solver
SolverFactory('ipopt').solve(Model)
Model.display()
