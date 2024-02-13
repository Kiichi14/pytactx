import event
from state import SpecialAgent

agent = SpecialAgent("Etienne")
event.subscribe(agent)

# On boucle tant que notre agent est vie
while True:
  agent.update()
  
