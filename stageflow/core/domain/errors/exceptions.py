
class StageFlowException(Exception):
    """Base exception for StageFlow"""

class WorkflowNotFoundException(StageFlowException):
    pass

class InstanceNotFoundException(StageFlowException):
    pass

class ConcurrentTransitionException(StageFlowException):
    pass

class InvalidTansitionException(StageFlowException):
    pass

class RuleVoilationException(StageFlowException):
    pass