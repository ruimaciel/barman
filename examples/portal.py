from barman.models import Static 
from barman.dofs import Node 
from barman.sections import Section
from barman.materials import LinearElastic 
from barman.elements import EulerBernoulli 


material = LinearElastic('steel', 200, 0.35)
section = Section(1,1);

node = [
    Node([0,0]), 
    Node([0,1]), 
    Node([2,1]), 
    Node([2,0])
]

model = Static()
model.append_element( EulerBernoulli([node[0], node[1]], section, material) )
model.append_element( EulerBernoulli([node[1], node[2]], section, material) )
model.append_element( EulerBernoulli([node[2], node[3]], section, material) )

