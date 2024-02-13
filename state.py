from stateMachine import State, StateMachine
from j2l.pytactx.agent import Agent, IAgent
from getpass import getpass

class ScanState(State):
  ## Récupération de l'état présent dans la StateMachine
  def __init__(self, stateMachine, agent:IAgent):
    super().__init__(stateMachine)
    self.__agent = agent
    self.__icp = 0
    self.__cp = [(18,20), (7, 2), (2,2), (2, 12)]
  ## Actions a réaliser dans l'état présent
  def doAction(self):
    ## Ajouter code de transition et de recherche d'ennemie
    self.__agent.fire(False)
    self.__agent.setColor(0,255,0)
    # Si la distance avec un ennemie est différent de 0 on change d'état 
    if self.__agent.distance != 0:
      self._parent.setState(AttackState(self._parent, self.__agent))
      return

    # On parcourt le tableau de position afin d'effectuer une ronde
    cpx, cpy = self.__cp[self.__icp]
    if not (self.__agent.x == cpx and self.__agent.y == cpy):
      self.__agent.moveTowards(cpx, cpy)
    else:
      self.__icp = (self.__icp + 1) % len(self.__cp)

class AttackState(State):
  ## Récupération de l'état présent dans la StateMachine
  def __init__(self, stateMachine, agent:IAgent):
      super().__init__(stateMachine)
      self.__agent = agent
      self.__xEnnemy = 0
      self.__yEnnemy = 0
  ## Actions a réaliser dans l'état présent
  def doAction(self):
    ## Ajouter code de transition et d'attaque
    # Si la position de l'agent correspond a la derniere position d'un ennemie on repasse ne mode scan
    if(self.__agent.x == self.__xEnnemy and self.__agent.y == self.__yEnnemy):
      self._parent.setState(ScanState(self._parent, self.__agent))

    # On capture les coordonnée d'un ennemi et on enregistre sa position dans les variables xEnnemy et yEnnemy
    if len(self.__agent.range) != 0:
      for ennemyName, ennemyAttributes in self.__agent.range.items():
        self.__xEnnemy, self.__yEnnemy = ennemyAttributes['x'], ennemyAttributes['y']
        break
        
    self.__agent.fire(True)
    self.__agent.setColor(255, 0, 0)
    self.__agent.moveTowards(self.__xEnnemy, self.__yEnnemy)  
    
class SpecialAgent:
  def __init__(self, playerID):
    # Initialise un Agent pour le SpecialAgent
    self.__agent = Agent(playerID, arena="LaTerreDuMilieu", username="demo", password=getpass("Enter password: "), server="mqtt.jusdeliens.com", verbosity=2)
    # On passe l'état par défault dans la StateMachine
    self.__fsm = StateMachine(None)
    self.__fsm.setState(ScanState(self.__fsm, self.__agent))

    # Méthode update 
  def update(self):
    self.__agent.update()
    self.__fsm.doAction()

  def addEventListener(self, eventType, eventHandler):
    ...