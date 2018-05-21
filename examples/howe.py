from barman import models
from barman import materials, dofs, sections
from barman.prescribed_displacements import PrescribedDisplacement
from barman.elements import Bar2 

from barman.analysis import LinearStatic


material = materials.LinearElastic('steel', 200, 0.35)
section = sections.Section(1,1);

node = [
    dofs.Node([0,0]), 
    dofs.Node([1,0]), 
    dofs.Node([1,1]),
    dofs.Node([2,0]), 
]

model = models.Static()
model.append_element( Bar2([node[0], node[1]], section, material) )
model.append_element( Bar2([node[1], node[2]], section, material) )
model.append_element( Bar2([node[0], node[2]], section, material) )
model.append_element( Bar2([node[1], node[3]], section, material) )
model.append_element( Bar2([node[2], node[3]], section, material) )

model.append_prescribed_displacement( PrescribedDisplacement( dofs.GlobalDoF(node[0], dofs.Parameter.dx), 0))
model.append_prescribed_displacement( PrescribedDisplacement( dofs.GlobalDoF(node[0], dofs.Parameter.dy), 0))
model.append_prescribed_displacement( PrescribedDisplacement( dofs.GlobalDoF(node[2], dofs.Parameter.dx), 0))
model.append_prescribed_displacement( PrescribedDisplacement( dofs.GlobalDoF(node[2], dofs.Parameter.dy), 0))

analysis = LinearStatic()
result = analysis.run(model)
