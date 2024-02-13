class StateMachine:
  ## On initialise la StateMachine avec un state de départ ( par défault: ScanState ) 
  def __init__(self, state:"State"):
      self.__actualState = state

  ## On fait appel a la méthode doAction du parent State
  def doAction(self):
      if self.__actualState != None:
          self.__actualState.doAction()

  ## Méthode qui met a jour le state en cours
  def setState(self, newState: "State"):
      self.__actualState = newState


class State:
  ## On initialise le State grace a la StateMachine
  def __init__(self, parentFSM:StateMachine):
      self._parent = parentFSM

  ## Méthode doAction a surchargé
  def doAction(self):
      """" to be overidden """
      pass